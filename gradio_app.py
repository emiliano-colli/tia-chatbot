import gradio as gr
from src.chatbot import TiaChatbot

bot = TiaChatbot()


def chat_fn(message, history):
    return bot.ask("gradio", message, origin="gradio").reply


demo = gr.ChatInterface(
    fn=chat_fn,
    title="Chatbot TRAMA",
    description="Preguntame sobre talleres, servicios y más 🌿",
)


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
