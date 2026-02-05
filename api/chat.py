from fastapi import APIRouter, UploadFile, File
from services.emergency_service import is_emergency
from services.speech_service import speech_to_text
from services.tts_service import text_to_speech
from models.schemas import TextRequest, TextResponse
from services.nlp_service import process_health_query
from services.language_service import detect_language
from services.translation_service import (
    translate_to_english,
    translate_from_english
)

router = APIRouter()

# -------------------------------
# TEXT CHAT ENDPOINT
# -------------------------------
@router.post("/chat/text", response_model=TextResponse)
def chat_text(request: TextRequest):

    # 1️⃣ Detect language
    detected_language = (
        request.language
        if request.language
        else detect_language(request.message)
    )

    # 2️⃣ Translate input → English
    english_text = translate_to_english(
        request.message,
        detected_language
    )

    # 3️⃣ 🚨 Emergency check
    if is_emergency(english_text):
        emergency_reply_en = (
            "This may be a medical emergency. "
            "Please seek immediate medical help or contact local emergency services."
        )

        final_reply = translate_from_english(
            emergency_reply_en,
            detected_language
        )

        # 🔊 Generate audio
        audio_path = text_to_speech(
            final_reply,
            detected_language
        )

        return TextResponse(
            reply_text=final_reply,
            detected_language=detected_language,
            confidence=1.0,
            audio_url=audio_path
        )

    # 4️⃣ Normal NLP logic
    reply_en, confidence = process_health_query(english_text)

    # 5️⃣ Translate response back
    final_reply = translate_from_english(
        reply_en,
        detected_language
    )

    # 🔊 Generate audio
    audio_path = text_to_speech(
        final_reply,
        detected_language
    )

    return TextResponse(
        reply_text=final_reply,
        detected_language=detected_language,
        confidence=confidence,
        audio_url=audio_path
    )


# -------------------------------
# AUDIO CHAT ENDPOINT
# -------------------------------
@router.post("/chat/audio", response_model=TextResponse)
def chat_audio(file: UploadFile = File(...)):

    # 1️⃣ Read audio
    audio_bytes = file.file.read()
    file.file.close()

    # 2️⃣ Speech → text + language (Whisper)
    text, whisper_lang = speech_to_text(audio_bytes)
    text = text.strip()

    # Prefer Whisper language for voice
    detected_language = whisper_lang

    # Safety fallback if Whisper fails
    if detected_language == "en" and len(text) > 20:
        detected_language = detect_language(text)

    # 3️⃣ Translate → English
    english_text = translate_to_english(
        text,
        detected_language
    )

    # 4️⃣ 🚨 Emergency check
    if is_emergency(english_text):
        emergency_reply_en = (
            "This may be a medical emergency. "
            "Please seek immediate medical help or contact local emergency services."
        )

        final_reply = translate_from_english(
            emergency_reply_en,
            detected_language
        )

        # 🔊 Generate audio
        audio_path = text_to_speech(
            final_reply,
            detected_language
        )

        return TextResponse(
            reply_text=final_reply,
            detected_language=detected_language,
            confidence=1.0,
            audio_url=audio_path
        )

    # 5️⃣ NLP logic
    reply_en, confidence = process_health_query(english_text)

    # 6️⃣ Translate back
    final_reply = translate_from_english(
        reply_en,
        detected_language
    )

    # 🔊 Generate audio
    audio_path = text_to_speech(
        final_reply,
        detected_language
    )

    return TextResponse(
        reply_text=final_reply,
        detected_language=detected_language,
        confidence=confidence,
        audio_url=audio_path
    )



