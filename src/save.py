from math import ceil
from PIL import Image, ImageFont, ImageDraw
import cv2 as cv
from typing import List
from convert import convert_img
import os


def save_img(size, img: cv.Mat, asciimap: List[str], outfile: str):
    rows, cols = size
    resized = cv.resize(img, (cols - 1, rows - 1))
    converted = convert_img(resized, asciimap)
    with open(outfile, 'w') as file:
        file.write(converted)
    print(f'File saved to {outfile}')


def get_best_font(size: int):
    fonts = [
        'DejaVuSansMono.ttf',  # Linux
        'Consolas Mono.ttf',   # MacOS
        'Consolas.ttf',        # Windows
    ]
    for font_filename in fonts:
        try:
            return ImageFont.truetype(font_filename, size=size)
        except IOError:
            print(f'Could not load font "{font_filename}".')
    print('Using default font.')
    return ImageFont.load_default()


def text_to_image(text: str, fg_color: int = 255, bg_color: int = 0):
    lines = text.splitlines()
    font = get_best_font(20)
    max_line_w, max_line_h = -float('inf'), -float('inf')
    for line in lines:
        l, t, r, b = font.getbbox(line)
        max_line_w = max(max_line_w, r - l)
        max_line_h = max(max_line_h, b - t)
    img_w, img_h = max_line_w, max_line_h * len(lines)
    # L is for 8-bit pixels, black and white
    image = Image.new('L', (img_w, img_h), color=bg_color)
    draw = ImageDraw.Draw(image)
    draw.text((0, 0), text, fill=fg_color, font=font)
    return image


def resized_wh(img: cv.Mat, term_size, keep_ratio: bool):
    rows, cols = term_size
    h, w, _ = img.shape
    if keep_ratio:
        if w > h:
            ratio = w / h
            nw = cols - 1
            nh = ceil(nw / ratio)
        else:
            ratio = h / w
            nh = rows - 1
            nw = ceil(nh / ratio)
    else:
        nw = cols - 1
        nh = rows - 1
    return nw, nh


def save_img_media(size, img: cv.Mat, asciimap: List[str], outfile: str):
    h, w, _ = img.shape
    nw, nh = resized_wh(img, size, False)
    resized = cv.resize(img, (nw, nh))
    converted = convert_img(resized, asciimap)

    out = text_to_image(converted)
    # out = out.resize((w, h))
    out.show()
    out.save(outfile)
    print(f'File saved to {outfile}')
