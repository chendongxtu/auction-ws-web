import os

FLASK_ENV = 'production'
    # 问kent，king他们要
SERVER_NAME = os.getenv('SERVER_NAME', 'uca.lixinchuxing.com')

SENTRY_ENVIRONMENT = 'production'
