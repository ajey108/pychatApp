from flask import Flask,render_template,request
from flask_socketio import SocketIO,emit
import random


app = Flask(__name__)
socketio = SocketIO(app)

#Store connected user key:sid value: username and avatarUrl
users = {}


@app.route('/')
def index():
    return render_template('index.html')

    #listening for the connect event
 @socketio.on('connect')
def handle_connect():
    username = f"User_{random.randint{1000,9999}}"
    gender = random.choice(['girl','boy'])
    avatar_Url = f "https://avatar.iran.liara.run/public/{gender}?username={username}"

    #store this user info in the users dictionary

    users[request.sid] = {"username":username,"avatar":avatar_Url}

    #notify all the user

    emit("user_joined",{'username':username,'avatar':avatar_Url},broadcast=True)

    emit('set_username',{'username':username})

#dlt the user

@socketio.on('disconnect')
def handle_disconnect:
    user = users.pop(request.sid,None)








if __name__ == '__main__':
        socketio.run(app)
        


