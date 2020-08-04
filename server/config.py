import os

SERVER_ROOT_PATH = ''
SERVER_STATIC_PATH = SERVER_ROOT_PATH+"static/"
STATIC_MARKER_PATH = SERVER_STATIC_PATH+'marker/asmjs/1.0/unify/'
STATIC_IMAGE_PATH = SERVER_STATIC_PATH+'image/base/1.0/unify'
# os.system("mkdir -p {}".format(_STATIC_IMAGE_PATH))
# os.system("mkdir -p {}".format(_STATIC_MARKER_PATH))

try:
    REDIS_URL = os.environ['REDIS_URL']
except KeyError:
    REDIS_URL = 'redis://127.0.0.1:6379'

ASSET_HOST = 'https://kivicube-asset.oss-cn-hangzhou.aliyuncs.com'
