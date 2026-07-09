from src.chatbot import TeaChatbot

def main():
    tea = TeaChatbot()
    session_id = "default"
    print("Téa 🌿 (escribí 'salir' para terminar)\n")
    while True:
        user_input = input("Vos: ")
        if user_input.lower() in ("salir", "exit", "quit"):
            print("Téa: ¡Hasta pronto! 🌿")
            break
        respuesta = tea.ask(session_id, user_input)
        print(f"Téa: {respuesta}\n")

if __name__ == "__main__":
    main()

"""
import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.api:app", host="0.0.0.0", port=8000, reload=True)
"""