from curses import wrapper
from convert import convert_img
from typing import List
from grayscale import Grayscale
import cv2 as cv
from time import sleep, time

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

def fix_too_slow_skip(video: cv.VideoCapture, start: float, curr_frame: int, fps: int) -> int:
    should_be = correct_frame(start, fps)
    while should_be > curr_frame:
        ret, _ = video.read()
        if not ret:
            return -1
        should_be = correct_frame(start, fps)
        curr_frame += 1
    return curr_frame

def fix_too_fast_sleep(video: cv.VideoCapture, start: float, curr_frame: int, fps: int) -> None:
    should_be = correct_frame(start, fps)
    sleeptime = (curr_frame - should_be) / fps
    sleep(max(sleeptime, 0))

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
def display_video(screen, video: cv.VideoCapture, asciimap: List[str]):
    screen.timeout(0)
    fps = int(video.get(cv.CAP_PROP_FPS))
    start = time()
    curr_frame = 0
    while True:
        curr_frame = fix_too_slow_skip(video, start, curr_frame, fps)
        if curr_frame == -1:
            break
        ret, img = video.read()
        curr_frame += 1
        if not ret:
            break
        draw_img(screen, img, asciimap)
        fix_too_fast_sleep(video, start, curr_frame, fps)
        if qpressed(screen):
            break

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