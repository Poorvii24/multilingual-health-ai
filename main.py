from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from api.chat import router as chat_router

# -----------------------------------
# Create FastAPI app
# -----------------------------------
app = FastAPI(
    title="Multilingual Health AI Backend",
    version="1.0.0"
)

# -----------------------------------
# CORS Middleware (Frontend Fix)
# -----------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Allow all origins (for dev)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------------
# Include API Routers
# -----------------------------------
app.include_router(chat_router)

# -----------------------------------
# Health Check Route
# -----------------------------------
@app.get("/health")
def health_check():
    return {"status": "ok"}

# -----------------------------------
# Serve Audio Files (IMPORTANT)
# -----------------------------------
app.mount(
    "/audio_responses",                     # URL path
    StaticFiles(directory="audio_responses"),  # Folder path
    name="audio_responses"
)
