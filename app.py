from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import random

app = Flask(__name__)
socketio = SocketIO(app)

# Store connected users, key: sid, value: dict with username and avatar
users = {}

@app.route('/')
def index():
    return render_template('index.html')

# Listening for the connect event
@socketio.on('connect')
def handle_connect():
    username = f"User_{random.randint(1000, 9999)}"
    gender = random.choice(['girl', 'boy'])
    avatar_url = f"https://avatar.iran.liara.run/public/{gender}?username={username}"

    # Store this user info in the users dictionary
    users[request.sid] = {"username": username, "avatar": avatar_url}

    # Notify all users
    emit("user_joined", {'username': username, 'avatar': avatar_url}, broadcast=True)
    emit('set_username', {'username': username})

# Delete the user on disconnect
@socketio.on('disconnect')
def handle_disconnect():
    user = users.pop(request.sid, None)
    if user:
        emit('user_left', {'username': user['username']}, broadcast=True)

# Handle sendMessage
@socketio.on('send_message')
def handle_message(data):
    user = users.get(request.sid)
    if user:
        emit('new_message', {
            'username': user['username'],
            'avatar': user['avatar'],
            'message': data['message']
        }, broadcast=True)

# Handle update_Username
@socketio.on('update_username')
def handle_update_username(data):
    old_username = users[request.sid]['username']
    new_username = data['username']  

    # Update the username in the users dictionary
    users[request.sid]['username'] = new_username

    # Notify users about the username update
    emit('username_updated', {
        'old_username': old_username,
        'new_username': new_username,
    }, broadcast=True)

if __name__ == '__main__':
    socketio.run(app)
