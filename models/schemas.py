from pydantic import BaseModel
from typing import Optional
from pydantic import BaseModel
from typing import Optional

class TextRequest(BaseModel):
    message: str
    language: Optional[str] = None

class TextResponse(BaseModel):
    reply_text: str
    detected_language: str
    confidence: float

class TextResponse(BaseModel):
    reply_text: str
    detected_language: str
    confidence: float
    audio_url: Optional[str] = None
