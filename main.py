from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from api.chat import router as chat_router

app = FastAPI(title="Multilingual Health AI Backend")

app.include_router(chat_router)

# Serve audio folder
app.mount(
    "/audio_responses",
    StaticFiles(directory="audio_responses"),
    name="audio_responses"
)
