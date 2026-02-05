import whisper
import tempfile
import os

model = whisper.load_model("tiny")

def speech_to_text(audio_bytes: bytes):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio.write(audio_bytes)
        temp_path = temp_audio.name

    try:
        # Detect language FIRST
        audio = whisper.load_audio(temp_path)
        audio = whisper.pad_or_trim(audio)

        mel = whisper.log_mel_spectrogram(audio).to(model.device)
        _, probs = model.detect_language(mel)
        detected_lang = max(probs, key=probs.get)

        # Then transcribe
        result = model.transcribe(temp_path)

        return result["text"], detected_lang

    finally:
        os.remove(temp_path)
