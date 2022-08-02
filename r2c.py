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
from utils.accounts import loadDB, saveDB

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

def r2c_ig(account, sub):

    doneVids = account["doneVids"]
    
    gt = getThreads(sub, doneVids)
    infos, doneVids = gt["infos"], gt["doneVideos"]
    a = text2mp3(infos)
    length, count = math.ceil(a["length"]), a["idx"]
    downloadScreenshots(infos, count)
    cutbg(length)
    vidP = makevideo(count, length, infos, sub)
    cleanup()
    ig = InstagramUploader(account["username"], account["password"])
    ig.upload(vidP, account["tags"])

    accs = loadDB()

    for acc in accs["instagram"]:
        if acc["username"] == account["username"] and acc["password"] == account["password"]:
            acc["doneVids"] = doneVids

    saveDB(accs)
    

if __name__ == "__main__":
    sub = input("sub: ")
    doneVids = []
    pp = loadDB()

    for coninha in pp["instagram"]:
        while True:
            r2c_ig(coninha, sub)