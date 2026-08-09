from src.chatbot import TiaChatbot
from src.utils.session_end import is_session_end_message

def main():
    tia = TiaChatbot()
    session_id = "default"
    print("TIA 🌿 (escribí 'salir', 'chau', 'fin'… para terminar)\n")
    while True:
        user_input = input("Vos: ")
        if is_session_end_message(user_input):
            tia.end_session(session_id, reason="formal")
            print("TIA: ¡Hasta pronto! 🌿")
            break
        respuesta = tia.ask(session_id, user_input)
        print(f"TIA: {respuesta}\n")

if __name__ == "__main__":
    main()

"""
import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.api:app", host="0.0.0.0", port=8000, reload=True)
"""
