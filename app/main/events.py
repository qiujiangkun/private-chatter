from flask import session, request
from flask_socketio import emit, join_room, leave_room
from .. import socketio

USER_NAMES = {}


@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = message['room']
    join_room(room)
    user = session.get('name')
    USER_NAMES[request.sid] = {'user': user, 'room': room, 'pubkey': message['pubkey']}
    emit('status', {'msg': user + ' has entered the room.', 'user': user, 'type': 'entered'}, room=room)


@socketio.on('text', namespace='/chat')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""

    data = USER_NAMES.get(request.sid)
    room = data['room']
    user = data['user']
    message['sender'] = user
    emit('message', message, room=room)


@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    data = USER_NAMES.get(request.sid)
    room = data['room']
    user = data['user']
    leave_room(room)
    emit('status', {'msg': user + ' has left the room.', 'user': user, 'type': 'left'}, room=room)


@socketio.on('disconnect', namespace='/chat')
def disconnect():
    data = USER_NAMES.get(request.sid)
    if data:
        del USER_NAMES[request.sid]
        emit('status', {'msg': data['user'] + ' has left the room.', 'user': data['user']}, room=data['room'])


@socketio.on('online_users', namespace='/chat')
def online_users():
    data = USER_NAMES.get(request.sid)
    room = data['room']

    users = []
    for data in USER_NAMES.values():
        if data['room'] == room:
            users.append({
                'user': data['user'],
                'pubkey': data['pubkey']
            })
    emit('status', {'users': users, 'type': 'list'}, room=room)
