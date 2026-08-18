import threading
import time
from dataclasses import dataclass
from datetime import datetime, timezone

from openai import OpenAI
from src.config import config
from src.prompts.loader import load_system_prompt
from src.knowledge.loader import load_knowledge
from src.tools import CHATBOT_TOOLS, run_tool
from src.notifications import build_session_summary, has_contact, send_admin_ping
from src.notifications.consultation_log import append_consultation_row, next_consulta_id
from src.utils.logger import get_logger
from src.utils.session_end import SESSION_END_REPLY, is_session_end_message

logger = get_logger(__name__)

MAX_TOOL_ITERATIONS = 3
_IDLE_SWEEP_SECONDS = 60


@dataclass
class AskResult:
    reply: str
    consulta_id: int | None = None


class TiaChatbot:
    def __init__(self, start_idle_watcher: bool = True):
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
        self.system_prompt = load_system_prompt()
        self.knowledge = load_knowledge()
        self.sessions: dict[str, list] = {}
        self.last_activity: dict[str, datetime] = {}
        self.consulta_ids: dict[str, int] = {}
        self.origins: dict[str, str] = {}
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

    def _ensure_consulta(self, session_id: str, origin: str) -> int:
        if session_id not in self.consulta_ids:
            self.consulta_ids[session_id] = next_consulta_id()
            self.origins[session_id] = origin or "web"
        elif origin and not self.origins.get(session_id):
            self.origins[session_id] = origin
        return self.consulta_ids[session_id]

    def ask(self, session_id: str, user_message: str, origin: str = "web") -> AskResult:
        self.expire_idle_sessions()

        if is_session_end_message(user_message):
            consulta_id = self.consulta_ids.get(session_id)
            if session_id in self.sessions:
                self.end_session(session_id, reason="formal")
            return AskResult(SESSION_END_REPLY, consulta_id)

        with self._lock:
            history = self._get_history(session_id)
            history.append({"role": "user", "content": user_message})
            self._touch(session_id)
            consulta_id = self._ensure_consulta(session_id, origin)

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
                        return AskResult(
                            "La sesión ya fue cerrada. Escribí de nuevo para empezar otra.",
                            consulta_id,
                        )
                    history = self.sessions[session_id]

                    if message.tool_calls:
                        self._append_tool_results(history, message)
                        self._touch(session_id)
                        continue

                    reply = message.content or ""
                    history.append({"role": "assistant", "content": reply})
                    self._touch(session_id)
                    return AskResult(reply, consulta_id)

            logger.error("Se alcanzó el tope de iteraciones de tools sin respuesta final")
            return AskResult(
                "Perdón, tuve un problema técnico. ¿Podés repetir tu consulta?",
                consulta_id,
            )

        except Exception as e:
            logger.error(f"Error al consultar el modelo: {e}")
            return AskResult(
                "Perdón, tuve un problema técnico. ¿Podés repetir tu consulta?",
                consulta_id,
            )

    def end_session(self, session_id: str, reason: str = "formal") -> bool:
        """Registra CSV, notifica PING si hay contacto, y limpia la sesión."""
        with self._lock:
            history = self.sessions.pop(session_id, None)
            self.last_activity.pop(session_id, None)
            consulta_id = self.consulta_ids.pop(session_id, None)
            origin = self.origins.pop(session_id, "")

        if history is None:
            return False

        if consulta_id is None:
            consulta_id = next_consulta_id()
        if not origin:
            origin = "web"

        summary = build_session_summary(history, client=self.client)
        summary.consulta_id = consulta_id
        summary.origin = origin
        append_consultation_row(
            consulta_id=consulta_id,
            nombre=summary.name,
            telefono=summary.phone,
            interes=summary.interests,
            origen=origin,
            reason=reason,
        )
        if has_contact(summary):
            send_admin_ping(summary)
        else:
            logger.info(
                "Sesión %s finalizada (%s) sin contacto; PING omitido",
                session_id,
                reason,
            )
        logger.info("Sesión %s finalizada (%s) consulta=#%s", session_id, reason, consulta_id)
        return True

    def reset_session(self, session_id: str):
        """Alias de cierre con notificación (compatibilidad API)."""
        self.end_session(session_id, reason="reset")
