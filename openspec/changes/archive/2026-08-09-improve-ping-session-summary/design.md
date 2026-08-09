## Context

El PING usa `build_session_summary` con regex/keywords. Falló en producción controlada: `Emiliano 1167462412` no matcheó nombre; interés `Yoga Postparto` vía opción `8` no apareció en keywords del usuario. El log sí era correcto. Se acordó resumen con LLM al cerrar.

## Goals / Non-Goals

**Goals:**
- Al `end_session`, obtener `nombre`, `telefono` e `intereses` interpretando el diálogo completo con el LLM.
- Usar esos campos en el asunto/cuerpo PING existentes.
- Fallback seguro si el LLM falla o devuelve JSON inválido.
- Cubrir con tests el caso real (nombre+tel juntos; interés por menú/inscripción).

**Non-Goals:**
- Cambiar SMTP, timeout o formato general del mail.
- Sheet/Notion.
- Persistir el resumen fuera del email.
- Eliminar por completo toda heurística de respaldo (puede quedar como fallback).

## Decisions

1. **LLM al cierre como fuente principal del resumen**  
   - Una llamada corta `chat.completions` con el log user/assistant y respuesta JSON forzada (`nombre`, `telefono`, `intereses`).  
   - Rationale: entiende menús, confirmaciones e inscripción.  
   - Alternativa rechazada como primaria: más regex — no cubre `8` → clase.

2. **Heurística como fallback**  
   - Si falla OpenAI/parseo, usar la lógica actual (o simplificada) y “No provisto” / “Ver log / no detectado”.  
   - Rationale: el mail debe salir igual.

3. **Reutilizar cliente OpenAI y `MODEL_NAME` del chatbot**  
   - Pasar el client o invocar desde un módulo de notifications que reciba un callable/client.  
   - Preferir: función `summarize_session(history, client)` en notifications, llamada desde `end_session` con `self.client`.  
   - Temperature baja / max_tokens bajo para resumen.

4. **Instrucciones al modelo de resumen**  
   - Extraer nombre y teléfono aunque vengan en el mismo mensaje.  
   - Inferir actividad elegida por número de menú o confirmación (“me quiero inscribir”).  
   - Si falta un dato: `null` o string vacío → mapear a “No provisto”.

5. **Log del mail**  
   - Sin cambio: diálogo legible user/TIA como hoy.

## Risks / Trade-offs

- [Costo/latencia extra al cerrar] → Mitigación: una sola llamada corta; solo en end_session.
- [LLM inventa nombre] → Mitigación: prompt estricto “solo del diálogo; si no está, vacío”; temperature baja.
- [JSON mal formado] → Mitigación: parse seguro + fallback heurístico.
- [Tests frágiles con API real] → Mitigación: mock del completion en unit tests; fixture del caso Emiliano.

## Migration Plan

1. Implementar `summarize_session` LLM + integrar en `build_session_summary` / `end_session`.
2. Actualizar tests.
3. Probar cierre real con el caso de menú.
4. Rollback: revert; PING sigue funcionando con heurística si se revierte.

## Open Questions

- Ninguna bloqueante.
