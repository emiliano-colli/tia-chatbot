## Context

Staging CT corre Uvicorn en `:8000` con FastAPI. Varios testers necesitan charlas paralelas (`session_id` distintos). Gradio descartado. Explore definió: `localStorage`, sin auth, logo local, historial mínimo en UI, cierre centralizado en backend.

Hoy `is_session_end_message` solo usa CLI/Gradio antes de `ask()`; `/chat` manda “chau” al LLM sin cerrar sesión ni PING.

## Goals / Non-Goals

**Goals:**
- Una página en `GET /` usable desde el browser (mismo origen que `/chat`).
- UUID en `localStorage`; recarga conserva id (server recuerda); UI vacía al F5.
- Despedida única vía `ask()` → `end_session` + texto fijo.
- Logo servido desde `/static/logo-trama.jpg` (asset en repo, no hotlink Instagram).

**Non-Goals:**
- Auth (Nginx htpasswd queda para después).
- Query params de origen Meta (`?interes=`).
- Rehidratar historial visual desde el server.
- Reemplazar Gradio en el CT (puede quedar sin usar).
- WebSockets, SPA framework, persistencia de sesiones en disco.

## Decisions

1. **Static + FileResponse en FastAPI**  
   - `app/static/index.html`, `StaticFiles` en `/static`.  
   - Rationale: cero build, un proceso, mismo despliegue en CT.  
   - Alternativa React: rechazada para MVP.

2. **Session id en `localStorage` key `tia_session_id`**  
   - Generar con `crypto.randomUUID()` si falta.  
   - Borrar key tras despedida exitosa o botón “Nueva consulta”.  
   - Alternativa cookie: no necesaria sin auth server-side.

3. **Cierre en `TiaChatbot.ask()`**  
   - Si `is_session_end_message(user_message)`: `end_session(session_id, reason="formal")`, return `SESSION_END_REPLY` constante.  
   - Rationale: una sola verdad para web, API y futuros clientes.  
   - CLI/Gradio pueden delegar a `ask()` (Gradio aún necesita id por visitante aparte).

4. **Historial UI**  
   - Array en JS; append por turno; no `localStorage` de mensajes.  
   - Recarga: pantalla vacía, id conservado → modelo sigue con contexto server-side.

5. **Logo**  
   - Descargar/commit `app/static/logo-trama.jpg` desde referencia TRAMA (no CDN en runtime).  
   - HTML: img + título “TIA · TRAMA”, hint de despedida como CLI.

6. **Despedida UX**  
   - Tras respuesta de cierre, UI limpia chat y borra `tia_session_id`; mensaje “Escribí de nuevo para empezar otra consulta”.  
   - Botón “Nueva consulta”: `POST /end/{id}` + clear id + clear UI (por si no dijeron chau).

## Risks / Trade-offs

- [Sin auth] → Mitigación: staging interno; runbook advierte.  
- [Logo copyright] → Asset oficial TRAMA; no hotlink.  
- [F5 pantalla vacía pero server recuerda] → Aceptado; hint en UI si hace falta.  
- [Doble end_session] → `end_session` ya es idempotente tras limpiar sesión.

## Migration Plan

1. Implementar `ask()` + static UI.  
2. Tests.  
3. `git pull` en CT, restart `tia.service`.  
4. Verificar Nginx pasa `/` y `/static` (no solo `/health`).

## Open Questions

- Ninguno bloqueante; auth y origen Meta quedan fuera de scope.
