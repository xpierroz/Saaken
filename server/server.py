import eventlet
import socketio

sio = socketio.Server()
app = socketio.WSGIApp(sio)

@sio.event 
def sending_screenshot(sid, data):
    print(f'{sid} - sending screenshot')
    sio.emit('receiving_screenshot', {'data': data['data']})
    
@sio.event
def mouse_click(sid, data):
    print("got some mouse clicks my g")
    sio.emit('receiveing_mouse_click', {'data': data['data']})


@sio.event
def connect(sid, environ):
    print(f'{sid} - connected')


if __name__ == '__main__':
    eventlet.wsgi.server(eventlet.listen(('', 5000)), app)
