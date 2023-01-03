import os

def media_path(file_path: str) -> str:
    if os.path.isfile(file_path):
        _, ext = os.path.splitext(file_path)
        if ext in ('.mp4', '.avi', '.jpg', '.png'):
            return file_path
        raise 'File format not valid'
    raise FileNotFoundError(file_path)