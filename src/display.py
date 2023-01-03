from curses import wrapper
from convert import convert_img
from typing import List
from grayscale import Grayscale
import cv2 as cv

# /////////////////////////////////////////
#    Utilities to help display an image
# /////////////////////////////////////////

def draw_img(screen, img: cv.Mat, asciimap: List[str]):
    rows, cols = screen.getmaxyx()
    resized = cv.resize(img, (cols - 1, rows - 1))
    screen.clear()
    screen.addstr(convert_img(resized, asciimap))
    screen.refresh()

def qpressed(screen, waittime):
    screen.timeout(waittime)
    if screen.getch() == ord('q'):
        return True
    return False


# /////////////////////////////////////////
#      The actual display functions
# /////////////////////////////////////////

def display(func):
    def wrap(*args, **kwds):
        wrapper(func, *args, *kwds)
    return wrap

@display
def display_img(screen, img: cv.Mat, asciimap: List[str]):
    while True:
        draw_img(screen, img, asciimap)
        if qpressed(screen, 10):
            break
