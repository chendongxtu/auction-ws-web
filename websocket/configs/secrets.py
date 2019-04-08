import os

SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'd664489ed846cc258cd5525017f1bc48')

REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')

SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', '')

