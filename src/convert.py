import cv2 as cv
from typing import List

def convert_img(img: cv.Mat, asciimap: List[str]) -> str:
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    out =  [[asciimap[val] for val in row] for row in gray]
    return '\n'.join([''.join(row) for row in out])