import eventlet
import socketio
from threading import Thread
from zlib import compress
import time
import pyautogui

from mss import mss

_sio = socketio.Client()

link = "http://127.0.0.1:3000"

WIDTH = 1900
HEIGHT = 1000

def gotta_share():
    __sio = socketio.Client()
    __sio.connect(link)
    time.sleep(5)
    while True:
        with mss() as sct:
            # The region to capture
            rect = {'top': 0, 'left': 0, 'width': WIDTH, 'height': HEIGHT}

            while True:
                # Capture the screen
                img = sct.grab(rect)
                # Tweak the compression level here (0-9)
                pixels = compress(img.rgb, 6)

                # Send the size of the pixels length
                size = len(pixels)
                size_len = (size.bit_length() + 7) // 8
                final_size_len = bytes([size_len])
                #conn.send(bytes([size_len]))

                # Send the actual pixels length
                size_bytes = size.to_bytes(size_len, 'big')
                final_size_bytes = size_bytes
                #conn.send(size_bytes)

                # Send pixels
                #conn.sendall(pixels)
                
                __sio.emit('sending_screenshot', {'data': {
                    'size_len': final_size_len,
                    'size_bytes': final_size_bytes, 
                    'pixels': pixels
                }})
                time.sleep(0.5) #Don't overload the server
                
@_sio.event
def connect():
    Thread(target=gotta_share).start()
    
@_sio.event
def receiveing_mouse_click(data):
    pyautogui.click(x=data['data']['x'], y=data['data']['y'])
                
_sio.connect(link)