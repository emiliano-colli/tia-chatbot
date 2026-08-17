## Why

El staging en Proxmox ya expone FastAPI (`/chat`, `/health`), pero usuarios internos no pueden probar en paralelo sin `curl`. Gradio comparte un solo `session_id` y no sirve para testers simultáneos. Hace falta una página mínima sobre el mismo Uvicorn y centralizar el cierre por despedida en el backend para que CLI, web y API se comporten igual.

## What Changes

- Servir `GET /` con una UI estática (HTML/JS) que asigna un `session_id` por navegador vía `localStorage` y llama a `POST /chat`.
- Montar assets en `/static` (logo TRAMA local, no URL de CDN externa).
- Centralizar detección de despedida en `TiaChatbot.ask()`: si el mensaje es cierre, ejecutar `end_session`, devolver respuesta fija de despedida y no pasar el texto al LLM.
- Tras despedida, la UI borra el `session_id` local; opcional botón “Nueva consulta” vía `POST /end/{id}`.
- Historial en pantalla: solo burbujas en memoria JS (sin rehidratar al recargar).
- Sin autenticación en esta iteración.
- Ajustar runbook de staging (Nginx debe pasar `/` y `/static`).

## Capabilities

### New Capabilities
- `internal-chat-ui`: Página de chat interna, identidad de sesión en el browser, integración con la API existente.

### Modified Capabilities
- `conversation-flow`: Cierre por frases de despedida MUST ocurrir en `ask()` de forma consistente para todos los canales que usen `/chat` o el bot directamente.

## Impact

- `app/api.py` (static files, `GET /`)
- `app/static/` (nuevo: `index.html`, logo)
- `src/chatbot.py` (`ask()` + despedida centralizada)
- `main.py`, `gradio_app.py` (opcional: simplificar duplicación de `is_session_end_message`)
- `src/utils/session_end.py` (constante de mensaje de despedida si aplica)
- Tests: `ask` con despedida, GET `/`
- `docs/runbook-staging-proxmox-ct.md` (nota Nginx)
