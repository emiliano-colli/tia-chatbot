import gradio as gr
from src.chatbot import TiaChatbot
from src.utils.session_end import is_session_end_message

bot = TiaChatbot()


def chat_fn(message, history):
    if is_session_end_message(message):
        bot.end_session("gradio", reason="formal")
        return "¡Hasta pronto! 🌿 Escribí de nuevo cuando quieras retomar."
    return bot.ask("gradio", message)


demo = gr.ChatInterface(
    fn=chat_fn,
    title="Chatbot TRAMA",
    description="Preguntame sobre talleres, servicios y más 🌿",
)


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
