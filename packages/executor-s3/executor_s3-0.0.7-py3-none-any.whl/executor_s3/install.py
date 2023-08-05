#!/usr/bin/env python3
import os
import json
import argparse
from daggerml import Dag
from executor_s3._config import CONFIG_FILE, TAG, DAG_NAME, DAG_VERSION


GROUP = os.getenv('DML_S3_GROUP', TAG)
BUCKET = os.getenv('DML_S3_BUCKET')


def main(group, bucket, config_file):
    dag = Dag.new(DAG_NAME, DAG_VERSION, group)
    if dag is None:
        raise RuntimeError('dag %s:%s already exists!' % (TAG, DAG_VERSION))
    assert isinstance(bucket, str) and len(bucket) > 0, 'bad bucket: %r' % bucket
    conf = {
        'executor': dag.executor.to_dict(),
        'secret': dag.secret,
        'bucket': bucket,
        'group': dag.group,
    }
    dag.commit([dag.executor, 'upload'])
    with open(os.path.expanduser(config_file), 'w') as f:
        json.dump(conf, f)
    return


def cli():
    parser = argparse.ArgumentParser(prog='executor-s3 configurator',
                                     description='Configures executor-s3')
    parser.add_argument('-g', '--group', default=GROUP)
    parser.add_argument('-b', '--bucket', default=BUCKET)
    parser.add_argument('-c', '--config-file', default=CONFIG_FILE)
    args = parser.parse_args()
    main(args.group, args.bucket, args.config_file)


if __name__ == '__main__':
    cli()
