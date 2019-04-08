# -*- encoding: utf8 -*-

import os
import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.contrib.fixers import ProxyFix
from redis import StrictRedis
from raven.contrib.flask import Sentry
from flask_cors import CORS
from flask_socketio import SocketIO

logger = logging.getLogger(__name__)

db = SQLAlchemy()
redis = None
sentry = Sentry()
async_mode = "gevent"
socketio = SocketIO()


def init_config(app, config):
    env = os.getenv('FLASK_ENV', 'development')
    app.config.from_object("websocket.configs.default")
    app.config.from_object("websocket.configs.secrets")
    app.config.from_object("websocket.configs.{}".format(env))
    app.config.update(config or {})


def init_logging(app):
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)

    handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s [%(pathname)s:%(lineno)s] - %(message)s'))

    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(handler)

    if app.debug:
        sa_logger = logging.getLogger('sqlalchemy.engine')
        sa_logger.setLevel(logging.INFO)
        sa_logger.addHandler(handler)


def init_redis(app):
    global redis
    redis = StrictRedis.from_url(app.config['REDIS_URL'])


def create_app(config=None):

    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app)

    init_config(app, config)
    init_logging(app)
    init_redis(app)

    sentry.init_app(app)

    db.init_app(app)
    CORS(app, supports_credentials=True)
    socketio.init_app(app=app, async_mode=async_mode,
                      message_queue=app.config['REDIS_URL'],
                      channel='auction_car_info_broadcast')

    from .main  import main as blueprint_main
    app.register_blueprint(blueprint_main)

    from .test import test as test_blueprint
    app.register_blueprint(test_blueprint, url_prefix='/api/v1/test')

    return app


from . import models # noqa
