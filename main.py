import math
from reddit.parser import getThreads
from tts.tts import SpeechEngine
from tts.voices import GTTS
import math
from reddit.screenshots import downloadScreenshots
from video.background import cutbg
from video.make import makevideo

def text2mp3(r_obj):
    to_mp3 = SpeechEngine(GTTS, r_obj)
    return to_mp3.run()

if __name__ == "__main__":
    infos = getThreads("AskReddit")

    a = text2mp3(infos)
    length, count = math.ceil(a["length"]), a["idx"]

    ss = downloadScreenshots(infos, count)
    cutbg(length)
    makevideo(count, length, infos, "AskReddit")