from curses import wrapper
from display_util import *
from typing import List
import cv2 as cv
from time import sleep
from ffpyplayer.player import MediaPlayer
from save import save_img, save_img_media


def display(func):
    def wrap(*args, **kwds):
        wrapper(func, *args, *kwds)
    return wrap


@display
def save_display_img(screen, img: cv.Mat, asciimap: List[str], filename: str):
    size = screen.getmaxyx()
    save_img_media(size, img, asciimap, filename)
    screen.timeout(0)
    while True:
        draw_img(screen, img, asciimap)
        if qpressed(screen):
            break
        sleep(0.01)


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
