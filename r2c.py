import math
from reddit.parser import getThreads
from tts.tts import SpeechEngine
from tts.voices import GTTS
import math
from reddit.screenshots import downloadScreenshots
from video.background import cutbg
from video.make import makevideo
from utils.cleaning import cleanup
from uploaders.insta import InstagramUploader

def text2mp3(r_obj):
    to_mp3 = SpeechEngine(GTTS, r_obj)
    return to_mp3.run()

def main(sub, doneVids=[]):
    gt = getThreads(sub, doneVids)
    infos, doneVids = gt["infos"], gt["doneVideos"]

    a = text2mp3(infos)
    length, count = math.ceil(a["length"]), a["idx"]
    downloadScreenshots(infos, count)
    cutbg(length)
    vidP = makevideo(count, length, infos, sub)
    cleanup()

    ig = InstagramUploader("idevfazt3stes", "Yoqu1201")
    ig.upload(vidP, ["askreddit", "quesiton", "reddit"])

    return doneVids


if __name__ == "__main__":
    sub = input("sub: ")
    doneVids = []
    while True:
        a = main(sub, doneVids)
        doneVids = a