from instagrapi import Client

class InstagramUploader():
    def __init__(self, username, password):
        self.cl = Client()
        self.cl.login(username, password)

    def upload(self, path, tags=None):
        self.cl.clip_upload(path, path.split("/")[-1].removesuffix(".mp4") + "# ".join(tag for tag in tags))