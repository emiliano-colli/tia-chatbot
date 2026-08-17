## 1. Centralized session end in ask()

- [x] 1.1 Añadir constante de respuesta de despedida (p. ej. en `session_end.py`) y detectar farewell al inicio de `TiaChatbot.ask()`: `end_session` + return sin LLM
- [x] 1.2 Ajustar CLI/Gradio para delegar despedida a `ask()` donde sea posible (evitar doble cierre); mantener loop CLI si hace falta

## 2. Static chat UI

- [x] 2.1 Crear `app/static/index.html` + CSS mínimo: logo local, área de mensajes, input, hint de despedida, botón “Nueva consulta”
- [x] 2.2 JS: `localStorage` `tia_session_id`, `POST /chat`, append burbujas en memoria, clear id/UI tras despedida y en nueva consulta (`POST /end/{id}`)
- [x] 2.3 Añadir `app/static/logo-trama.jpg` (asset local; no hotlink CDN)
- [x] 2.4 Montar static en FastAPI: `GET /`, `/static`

## 3. Verification and docs

- [x] 3.1 Tests: farewell vía `ask`/`/chat`; GET `/` devuelve HTML; `is_session_end_message` sin regresión
- [x] 3.2 Actualizar `docs/runbook-staging-proxmox-ct.md`: Nginx debe proxy `/` y `/static`; probar dos browsers en paralelo
