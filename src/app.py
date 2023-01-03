from argparse import ArgumentParser, BooleanOptionalAction
from grayscale import Grayscale
from util import media_path, is_img_path
from display import display_img
import cv2 as cv

class App:
    def __init__(self) -> None:
        self.filename: str = ''
        self.grayscale: Grayscale = Grayscale.NORMAL
        self.audio: bool = False

    def parse_args(self) -> None:
        parser = ArgumentParser(description='Convert images and videos to ascii.')
        parser.add_argument('-f', '--filename', help='File to convert', default='', type=media_path)
        parser.add_argument('-g', '--grayscale', help='Which grayscale to use', default=Grayscale.NORMAL ,type=Grayscale, choices=list(Grayscale))
        parser.add_argument('-a', '--audio', help='Play video with audio', default=False, action=BooleanOptionalAction)
        args = parser.parse_args()
        self.filename = args.filename
        self.grayscale = args.grayscale
        self.audio = args.audio

    def run(self) -> None:
        self.parse_args()
        asciimap = self.grayscale.asciimap()

        if is_img_path(self.filename):
            img = cv.imread(self.filename)
            display_img(img, asciimap)