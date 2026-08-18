## 1. Persistence

- [x] 1.1 Añadir `CONSULTATION_LOG_PATH` y `CONSULTATION_SEQ_PATH` en config / `.env.example`; gitignore `data/`; lock de archivo para el contador
- [x] 1.2 Implementar assign de ID correlativo y append CSV (`id,closed_at,nombre,telefono,interes,origen,reason`) con datetime en `America/Argentina/Buenos_Aires`

## 2. Session hook and PING gate

- [x] 2.1 En el primer `ask()` de una sesión, asignar `consulta_id` y `origin`; devolver el id al caller
- [x] 2.2 En `end_session`: escribir CSV siempre; `send_admin_ping` solo si hay nombre o teléfono reales
- [x] 2.3 Actualizar `format_ping_email`: asunto y cuerpo con ID, nombre, teléfono, interés y origen

## 3. Channels

- [x] 3.1 `POST /chat`: aceptar origen (default `web`) y devolver `consulta_id` en `ChatResponse`
- [x] 3.2 UI: label muted `#N` en el chrome tras la primera respuesta; CLI: imprimir el id una vez; `main.py` origin `cli`

## 4. Verification and docs

- [x] 4.1 Tests: “Hola” cierra → CSV sí, PING no; con nombre o teléfono → CSV + PING; IDs correlativos; origen web/cli
- [x] 4.2 Runbook: path persistente del CSV en el CT y que el mail ya no sale sin contacto
