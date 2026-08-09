import threading
import time
from datetime import datetime, timezone

from openai import OpenAI
from src.config import config
from src.prompts.loader import load_system_prompt
from src.knowledge.loader import load_knowledge
from src.tools import CHATBOT_TOOLS, run_tool
from src.notifications import build_session_summary, send_admin_ping
from src.utils.logger import get_logger

logger = get_logger(__name__)

MAX_TOOL_ITERATIONS = 3
_IDLE_SWEEP_SECONDS = 60


class TiaChatbot:
    def __init__(self, start_idle_watcher: bool = True):
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
        self.system_prompt = load_system_prompt()
        self.knowledge = load_knowledge()
        self.sessions: dict[str, list] = {}
        self.last_activity: dict[str, datetime] = {}
        self._lock = threading.Lock()
        self._stop_watcher = threading.Event()
        self._watcher: threading.Thread | None = None
        if start_idle_watcher:
            self._start_idle_watcher()

    def _build_context(self) -> str:
        return f"\n\n# BASE DE CONOCIMIENTO\n{self.knowledge}"

    def _get_history(self, session_id: str) -> list:
        if session_id not in self.sessions:
            self.sessions[session_id] = [
                {"role": "system", "content": self.system_prompt + self._build_context()}
            ]
            self.last_activity[session_id] = datetime.now(timezone.utc)
        return self.sessions[session_id]

    def _touch(self, session_id: str) -> None:
        self.last_activity[session_id] = datetime.now(timezone.utc)

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

    def _start_idle_watcher(self) -> None:
        self._watcher = threading.Thread(
            target=self._idle_watcher_loop,
            name="tia-idle-watcher",
            daemon=True,
        )
        self._watcher.start()

    def _idle_watcher_loop(self) -> None:
        while not self._stop_watcher.wait(_IDLE_SWEEP_SECONDS):
            try:
                self.expire_idle_sessions()
            except Exception as exc:
                logger.error("Error en barrido de sesiones inactivas: %s", exc)

    def expire_idle_sessions(self) -> list[str]:
        """Cierra sesiones inactivas y notifica. Devuelve session_ids cerrados."""
        timeout = config.SESSION_TIMEOUT_MINUTES
        if timeout <= 0:
            return []

        now = datetime.now(timezone.utc)
        expired: list[str] = []
        with self._lock:
            candidates = list(self.last_activity.items())

        for session_id, last_seen in candidates:
            idle_minutes = (now - last_seen).total_seconds() / 60
            if idle_minutes >= timeout:
                if self.end_session(session_id, reason="timeout"):
                    expired.append(session_id)
        return expired

    def ask(self, session_id: str, user_message: str) -> str:
        self.expire_idle_sessions()

        with self._lock:
            history = self._get_history(session_id)
            history.append({"role": "user", "content": user_message})
            self._touch(session_id)

        try:
            for _ in range(MAX_TOOL_ITERATIONS):
                with self._lock:
                    messages = list(history)

                response = self.client.chat.completions.create(
                    model=config.MODEL_NAME,
                    messages=messages,
                    tools=CHATBOT_TOOLS,
                    temperature=config.TEMPERATURE,
                    max_tokens=config.MAX_TOKENS,
                )
                message = response.choices[0].message

                with self._lock:
                    if session_id not in self.sessions:
                        return "La sesión ya fue cerrada. Escribí de nuevo para empezar otra."
                    history = self.sessions[session_id]

                    if message.tool_calls:
                        self._append_tool_results(history, message)
                        self._touch(session_id)
                        continue

                    reply = message.content or ""
                    history.append({"role": "assistant", "content": reply})
                    self._touch(session_id)
                    return reply

            logger.error("Se alcanzó el tope de iteraciones de tools sin respuesta final")
            return "Perdón, tuve un problema técnico. ¿Podés repetir tu consulta?"

        except Exception as e:
            logger.error(f"Error al consultar el modelo: {e}")
            return "Perdón, tuve un problema técnico. ¿Podés repetir tu consulta?"

    def end_session(self, session_id: str, reason: str = "formal") -> bool:
        """Notifica PING una vez y limpia la sesión. True si había sesión."""
        with self._lock:
            history = self.sessions.pop(session_id, None)
            self.last_activity.pop(session_id, None)

        if history is None:
            return False

        summary = build_session_summary(history, client=self.client)
        send_admin_ping(summary)
        logger.info("Sesión %s finalizada (%s)", session_id, reason)
        return True

    def reset_session(self, session_id: str):
        """Alias de cierre con notificación (compatibilidad API)."""
        self.end_session(session_id, reason="reset")
