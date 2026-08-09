## Why

Tras cada conversación con TIA, TRAMA necesita enterarse del contacto, sus intereses y el log de la charla. Hoy al cerrar o abandonar una sesión no se notifica a nadie. Un email “PING” al admin al fin de sesión (cierre formal o timeout) cubre ese hueco sin montar aún un registro en planilla.

## What Changes

- Agregar cierre de sesión unificado (`end_session`) que arma y envía un email al admin con contacto, intereses y log completo.
- Disparar ese cierre por: (1) cierre formal del usuario y (2) inactividad tras `SESSION_TIMEOUT_MINUTES` configurable en `.env`.
- Enviar el mail vía Gmail SMTP (App Password), con remitente y destinatario admin **distintos**, credenciales solo en `.env`.
- Formato PING fijo: asunto `Nueva consulta TIA — {nombre}`; cuerpo con Contacto, Intereses y Log.
- Extender `.env.example` / config con variables SMTP, `ADMIN_EMAIL`, `MAIL_FROM` y timeout.
- Exponer cierre formal en los entrypoints relevantes (CLI / API como mínimo) y actualizar prompt si hace falta para el cierre conversacional.

## Capabilities

### New Capabilities
- `admin-email-notification`: Notificación por email al admin al finalizar una sesión (formal o por timeout), con payload PING.

### Modified Capabilities
- (ninguna)

## Impact

- Código: `src/config.py`, nuevo módulo de mail/sesión (p. ej. `src/notifications/` o similar), `src/chatbot.py` (actividad + `end_session`), `main.py`, `app/api.py`, posiblemente Gradio
- Config: `.env` / `.env.example`
- Dependencias: preferir stdlib `smtplib`; solo agregar lib si hace falta justificar
- Sin Sheet/Notion en este change
