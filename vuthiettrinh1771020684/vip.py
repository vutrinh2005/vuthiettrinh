from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*") 

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('send_encrypted_message')
def handle_encrypted_message(data):

    room = data.get('room')
    message = data.get('message')

        emit('receive_encrypted_message', {'message': message}, room=room, include_self=False)

@socketio.on('join')
def on_join(data):
    room = data.get('room')
    if room:
        join_room(room)
        emit('status', {'msg': f'Bạn đã tham gia phòng {room}'})

@socketio.on('leave')
def on_leave(data):
    room = data.get('room')
    if room:
        leave_room(room)
        emit('status', {'msg': f'Bạn đã rời phòng {room}'})

if __name__ == '__main__':

    import eventlet
    eventlet.monkey_patch()
    socketio.run(app, host='0.0.0.0', port=5000)
