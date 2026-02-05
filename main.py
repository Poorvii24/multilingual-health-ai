from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api.chat import router as chat_router

# Create FastAPI app
app = FastAPI(
    title="Multilingual Health AI Backend",
    version="1.0.0"
)

# Include chat routes
app.include_router(chat_router)


# -------------------------------
# Health check route
# -------------------------------
@app.get("/health")
def health_check():
    return {"status": "ok"}


# -------------------------------
# Serve audio files (IMPORTANT)
# -------------------------------
app.mount(
    "/audio_responses",                 # URL path
    StaticFiles(directory="audio_responses"),  # Folder in project
    name="audio_responses"
)
