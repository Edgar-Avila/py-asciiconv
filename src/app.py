from argparse import ArgumentParser, BooleanOptionalAction
from ffpyplayer.player import MediaPlayer
from grayscale import Grayscale
from display import *
from util import *
import cv2 as cv

class App:
    def __init__(self) -> None:
        self.filename: str | None = ''
        self.grayscale: Grayscale = Grayscale.NORMAL

    def parse_args(self) -> None:
        parser = ArgumentParser(description='Convert images and videos to ascii.')
        parser.add_argument('-f', '--filename', help='File to convert', type=media_path)
        parser.add_argument('-g', '--grayscale', help='Which grayscale to use', default=Grayscale.NORMAL ,type=Grayscale, choices=list(Grayscale))
        args = parser.parse_args()
        self.filename = args.filename
        self.grayscale = args.grayscale

    def run(self) -> None:
        self.parse_args()
        asciimap = self.grayscale.asciimap()

        if self.filename is None:
            video = cv.VideoCapture(0)
            display_camera(video, asciimap)
            video.release()

        elif is_img_path(self.filename):
            img = cv.imread(self.filename)
            display_img(img, asciimap)
        
        elif is_video_path(self.filename):
            video = cv.VideoCapture(self.filename)
            player = MediaPlayer(self.filename)
            display_video(video, player, asciimap)
            video.release()
