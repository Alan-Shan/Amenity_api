import datetime
import uuid

import sqlalchemy
import sqlalchemy.exc
from flask import make_response, current_app as app, jsonify, request
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash
from application.dbmodels import *
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, create_refresh_token,
    get_jwt_identity, jwt_refresh_token_required
)

from application.schemas import UserSchema, TerritoriesSchema, MarkersSchema

JWTManager(app)


def check_adm(user_id):  # check for admin rights
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return False
    return user.role


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


@app.route('/refresh_token', methods=['GET'])  # Token refresher
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


@app.route('/register', methods=['POST'])
def register():
    """Registers a new User"""
    try:
        form = request.get_json()
        hashed_password = generate_password_hash(form['password'], method='sha256')
        new_user = User(id=str(uuid.uuid4()),
                        username=form['username'],
                        password=hashed_password,
                        name=form['name'],
                        email=form['email'],
                        role=False)
        db.session.add(new_user)
        db.session.commit()

        # Database insertion failed
    except sqlalchemy.exc.IntegrityError as e:
        return jsonify({'error': 'Username is not unique or SQL Operation Failed'}), 500
        # Wrong type (probably the pass)
    except TypeError:
        return jsonify({'error': 'TypeError'}), 400

    return jsonify({'response': 'OK'}), 200


###############################################
# CONTENT SECTION
###############################################

@app.route('/ping')  # Test connection
@jwt_required
def ping():
    return get_jwt_identity(), 200


@app.route('/api/users', methods=['GET'])
@app.route('/api/users/<user_id>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@jwt_required
def users(user_id=None):
    if request.method == 'GET':
        if user_id is None:
            return jsonify(UserSchema(many=True).dump(User.query.all())), 200
        user = User.query.filter_by(id=user_id).first()
        if user is None:
            return jsonify({'error': 'Index out of bounds'}), 400
        return jsonify(UserSchema().dump(user)), 200


@app.route('/api/territories', methods=['GET', 'POST'])
@app.route('/api/territories/<territory_id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required
def territories(territory_id=None):
    if request.method == 'GET':
        if territory_id is None:
            return jsonify(TerritoriesSchema(many=True).dump(Territories.query.all())), 200
        territory = Territories.query.filter_by(id=territory_id).first()
        if territory is None:
            return jsonify({'error': 'Index out of bounds'}), 400
        return jsonify(TerritoriesSchema().dump(territory)), 200
    if request.method == 'POST':
        try:
            form = request.get_json()
            user_id = get_jwt_identity()
            if check_adm(user_id) is not True and form['user'] != user_id:
                form['user'] = user_id
            new_territory = Territories(id=str(uuid.uuid4()),
                                        name=form['name'],
                                        description=form['description'] if 'description' in form else '',
                                        user=form['user'])
            db.session.add(new_territory)
            for i, coordinate in enumerate(form['longitude']):
                db.session.add(TerritoryCoordinates(
                    id=str(uuid.uuid4()),
                    longitude=coordinate,
                    latitude=form['latitude'][i],
                    territory=new_territory.id
                ))
            db.session.commit()
            # Database insertion failed
        except sqlalchemy.exc.IntegrityError:
            return jsonify({'error': 'SQL Operation Failed'}), 500
        except TypeError:
            return jsonify({'error': 'TypeError'}), 400
        return jsonify({'response': 'OK'}), 200


@app.route('/api/markers', methods=['GET', 'POST'])
@app.route('/api/markers/<marker_id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required
def markers(marker_id=None):
    if request.method == 'GET':
        if marker_id is None:
            return jsonify(MarkersSchema(many=True).dump(Markers.query.all())), 200
        marker = Markers.query.filter_by(id=marker_id).first()
        if marker is None:
            return jsonify({'error': 'Index out of bounds'}), 400
        return jsonify(MarkersSchema().dump(marker)), 200
    if request.method == 'POST':
        try:
            form = request.get_json()
            new_marker = Markers(id=str(uuid.uuid4()),
                                 name=form['name'],
                                 description=form['description'] if 'description' in form else '',
                                 email=form['email'],
                                 latitude=form['latitude'],
                                 longitude=form['longitude'],
                                 territory=form['territory'],
                                 user=form['user'])
            db.session.add(new_marker)
            db.session.commit()
            # Database insertion failed
        except sqlalchemy.exc.IntegrityError:
            return jsonify({'error': 'SQL Operation Failed'}), 500
        except TypeError:
            return jsonify({'error': 'TypeError'}), 400
        return jsonify({'response': 'OK'}), 200
