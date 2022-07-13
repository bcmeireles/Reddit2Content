from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip, concatenate_audioclips, ImageClip, concatenate_videoclips, CompositeVideoClip
import multiprocessing
import re
import os
from os.path import exists
from moviepy.video.io import ffmpeg_tools

def makevideo(num, length, r_obj, sub):
    VideoFileClip.reW = lambda clip: clip.resize(width=1080)
    VideoFileClip.reH = lambda clip: clip.resize(width=1920)

    background_clip = (
        VideoFileClip("temp/background.mp4")
        .without_audio()
        .resize(height=1920)
        .crop(x1=1166.6, y1=0, x2=2246.6, y2=1920)
    )

    audio_clips = []
    for i in range(0, num):
        audio_clips.append(AudioFileClip(f"temp/mp3/{i}.mp3"))
    audio_clips.insert(0, AudioFileClip("temp/mp3/title.mp3"))
    audio_concat = concatenate_audioclips(audio_clips)
    audio_composite = CompositeAudioClip([audio_concat])

    total_length = sum([clip.duration for clip in audio_clips])
    int_total_length = round(total_length)

    image_clips = []

    image_clips.insert(
            0,
            ImageClip("temp/screenshots/title.png")
            .set_duration(audio_clips[0].duration)
            .set_position("center")
            .resize(width=1080 - 100),
        )

    for i in range(0, num):
        image_clips.append(
            ImageClip(f"temp/screenshots/comment_{i}.png")
            .set_duration(audio_clips[i + 1].duration)
            .set_position("center")
            .resize(width=1080 - 100),
        )

    image_concat = concatenate_videoclips(image_clips).set_position(("center", "center"))
    image_concat.audio = audio_composite
    final = CompositeVideoClip([background_clip, image_concat])
    title = re.sub(r"[^\w\s-]", "", r_obj["title"])
    idx = re.sub(r"[^\w\s-]", "", r_obj["id"])
    filename = f"{title}.mp4"

    if not exists(f"results/{sub}"):
        os.makedirs(f"results/{sub}")

    final.write_videofile(
        "temp/temp.mp4",
        fps=30,
        audio_codec="aac",
        audio_bitrate="192k",
        verbose=False,
        threads=multiprocessing.cpu_count(),
    )
    ffmpeg_tools.ffmpeg_extract_subclip(
        "temp/temp.mp4", 0, length, targetname=f"results/{sub}/{filename}"
    )