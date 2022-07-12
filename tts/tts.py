import translators as ts
from moviepy.editor import AudioFileClip, CompositeAudioClip, concatenate_audioclips

import re

from pathlib import Path

MAX_CHARS = 300

class SpeechEngine:
    def __init__(self, module, r_obj, path="temp/mp3"):
        self.module = module
        self.redditObject = r_obj
        self.path = path
        self.lenght = 0
        self.maxlenght = 50 # seconds

    def run(self):

        Path(self.path).mkdir(parents=True, exist_ok=True)

        # This file needs to be removed in case this post does not use post text, so that it won't appear in the final video
        try:
            Path(f"{self.path}/posttext.mp3").unlink()
        except OSError:
            pass

        print("Saving text to MP3... ")

        self.call("title", self.redditObject["title"])
        if self.redditObject["text"] != "":
            self.call("content", self.redditObject["text"])

        replyID = None
        for replyID, reply in enumerate(self.redditObject["replies"]):
            if self.length < self.maxlenght:
                if not len(reply["body"]) > MAX_CHARS:
                    self.call(replyID, reply["body"])
                else:
                    self.spit(replyID, reply["body"])
            else:
                break

        return {"length": self.length, "idx": replyID}


    def call(self, fName, text):
        self.module.run(text=parseText(text), filepath=f"{self.path}/{fName}.mp3")

        try:
            clip = AudioFileClip(f"{self.path}/{fName}.mp3")
            self.length += clip.duration
            clip.close()
        except:
            self.length = 0

    def split(self, id, text):
        splitFiles = []
        splitText = [x.group().strip() for x in re.finditer(r" *(((.|\n){0," + str(MAX_CHARS) + "})(\.|.$))", text)]

        off = 0
        for idy, cut in enumerate(splitText):
            if not cut or cut.isspace():
                off += 1
                continue

            self.call(f"{id}-{idy - off}.part", cut)
            splitFiles.append(AudioFileClip(f"{self.path}/{id}-{idy - off}.part.mp3"))

        CompositeAudioClip([concatenate_audioclips(splitFiles)]).write_audiofile(f"{self.path}/{id}.mp3", fps=44100, verbose=False, logger=None)

        for i in splitFiles:
            name = i.filename
            i.close()
            Path(name).unlink()

        
def parseText(text):
    urls_ex = r"((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*"
    nourls = re.sub(urls_ex, " ", text)

    apost_ex = r"\s['|’]|['|’]\s|[\^_~@!&;#:\-%“”‘\"%\*/{}\[\]\(\)\\|<>=+]"
    apost = re.sub(apost_ex, " ", nourls)

    clean = apost.replace("shit", "crap").replace("fuck", "f word") # to do

    clean.replace("+", "plus").replace("-", "minus").replace("&", "and")

    return " ".join(clean.split())

