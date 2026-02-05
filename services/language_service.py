from langdetect import detect, LangDetectException
import re

def is_likely_english(text: str) -> bool:
    # If text contains only basic ASCII letters and spaces
    return bool(re.fullmatch(r"[A-Za-z0-9\s.,!?']+", text))

def detect_language(text: str) -> str:
    cleaned = text.strip()

    # Very short text → default English
    if len(cleaned) < 5:
        return "en"

    # Likely English text → force English
    if is_likely_english(cleaned):
        return "en"

    try:
        return detect(cleaned)
    except LangDetectException:
        return "en"
