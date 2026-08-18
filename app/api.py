from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from src.chatbot import TiaChatbot

STATIC_DIR = Path(__file__).resolve().parent / "static"

app = FastAPI(title="TIA Chatbot API")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
bot = TiaChatbot()

class ChatRequest(BaseModel):
    session_id: str
    message: str
    origin: str = "web"


class ChatResponse(BaseModel):
    reply: str
    consulta_id: int | None = None

@app.get("/")
def index():
    return FileResponse(STATIC_DIR / "index.html")

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    result = bot.ask(request.session_id, request.message, origin=request.origin or "web")
    return ChatResponse(reply=result.reply, consulta_id=result.consulta_id)

@app.post("/end/{session_id}")
def end_session(session_id: str):
    closed = bot.end_session(session_id, reason="formal")
    if not closed:
        return {"status": "sin sesión activa"}
    return {"status": "sesión finalizada y admin notificado"}

@app.post("/reset/{session_id}")
def reset(session_id: str):
    """Alias de /end: cierra y envía PING al admin."""
    closed = bot.end_session(session_id, reason="reset")
    if not closed:
        return {"status": "sin sesión activa"}
    return {"status": "sesión finalizada y admin notificado"}

@app.get("/health")
def health():
    return {"status": "ok"}
