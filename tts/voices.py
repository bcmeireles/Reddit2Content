from gtts import gTTS

class GTTS:
    def __init__(self):
        self.max_chars = 0
        self.voices = []

    def run(text, filepath):
        tts = gTTS(text=text, lang="en", slow=False)

        tts.save(filepath)