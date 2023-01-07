from argparse import ArgumentParser
from ffpyplayer.player import MediaPlayer
from grayscale import Grayscale
from display import *
from util import *
import cv2 as cv


# Display command
def display(args) -> None:
    asciimap = args.grayscale.asciimap()
    if args.input is None:
        video = cv.VideoCapture(0)
        display_camera(video, asciimap)
        video.release()
    elif is_img_path(args.input):
        img = cv.imread(args.input)
        display_img(img, asciimap)
    elif is_video_path(args.input):
        video = cv.VideoCapture(args.input)
        player = MediaPlayer(args.input)
        display_video(video, player, asciimap)
        video.release()
        player.close_player()


def save(args) -> None:
    asciimap = args.grayscale.asciimap()
    if is_img_path(args.input):
        img = cv.imread(args.input)
        save_mode = 'img' if is_img_path(args.output) else 'txt'
        size = display_img(img, asciimap)
        print(size)
        if save_mode == 'img':
            save_img_media(size, img, asciimap, args.output)
        elif save_mode == 'txt':
            save_img(size, img, asciimap, args.output)
    elif is_video_path(args.input):
        print('Saving videos is not supported yet.')
        exit(1)
    else:
        print('Invalid file type.')
        exit(1)


def parse_args() -> None:
    app_desc = 'Convert images and videos to ascii.'
    display_help = 'Display an image, video, or camera'
    save_help = 'Save an image'

    # App parser
    parser = ArgumentParser(description=app_desc)
    subparsers = parser.add_subparsers()
    parser.add_argument(
        '-g',
        '--grayscale',
        help='Which grayscale to use',
        default=Grayscale.NORMAL,
        type=Grayscale,
        choices=list(Grayscale)
    )

    # Display parser
    display_parser = subparsers.add_parser('display', help=display_help)
    display_parser.set_defaults(func=display)
    display_parser.add_argument(
        '-i',
        '--input',
        help='File to convert',
        type=media_path
    )

    # Save parser
    save_parser = subparsers.add_parser('save', help=save_help)
    save_parser.set_defaults(func=save)
    save_parser.add_argument(
        '-i',
        '--input',
        help='File to convert (image)',
        type=media_path,
        required=True
    )
    save_parser.add_argument(
        '-o',
        '--output',
        help='File to save (image or text)',
        type=out_path_creatable,
        required=True
    )

    return parser.parse_args()


def run() -> None:
    args = parse_args()
    args.func(args)
