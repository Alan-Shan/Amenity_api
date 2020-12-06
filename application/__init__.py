from flask import Blueprint
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_socketio import SocketIO

socketio = SocketIO()
db = SQLAlchemy()
ma = Marshmallow()
main = Blueprint('main', __name__)


def create_app():
    """Create an application."""
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')
    CORS(app, supports_credentials=True)
    app.register_blueprint(main)
    socketio.init_app(app)
    db.init_app(app)
    ma.init_app(app)
    with app.app_context():
        from . import routes, events
        from . import dbmodels
        db.create_all()
        return app
