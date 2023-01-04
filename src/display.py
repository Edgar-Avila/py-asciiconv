from curses import wrapper
from convert import convert_img
from typing import List
from grayscale import Grayscale
import cv2 as cv
from time import sleep, time
from ffpyplayer.player import MediaPlayer
import os

# /////////////////////////////////////////
#    Utilities to help display an image
# /////////////////////////////////////////

def save_img(screen, img: cv.Mat, asciimap: List[str], filename: str):
    rows, cols = screen.getmaxyx()
    resized = cv.resize(img, (cols - 1, rows - 1))
    converted = convert_img(resized, asciimap)
    out_path, _ = os.path.splitext(filename)
    out_path = f'{out_path}.txt'
    with open(out_path, 'w') as file:
        file.write(converted)
    print(f'File saved to {out_path}')

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
def display_img(screen, img: cv.Mat, asciimap: List[str], filename: str | None):
    if filename is not None:
        save_img(screen, img, asciimap, filename)

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
    
    started = False
    # Play video
    while True:
        ret, img = video.read()
        frame, val = player.get_frame()
        if not ret:
            break
        if val == 'eof':
            break
        elif frame is None:
            # Sometimes val will not work
            # and we need to break using frame
            if not started:
                started = True
                sleep(0.01)
            else:
                break
        else: 
            while val == 0:
                ret, img = video.read()
                frame, val = player.get_frame()
                # Sometimes val will not work
                # and we need to break using frame
                if frame is None:
                    break
            sleep(val)
        draw_img(screen, img, asciimap)
        if qpressed(screen):
            break