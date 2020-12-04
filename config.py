from os import environ, path
from dotenv import load_dotenv

basedir = (path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class DevelopmentConfig:
    FLASK_ENV = 'development'
    TESTING = True
    DEBUG = True
    SECRET_KEY = environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL')
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_TOKEN_LOCATION = ('headers', 'query_string')
    JWT_QUERY_STRING_NAME = 'token'
    JWT_HEADER_TYPE = ''
