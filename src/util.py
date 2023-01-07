import os
from typing import Tuple

IMG_EXTS = ('.jpg', '.png')
VIDEO_EXTS = ('.mp4', '.avi')
TXT_EXTS = ('.txt',)


################################################
# File path validation helpers for the parser #
################################################
def out_path_creatable(file_path: str) -> str:
    try:
        with open(file_path, 'r') as _:
            pass
        if not is_img_or_txt_path(file_path):
            raise 'File extension not valid'
        return file_path
    except IOError:
        try:
            with open(file_path, 'w') as _:
                pass
            os.remove(file_path)
            if not is_img_or_txt_path(file_path):
                raise 'File extension not valid'
            return file_path
        except IOError:
            raise 'File path not valid'


def type_path(file_path: str, type: Tuple[str]) -> str:
    if os.path.isfile(file_path):
        _, ext = os.path.splitext(file_path)
        if ext in type:
            return file_path
        raise 'File format not valid'
    raise FileNotFoundError(file_path)


def img_path(file_path: str) -> str:
    return type_path(file_path, IMG_EXTS)


def img_or_txt_path(file_path: str) -> str:
    return type_path(file_path, IMG_EXTS + TXT_EXTS)


def media_path(file_path: str) -> str:
    return type_path(file_path, IMG_EXTS + VIDEO_EXTS)

#####################################################
# File path validation helpers for boolean checking #
#####################################################


def is_type_path(file_path: str, type: Tuple[str]) -> bool:
    _, ext = os.path.splitext(file_path)
    if ext in type:
        return True
    return False


def is_img_path(file_path: str) -> bool:
    return is_type_path(file_path, IMG_EXTS)


def is_video_path(file_path: str) -> bool:
    return is_type_path(file_path, VIDEO_EXTS)


def is_txt_path(file_path: str) -> bool:
    return is_type_path(file_path, TXT_EXTS)


def is_img_or_txt_path(file_path: str) -> bool:
    return is_type_path(file_path, IMG_EXTS + TXT_EXTS)
