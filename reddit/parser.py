from os import getenv
import json

import random

import praw
from praw.models import MoreComments

def checkThreads(allThreads, sub, doneVideos):
    """
    Receives possible video submissions and the subreddit they belong to, returns
    a thread that has not been converted into a video yet
    """

    #with open("./content/data/vids.json", "r", encoding="utf-8") as f:
    #    done = json.load(f)

    toShuffle = []

    for thread in allThreads:
        if not thread.stickied:
            if not str(thread) in doneVideos:
                if not thread.over_18:
                    toShuffle.append(thread)
                    
    if len(toShuffle) > 0:
        return {"thread": random.choice(toShuffle), "doneVideos": doneVideos}

    return checkThreads(sub.top(time_filter="hour"), sub, doneVideos)

def doubleCheck(thread, doneVideos):
    if not str(thread) in doneVideos:
        doneVideos.append(str(thread))
        return {"status": True, "doneVideos": doneVideos}

def getInfo(thread):
    info = {}
    info["link"] = thread.permalink
    info["title"] = thread.title
    info["text"] = thread.selftext
    info["id"] = thread.id
    info["replies"] = []

    for reply in thread.comments:
        if not isinstance(reply, MoreComments):
            if not reply == "[removed]":
                if not reply == "[deleted]":
                    if not reply.stickied:
                        if len(reply.body) < 500:
                            info["replies"].append({
                                "body": reply.body,
                                "link": reply.permalink,
                                "id": reply.id
                            })

    return info

def getThreads(subreddit, doneVids=[]):

    reddit = praw.Reddit(
        client_id=getenv("REDDIT_CLIENT_ID"),
        client_secret=getenv("REDDIT_CLIENT_SECRET"),
        user_agent="r2c",
        username=getenv("REDDIT_USER"),
        passkey=getenv("REDDIT_PASSWORD"),
        check_for_async=False,
    )

    sub = reddit.subreddit(subreddit)

    hotThreads = sub.hot(limit=20)
    possib = checkThreads(hotThreads, sub, doneVids)
    doneVids = possib["doneVideos"]
    thread = possib["thread"]
    if doubleCheck(thread, doneVids)["status"]:
        infos = getInfo(thread)
    else:
        getThreads(subreddit, doneVids)

    return {"infos": infos, "doneVideos": doneVids}