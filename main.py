from reddit.parser import getThreads
from tts.tts import SpeechEngine
from tts.voices import GTTS

def text2mp3(r_obj):
    to_mp3 = SpeechEngine(GTTS, r_obj)

if __name__ == "__main__":
    infos = getThreads("AskReddit")