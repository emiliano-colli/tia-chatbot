from src.chatbot import TiaChatbot

def main():
    tia = TiaChatbot()
    session_id = "default"
    print("TIA 🌿 (escribí 'salir' para terminar)\n")
    while True:
        user_input = input("Vos: ")
        if user_input.lower() in ("salir", "exit", "quit"):
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
