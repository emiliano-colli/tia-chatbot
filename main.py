from src.chatbot import TiaChatbot
from src.utils.session_end import is_session_end_message

def main():
    tia = TiaChatbot()
    session_id = "default"
    shown_id = None
    print("TIA 🌿 (escribí 'salir', 'chau', 'fin'… para terminar)\n")
    while True:
        user_input = input("Vos: ")
        result = tia.ask(session_id, user_input, origin="cli")
        if result.consulta_id is not None and result.consulta_id != shown_id:
            print(f"  · consulta #{result.consulta_id}")
            shown_id = result.consulta_id
        print(f"TIA: {result.reply}\n")
        if is_session_end_message(user_input):
            break

if __name__ == "__main__":
    main()

"""
import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.api:app", host="0.0.0.0", port=8000, reload=True)
"""
