import os

def media_path(file_path: str) -> str:
    if os.path.isfile(file_path):
        if is_img_path(file_path) or is_video_path(file_path):
            return file_path
        raise 'File format not valid'
    raise FileNotFoundError(file_path)

def is_img_path(file_path: str) -> bool:
    _, ext = os.path.splitext(file_path)
    if ext in ('.jpg', '.png'):
        return True
    return False

def is_video_path(file_path: str) -> bool:
    _, ext = os.path.splitext(file_path)
    if ext in ('.mp4', '.avi'):
        return True
    return False