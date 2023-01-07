import cv2 as cv
from typing import List
from convert import convert_img


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
