## Context

TIA ya pide nombre y teléfono en el prompt y guarda historial en memoria, pero `reset_session` solo borra la sesión. No hay timeout ni aviso al admin. Se acordó un PING por email (Gmail SMTP, App Password en `.env`), destinatario admin distinto del remitente, disparado por cierre formal o inactividad configurable.

## Goals / Non-Goals

**Goals:**
- Un solo camino `end_session(session_id, reason)` que construye el payload PING y envía el mail.
- Cierre formal desde CLI/API (y Gradio si es viable con poco cambio).
- Timeout por inactividad usando `SESSION_TIMEOUT_MINUTES` y `last_activity` por sesión.
- Config SMTP + `ADMIN_EMAIL` + `MAIL_FROM` en `.env` / `Config`.
- Formato fijo de asunto/cuerpo PING.

**Non-Goals:**
- Sheet/Notion u otro registro persistente de visitantes.
- WhatsApp/Slack.
- Colas (Redis/SQS).
- Dashboard admin.
- Garantizar entrega 100% si Gmail rechaza (sí: loguear error y no tumbar el chat).

## Decisions

1. **Hook de sistema, no solo tool del LLM**  
   - `end_session` en código de aplicación.  
   - Rationale: el timeout no puede depender del modelo.  
   - Opcional: tool `end_session` / detección de despedida que llame al mismo hook (complemento, no único disparo).

2. **Gmail SMTP con stdlib `smtplib` + `email.message`**  
   - Rationale: sin dependencia nueva si alcanza.  
   - Alternativa: Resend/SendGrid — más limpio a escala, fuera de lo pedido.

3. **Remitente ≠ admin**  
   - `SMTP_USER` / `MAIL_FROM` envían; `ADMIN_EMAIL` recibe.

4. **Armado del payload**  
   - Contacto e intereses: extracción best-effort del historial (heurística o una llamada LLM corta de resumen al cerrar).  
   - Preferencia de diseño: primero intentar parseo/resumen estructurado al cierre; si no hay datos, asunto `Nueva consulta TIA — Sin identificar` y campos “No provisto”.  
   - Log: mensajes `user`/`assistant` de la sesión (sin system prompt completo ni tool dumps crudos si ensucian; incluir diálogo legible).

5. **Timeout**  
   - Actualizar `last_activity` en cada `ask()`.  
   - Barrido: en cada `ask()` (o timer en background del proceso) cerrar sesiones con `now - last_activity >= SESSION_TIMEOUT_MINUTES`.  
   - Para MVP single-process: chequeo al inicio de `ask()` + endpoint/periodo simple es suficiente.  
   - Default razonable en `.env.example` (p. ej. 30) si no se setea.

6. **Idempotencia**  
   - Una sesión solo notifica una vez; tras `end_session` se elimina el estado.

7. **Cierre formal**  
   - CLI: palabra `salir` (ya existe) pasa a llamar `end_session` antes de salir.  
   - API: `POST /end/{session_id}` (o evolucionar `/reset` a end+notify; preferir `/end` explícito y dejar `/reset` como clean sin mail solo si hace falta — por defecto unificar a end con notify).  
   - Decisión: `/reset` puede quedar como alias de end con notify, o documentar `/end` nuevo; preferir **`end_session` con notify** como comportamiento de cierre y exponer `/end/{session_id}`.

## Risks / Trade-offs

- [Gmail bloquea login / App Password mal configurada] → Mitigación: error en log; documentar setup en README; no romper `ask()`.
- [Resumen de contacto incorrecto] → Mitigación: “No provisto” + log completo para que el admin lea la fuente.
- [Timeout no corre si nadie habla] → Mitigación: documentar que en MVP el barrido ocurre al procesar tráfico; opcional thread/timer liviano si se necesita cierre sin tráfico.
- [PII en email] → Mitigación: solo a `ADMIN_EMAIL`; no loguear el cuerpo completo en stdout.
- [Sesión vacía / solo saludo] → Mitigación: igual se puede notificar o omitir si no hubo interacción útil; preferir notificar siempre al end formal/timeout con lo que haya (admin decide).

## Migration Plan

1. Variables nuevas en `.env.example` y `Config`.
2. Módulo mail + `end_session` + activity tracking.
3. Wire CLI/API.
4. Probar envío a admin real con App Password.
5. Rollback: revert; sin migración de datos.

## Open Questions

- Ninguna bloqueante. Detalle de implementación: resumen por LLM vs heurística — elegir la opción más simple que cumpla el formato PING en apply.
