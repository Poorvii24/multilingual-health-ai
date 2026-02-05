import uuid
import os
from gtts import gTTS

OUTPUT_DIR = "audio_responses"

def text_to_speech(text: str, language: str):

    # Ensure folder exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    filename = f"{uuid.uuid4()}.mp3"
    filepath = os.path.join(OUTPUT_DIR, filename)

    tts = gTTS(text=text, lang=language)
    tts.save(filepath)

    # 🌐 Return browser-playable URL
    return f"http://127.0.0.1:8000/audio_responses/{filename}"
