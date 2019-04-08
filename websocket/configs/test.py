import os

FLASK_ENV = 'test'

# 这个名字问kent，king他们要
SERVER_NAME = os.getenv('SERVER_NAME', 'auction.test.dos.cheanjia.net')

SENTRY_ENVIRONMENT = 'test'

