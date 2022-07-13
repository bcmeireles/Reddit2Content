import random
from random import randrange
import os
from moviepy.editor import VideoFileClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

def cutbg(length):
    background = VideoFileClip("background1.mp4")

    print(int(length))
    print(int(background.duration))
    
    start = randrange(180, int(background.duration) - int(length ))
    end = start + length 

    try:
        ffmpeg_extract_subclip(
            "background1.mp4",
            start,
            end,
            targetname="temp/background.mp4",
        )
    except (OSError, IOError):  # ffmpeg issue see #348
        print("FFMPEG issue. Trying again...")
        with VideoFileClip("background1.mp4") as video:
            new = video.subclip(start, end)
            new.write_videofile("temp/background.mp4")
    print("Background video chopped successfully!")