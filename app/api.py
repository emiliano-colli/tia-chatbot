from fastapi import FastAPI
from pydantic import BaseModel
from src.chatbot import TiaChatbot

app = FastAPI(title="TIA Chatbot API")
bot = TiaChatbot()

class ChatRequest(BaseModel):
    session_id: str
    message: str

class ChatResponse(BaseModel):
    reply: str

@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    reply = bot.ask(request.session_id, request.message)
    return ChatResponse(reply=reply)

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
