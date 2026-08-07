from openai import OpenAI
from src.config import config
from src.prompts.loader import load_system_prompt
from src.knowledge.loader import load_knowledge
from src.tools import CHATBOT_TOOLS, run_tool
from src.utils.logger import get_logger

logger = get_logger(__name__)

MAX_TOOL_ITERATIONS = 3


class TiaChatbot:
    def __init__(self):
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
        self.system_prompt = load_system_prompt()
        self.knowledge = load_knowledge()
        self.sessions: dict[str, list] = {}

    def _build_context(self) -> str:
        return f"\n\n# BASE DE CONOCIMIENTO\n{self.knowledge}"

    def _get_history(self, session_id: str) -> list:
        if session_id not in self.sessions:
            self.sessions[session_id] = [
                {"role": "system", "content": self.system_prompt + self._build_context()}
            ]
        return self.sessions[session_id]

    def _append_tool_results(self, history: list, message) -> None:
        history.append(message.model_dump(exclude_none=True))
        for tool_call in message.tool_calls or []:
            result = run_tool(tool_call.function.name, tool_call.function.arguments)
            history.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result,
                }
            )

    def ask(self, session_id: str, user_message: str) -> str:
        history = self._get_history(session_id)
        history.append({"role": "user", "content": user_message})

        try:
            for _ in range(MAX_TOOL_ITERATIONS):
                response = self.client.chat.completions.create(
                    model=config.MODEL_NAME,
                    messages=history,
                    tools=CHATBOT_TOOLS,
                    temperature=config.TEMPERATURE,
                    max_tokens=config.MAX_TOKENS,
                )
                message = response.choices[0].message

                if message.tool_calls:
                    self._append_tool_results(history, message)
                    continue

                reply = message.content or ""
                history.append({"role": "assistant", "content": reply})
                return reply

            logger.error("Se alcanzó el tope de iteraciones de tools sin respuesta final")
            return "Perdón, tuve un problema técnico. ¿Podés repetir tu consulta?"

        except Exception as e:
            logger.error(f"Error al consultar el modelo: {e}")
            return "Perdón, tuve un problema técnico. ¿Podés repetir tu consulta?"

    def reset_session(self, session_id: str):
        self.sessions.pop(session_id, None)
