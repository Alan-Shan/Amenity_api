from datetime import datetime
from functools import wraps

import jwt
from flask import session, current_app
from flask_socketio import emit, join_room, leave_room
from . import socketio
from .dbmodels import User


def login_required(f):
    """Wrapper connected to JWT tokens in API part of the app"""
    @wraps(f)
    def decorated(message, user=None):
        try:
            data = jwt.decode(message['token'], current_app.config['SECRET_KEY'])
            user = User.query.filter_by(id=data['identity']).first()
            if (user is None) or (datetime.fromtimestamp(data['exp']) < datetime.now()):
                emit('error', {'msg': 'invalid_token'}, namespace='/errors')
                return False
        except jwt.exceptions.ExpiredSignatureError as e:
            emit('error', {'msg': 'invalid_token'}, namespace='/errors')
            return False
        return f(message, user)

    return decorated


@socketio.on('joined', namespace='/chat')
@login_required
def joined(data, user):
    """Emitted by client on connect,
    response emitted from the server to all connected clients"""

    room = data['room']
    join_room(room)
    print(room + " for " + user.username)
    emit('status', {'msg': user.username + ' has entered the room.'}, room=room)


@socketio.on('text', namespace='/chat')
@login_required
def text(data, user):
    """Messages def"""
    room = data['room']
    emit('message', {'msg': user.username + ':' + data['msg']}, room=room)


@socketio.on('left', namespace='/chat')
@login_required
def left(data, user):
    """"Emitted by client when they leave a room,
    response emitted from the server to all connected clients"""
    room = data['room']
    leave_room(room)
    emit('status', {'msg': user.username + ' has left the room.'}, room=room)
