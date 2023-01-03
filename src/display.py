from curses import wrapper
from convert import convert_img
from typing import List
from grayscale import Grayscale
import cv2 as cv
from time import sleep, time
from ffpyplayer.player import MediaPlayer

# /////////////////////////////////////////
#    Utilities to help display an image
# /////////////////////////////////////////

def draw_img(screen, img: cv.Mat, asciimap: List[str]):
    rows, cols = screen.getmaxyx()
    resized = cv.resize(img, (cols - 1, rows - 1))
    screen.clear()
    screen.addstr(convert_img(resized, asciimap))
    screen.refresh()

def qpressed(screen):
    if screen.getch() == ord('q'):
        return True
    return False

def correct_frame(start: float, fps: int) -> int:
    end = time()
    secs = end - start
    return int(fps * secs)

# /////////////////////////////////////////
#      The actual display functions
# /////////////////////////////////////////

def display(func):
    def wrap(*args, **kwds):
        wrapper(func, *args, *kwds)
    return wrap

@display
def display_img(screen, img: cv.Mat, asciimap: List[str]):
    screen.timeout(0)
    while True:
        draw_img(screen, img, asciimap)
        if qpressed(screen):
            break
        sleep(0.01)


@display
def display_camera(screen, video: cv.VideoCapture, asciimap: List[str]):
    screen.timeout(0)
    while True:
        ret, img = video.read()
        if not ret:
            break
        draw_img(screen, img, asciimap)
        if qpressed(screen):
            break
        sleep(0.01)

@display
def display_video(screen, video: cv.VideoCapture, player: MediaPlayer, asciimap: List[str]):
    screen.timeout(0)
    player.set_pause(False)
    # Wait for player to load
    while True:
        frame, val = player.get_frame()
        if frame is not None:
            ret, img = video.read()
            break
    
    # Play video
    while True:
        ret, img = video.read()
        frame, val = player.get_frame()
        if not ret:
            break
        if val == 'eof':
            break
        elif frame is None:
            sleep(0.01)
        else: 
            while val == 0:
                ret, img = video.read()
                frame, val = player.get_frame()
            sleep(val)
        draw_img(screen, img, asciimap)
        if qpressed(screen):
            break