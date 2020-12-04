import datetime
import uuid

import sqlalchemy
from flask import make_response, current_app as app, jsonify, request
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash
from application.dbmodels import *
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, create_refresh_token,
    get_jwt_identity, jwt_refresh_token_required
)

JWTManager(app)


def check_adm(user_id):  # check for admin rights
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return False
    if user.role == 'admin':
        return True
    else:
        return False


###############################################
# AUTH SECTION
###############################################

@app.route('/auth', methods=['GET', 'POST'])  # Main auth endpoint
def authentication():
    """
    Basic Auth method
    You can use either GET or POST methods

    :params: Basic auth string (login and pass)
    :return: auth token and refresh token
    """
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

    user = User.query.filter_by(username=auth.username).first()

    if user is None:
        return jsonify({'error': 'Invalid auth!'}), 403

    if check_password_hash(user.password, auth.password):
        token = create_access_token(identity=user.id,
                                    expires_delta=datetime.timedelta(minutes=30))
        refreshtoken = create_refresh_token(identity=user.id,
                                            expires_delta=datetime.timedelta(days=7))
        return jsonify({'token': token,
                        'refresh_token': refreshtoken}), 200

    return make_response('could not verify', 403, {'WWW.Authentication': 'Basic realm: "login required"'})


@app.route('/refresh_token', methods=['POST'])  # Token refresher
@jwt_refresh_token_required
def refresh_token():
    """
    Auth token refresher
    POST ONLY

    :return: NEW auth token and NEW refresh token
    """
    try:
        user = User.query.filter_by(id=get_jwt_identity()).first()
        token = create_access_token(identity=user.id,
                                    expires_delta=datetime.timedelta(minutes=30))
        refreshtoken = create_refresh_token(identity=user.id,
                                            expires_delta=datetime.timedelta(days=30))
        return jsonify({'token': token,
                        'refresh_token': refreshtoken}), 200
    except AttributeError:
        return jsonify({'error': 'Token is invalid!'}), 401


###############################################
# CONTENT SECTION
###############################################

@app.route('/ping')  # Test connection
@jwt_required
def ping():
    return 'pong', 200