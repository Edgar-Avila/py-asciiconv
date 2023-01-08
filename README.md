# AsciiConv

A python program to convert images and videos to ascii.

## Usage
### Exit
To quit the app at any time you can press q.
### Commands
* ***display:*** Display from an image, video or camera source
  * _***input (i):***_ Input file _(Leave empty to take from camera)_
* ***save***: Saves an image _(Video not supported)_
  * _***input (i):***_ Input file
  * _***output (o):***_ Output file _(Can be txt, jpg or png)_
### Flags (App level)
* ***grayscale (g):*** How many values do you want to represent shades
  * _***binary:***_ Black and white
  * _***normal:***_ 10 values _(Recommended, default)_
  * _***extended:***_ A lot of values

### Resolution
You probably are not satisfied with the pixelated result that your terminal produces. 

The program takes up all the available space in your terminal and produces a resized output where the width is the number of characters your terminal can hold horizontally and the width is the number of characters your terminal can hold vertically. The original aspect ratio is not kept when displaying the image/video/camera.

So, to improve the resolution of the image you just need to decrease your font size and/or increase the size of your terminal.

Also, increasing too much the resolution of a video to display will slow down the processing of the images and decrease the overall quality, since the app will try to skip some frames to keep up with the audio.

## Installation
This project uses poetry to manage its dependencies, all you have to do is install poetry following their [installation guide](https://python-poetry.org/docs/).

### Install dependencies
Place yourself int the project root and run:
```properties
poetry install
```
Or you can install the dependencies by hand using pip

> _***NOTE:***_ Don't forget to check that your python version is correct.

### Activate env
Check the directory where the env was created:
```properties
poetry env info --path
```

Then activate the environment using the path you just got. ***This differs between different OS***, for example using Windows and Powershell:
```properties
<env_path>\Scripts\activate.ps1
```

### Start the app
Then you should be able to run any command like:

```properties
python ./src/main.py display -i <input_file>
```

or

```properties
python ./src/main.py -g binary display -i <input_file> -o <output_file>
```