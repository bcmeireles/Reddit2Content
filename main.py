from reddit.parser import getThreads
from tts.tts import SpeechEngine
from tts.voices import GTTS

def text2mp3(r_obj):
    to_mp3 = SpeechEngine(GTTS, r_obj)
    return to_mp3.run()

if __name__ == "__main__":
    infos = getThreads("AskReddit")
    #leng, no = text2mp3(infos)
    #print(leng, no)
    a = text2mp3(infos)
    print(a)