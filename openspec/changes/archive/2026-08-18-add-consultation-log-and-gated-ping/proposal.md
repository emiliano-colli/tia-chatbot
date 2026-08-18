## Why

Hoy cada cierre de sesión manda un PING, incluso si el usuario solo escribió “Hola”: el correo no sirve y no hay un registro para contar consultas. Hace falta un ID correlativo, un CSV interno de todas las conversaciones, y mandar mail solo cuando hay al menos un dato de contacto.

## What Changes

- Asignar un **ID entero único y correlativo** a cada consulta (al primer mensaje), independiente del UUID de sesión.
- Append de una fila **CSV** al cerrar (formal, timeout o reset): ID, fecha/hora, nombre, teléfono, interés, origen (`web` / `cli`; redes más adelante).
- **Todas** las consultas van al CSV. El PING **solo** si hay nombre o teléfono reales (`No provisto` no cuenta). El interés solo no dispara mail.
- El ID va en **asunto y cuerpo** del mail, junto con nombre / celular / interés detectado.
- Mostrar el ID de forma **discreta** en la UI web y una vez en CLI.
- **BREAKING** (menor): `POST /chat` incluye `consulta_id` en la respuesta; el PING deja de enviarse en cierres sin contacto (el spec actual exigía mail siempre).

## Capabilities

### New Capabilities

- `consultation-log`: ID correlativo, CSV de cierre, origen del canal, exposición discreta del ID al usuario.

### Modified Capabilities

- `admin-email-notification`: PING condicionado a contacto; asunto y cuerpo incluyen ID, nombre, teléfono e interés.
- `internal-chat-ui`: la página muestra el ID de consulta de forma poco prominente una vez asignado.

## Impact

- `src/chatbot.py` (`ask` / `end_session`: ID, origen, log, gate del PING)
- `src/notifications/` (CSV, subject/body, `has_contact`)
- `src/config.py`, `.env.example` (`CONSULTATION_LOG_PATH`)
- `app/api.py` (`origin`, `consulta_id` en `/chat`)
- `app/static/index.html` (ID chico en el chrome)
- `main.py` (origen `cli`, mostrar ID)
- `docs/runbook-staging-proxmox-ct.md` (path del CSV, volumen si el CT se recrea)
- Tests de cierre, PING gated, CSV e ID en `GET /` no aplica: sí en `/chat` y UI
- `.gitignore` del CSV local si vive en el repo working tree
