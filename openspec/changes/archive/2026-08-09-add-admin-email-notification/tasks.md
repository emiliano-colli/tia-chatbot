## 1. Config and mail transport

- [x] 1.1 Extender `src/config.py` y `.env.example` con `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`, `MAIL_FROM`, `ADMIN_EMAIL`, `SESSION_TIMEOUT_MINUTES`
- [x] 1.2 Implementar envío SMTP Gmail (stdlib) y builder del email PING (asunto + Contacto / Intereses / Log)

## 2. Session end lifecycle

- [x] 2.1 Agregar tracking de `last_activity` y `end_session(session_id, reason)` en el chatbot (armar payload, notificar una vez, limpiar sesión)
- [x] 2.2 Disparar cierre por timeout según `SESSION_TIMEOUT_MINUTES` (barrido al procesar actividad y/o mecanismo liviano en proceso)
- [x] 2.3 Cablear cierre formal: CLI `salir` y endpoint API de fin de sesión; alinear `/reset` o documentar el nuevo contrato

## 3. Prompt, docs and verification

- [x] 3.1 Ajustar prompt/docs mínimos si hace falta para el cierre de conversación y variables de entorno
- [x] 3.2 Tests unitarios del formateo PING / end_session (mail mockeado) y verificación manual de config si hay credenciales
