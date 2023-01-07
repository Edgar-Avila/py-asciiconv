import cv2 as cv
from typing import List
from convert import convert_img
import os


def save_img(size, img: cv.Mat, asciimap: List[str], filename: str):
    rows, cols = size
    resized = cv.resize(img, (cols - 1, rows - 1))
    converted = convert_img(resized, asciimap)
    out_path, _ = os.path.splitext(filename)
    out_path = f'{out_path}.txt'
    with open(out_path, 'w') as file:
        file.write(converted)
    print(f'File saved to {out_path}')
