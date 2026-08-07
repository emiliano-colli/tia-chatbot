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

@app.post("/reset/{session_id}")
def reset(session_id: str):
    bot.reset_session(session_id)
    return {"status": "sesión reiniciada"}

@app.get("/health")
def health():
    return {"status": "ok"}
