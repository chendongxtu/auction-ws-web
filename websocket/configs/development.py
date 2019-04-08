import os

DEBUG = True
TESTING = False

FLASK_ENV = 'development'
REDIS_SENTINEL = ''
SERVER_NAME = os.getenv('SERVER_NAME', 'a.com')

SENTRY_ENVIRONMENT = 'development'
SENTRY_CONFIG = {
}
