from gtts import gTTS
import uuid


def speak(text):
    filename = f"speech_{uuid.uuid4().hex}.mp3"

    tts = gTTS(
        text=text,
        lang="en"
    )

    tts.save(filename)

    return filename