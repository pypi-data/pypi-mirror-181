import os
import boto3
import base64
import tarfile
import logging
import daggerml as dml
from time import sleep
from uuid import uuid4
from hashlib import md5
from tempfile import NamedTemporaryFile
from botocore.exceptions import ClientError
from subprocess import PIPE, run as run_shell
from pkg_resources import get_distribution, DistributionNotFound
from daggerml._config import AWS_LOCALSTACK_ENDPOINT
from executor_s3._config import BUCKET, TAG, SECRET, GROUP, DAG_NAME, DAG_VERSION, EXECUTOR
try:
    __version__ = get_distribution("executor-s3").version
except DistributionNotFound:
    __version__ = 'local'


logger = logging.getLogger(__name__)
this_dir = os.path.dirname(os.path.realpath(__file__))


class S3Resource(dml.Resource):
    def __init__(self, resource_id, executor=EXECUTOR, tag=TAG):
        super().__init__(resource_id, executor, tag)

    @property
    def uri(self):
        return base64.decodebytes(self.id.encode()).decode()

dml.register_tag(TAG, S3Resource)


def md5sum(path):
    hash_md5 = md5()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def run_s3_dag(attempts_left=float('inf')):
    dag = dml.Dag.from_claim(EXECUTOR, SECRET, 1, GROUP)
    if dag is None:
        if attempts_left <= 0:
            raise RuntimeError('AHHHH exec_dag was None too many times!')
        return attempts_left - 1
    try:
        expr = dag.expr.to_py()
        assert len(expr) == 2 and len(expr[0]) == 2, 'malformed expression'
        assert isinstance(expr[1], str), 'malformed expression'
        dag.commit(S3Resource(expr[1], EXECUTOR))
        return attempts_left
    except Exception as e:
        dag.fail({'message': str(e), 'expr': expr})
        return attempts_left - 1


def resource_exec_fn(dag, resource_id):
    fn = dag.load(DAG_NAME, DAG_VERSION)
    assert fn[0].to_py().id == EXECUTOR.id, 's3 resource loaded has the wrong executor'
    resp = fn(resource_id, block=False)
    n_left = 1
    while resp.check() is None:
        n_left = run_s3_dag(n_left)
        sleep(1)
    return resp.result


def s3_obj_exists(s3_client, bucket, key):
    try:
        s3_client.head_object(Bucket=bucket, Key=key)
    except ClientError as e:
        return int(e.response['Error']['Code']) != 404
    return True


def upload_file(path, bucket, key):
    s3client = boto3.client('s3', endpoint_url=AWS_LOCALSTACK_ENDPOINT)
    if not s3_obj_exists(s3client, bucket, key):
        s3client.upload_file(path, bucket, key)
        return True
    return False


def exec_fn(f):
    def wrap(dag, *args, **kwargs):
        assert BUCKET is not None, 'bucket not configured'
        uri = f(*args, **kwargs)
        resource_id = base64.encodebytes(uri.encode()).decode().strip()
        return resource_exec_fn(dag, resource_id)
    return wrap


@exec_fn
def tar(path):
    path = os.path.abspath(path)
    logger.info('set path to: %r', path)
    with NamedTemporaryFile('w+') as f:
        with tarfile.open(f.name, "w:gz") as tar:
            tar.add(path, arcname='/')
        proc = run_shell([f'{this_dir}/hash-tar.sh', f.name], stdout=PIPE, stderr=PIPE)
        if proc.returncode != 0:
            raise RuntimeError('failed to get hash of file: %s', f.name)
        md5 = proc.stdout
        assert md5 is not None, 'bad md5sum'
        key = f'executor/s3/data/tar/{md5.decode()}.tar'
        upload_file(f.name, BUCKET, key)
    return f's3://{BUCKET}/{key}'


dml.Dag.s3_tar = tar


@exec_fn
def upload(path):
    path = os.path.abspath(path)
    logger.info('set path to: %r', path)
    md5_hash = md5sum(path)
    key = f'executor/s3/data/misc/{md5_hash}/' + path.split('/')[-1]
    upload_file(path, BUCKET, key)
    return f's3://{BUCKET}/{key}'


dml.Dag.s3_upload = upload


@exec_fn
def parquet(df):
    import pandas as pd
    import pandas.util as pu
    if not isinstance(df, pd.DataFrame):
        raise TypeError('df must be a dataframe')
    _hash = pu.hash_pandas_object(df).sum()
    key = f'executor/s3/data/dataframe-pandas/{_hash}.parquet'
    s3_loc = f's3://{BUCKET}/{key}'
    df.to_parquet(s3_loc)
    return s3_loc


@exec_fn
def new_prefix():
    return f's3://{BUCKET}/executor/s3/data/unique-prefix/{uuid4().hex}/'
