# TIA Chatbot

Asistente virtual de TRAMA y Comunidad Maternar.

## Instalación

1. Crear entorno virtual: `python -m venv venv`
2. Activar: `venv\Scripts\activate` (Windows) o `source venv/bin/activate` (Mac/Linux)
3. Instalar dependencias: `pip install -r requirements.txt`
4. Copiá `.env.example` a `.env` y completá:
   - `OPENAI_API_KEY`
   - SMTP Gmail (`SMTP_USER`, `SMTP_PASSWORD` = App Password, `MAIL_FROM`)
   - `ADMIN_EMAIL` (cuenta distinta que recibe el PING)
   - `SESSION_TIMEOUT_MINUTES` (inactividad antes de cerrar y notificar)

## Ejecutar

- CLI: `python main.py` (escribí `salir` para cerrar y notificar)
- API: `uvicorn app.api:app --reload` — `POST /chat`, `POST /end/{session_id}` (y `/reset` como alias)
- Gradio: `python gradio_app.py` (`salir` cierra la sesión Gradio)

## Notificación al admin

Al cerrar por `salir`/`/end` o por timeout, se envía un email PING con contacto, intereses y log de la charla.
