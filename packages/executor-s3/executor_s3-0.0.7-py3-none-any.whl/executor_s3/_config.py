import os
import json
from daggerml import Resource


TAG = 'com.daggerml.resource.s3'
DAG_NAME = TAG
DAG_VERSION = 1
CONFIG_FILE = os.path.expanduser(os.getenv('DML_S3_CONFIG', '~/.dml/s3.json'))

if os.path.isfile(CONFIG_FILE):
    with open(CONFIG_FILE, 'r') as f:
        conf = json.load(f)
else:
    conf = {}
GROUP = conf.get('group')
BUCKET = conf.get('bucket')
SECRET = conf.get('secret')
EXECUTOR = conf.get('executor')
if EXECUTOR is not None:
    EXECUTOR = Resource.from_dict(EXECUTOR)
