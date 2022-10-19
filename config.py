"""Logging Server configuration."""
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    """Base config."""
    LOG_SVR_DIGEST_KEY = str.encode(environ.get('LOG_SVR_DIGEST_KEY'))
    LOG_SVR_FILE = environ.get('LOG_SVR_FILE')
    LOG_SVR_IP = environ.get('LOG_SVR_IP')
    LOG_SVR_PORT = int(environ.get('LOG_SVR_PORT'))


class ProdConfig(Config):
    LOG_SVR_ENV = 'production'
    LOG_SVR_DEBUG = False
    LOG_SVR_TESTING = False


class DevConfig(Config):
    LOG_SVR_ENV = 'development'
    LOG_SVR_DEBUG = True
    LOG_SVR_TESTING = True
