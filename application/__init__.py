from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_redis import FlaskRedis
from sqlalchemy.engine import Engine
from sqlalchemy import event
from flask_cors import CORS

db = SQLAlchemy()


def init_app():
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')
    CORS(app, supports_credentials=True)
    db.init_app(app)

    with app.app_context():
        from . import routes

        from . import dbmodels
        db.create_all()

        return app


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
