import math
from reddit.parser import getThreads
from tts.tts import SpeechEngine
from tts.voices import GTTS
import math
from reddit.screenshots import downloadScreenshots
from video.background import cutbg
from video.make import makevideo
from utils.cleaning import cleanup, clearTerminal
from uploaders.insta import InstagramUploader
from utils.accounts import loadDB, saveDB
from utils.menu import menu, logo, serviceSelector
import time
import random

def text2mp3(r_obj):
    to_mp3 = SpeechEngine(GTTS, r_obj)
    return to_mp3.run()

def main(sub, doneVids=[]):
    gt = getThreads(sub, doneVids)
    infos, doneVids = gt["infos"], gt["doneVideos"]
    print(f"[{i}] Thread grabbed: {infos['title']}")

    a = text2mp3(infos)
    length, count = math.ceil(a["length"]), a["idx"]
    downloadScreenshots(infos, count)
    cutbg(length)
    vidP = makevideo(count, length, infos, sub)
    cleanup()

    ig = InstagramUploader("idevfazt3stes", "Yoqu1201")
    ig.upload(vidP, ["askreddit", "quesiton", "reddit"])

    return doneVids

def r2c_ig(account, sub, i):

    doneVids = account["doneVids"]
    
    gt = getThreads(sub, doneVids)
    
    infos, doneVids = gt["infos"], gt["doneVideos"]

    print(f"[{i}] Thread grabbed: {infos['title']}")

    a = text2mp3(infos)
    length, count = math.ceil(a["length"]), a["idx"]
    downloadScreenshots(infos, count)
    print(f"[{i}] Screenshots downloaded")
    cutbg(length)
    print(f"[{i}] Background cut")
    vidP = makevideo(count, length, infos, sub)
    cleanup()
    print(f"[{i}] Uploading...")
    ig = InstagramUploader(account["username"], account["password"])
    ig.upload(vidP, account["tags"])
    print(f"[{i}] Uploaded\n")

    accs = loadDB()

    for acc in accs["instagram"]:
        if acc["username"] == account["username"] and acc["password"] == account["password"]:
            acc["doneVids"] = doneVids

    saveDB(accs)
    

if __name__ == "__main__":
    menu()

    clearTerminal()
    logo()

    service = serviceSelector()
    timer = int(input("Choose sleep time between posts (in minutes): ")) * 60

    accs = loadDB()

    i = 1

    while True:
        for acc in accs[service]:
            if acc["enabled"] == "True":
                sub = random.choice(acc["subs"])
                print(f'[{i}] in {acc["username"]} from {sub}')
                r2c_ig(acc, sub, i)

        print(f"Sleeping for {timer / 60} minutes")
        i += 1
        time.sleep(timer)