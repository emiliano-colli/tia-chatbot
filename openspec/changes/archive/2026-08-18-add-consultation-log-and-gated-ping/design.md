## Context

`end_session` siempre llama `send_admin_ping` tras `build_session_summary`. Un “Hola” + timeout genera mail. No hay ID correlativo ni archivo de consultas. El UUID de `localStorage` no cuenta volumen.

Hay que asignar el ID **en el primer mensaje** para poder mostrarlo en la UI durante la charla, y persistir la fila CSV **al cerrar**.

Constraint: sin DB nueva, un proceso Uvicorn en staging, Excel-friendly.

## Goals / Non-Goals

**Goals:**
- ID entero correlativo por consulta.
- CSV al cierre: id, datetime, nombre, teléfono, interés, origen.
- PING solo con nombre o teléfono reales.
- ID + contacto + interés en asunto y cuerpo del mail.
- ID discreto en UI web y una línea en CLI.
- Origen `web` / `cli` ahora (redes después, misma columna).

**Non-Goals:**
- Dashboard, Notion, Google Sheets.
- Autenticación del CSV.
- Integración Meta/IG (solo reservar columna `origen`).
- Reemplazar el UUID de sesión.
- Mostrar el ID de forma prominente (hero, burbuja de sistema).

## Decisions

1. **ID al primer `ask()` que crea historial, no al cierre**  
   Guardar `consulta_id` y `origin` en dicts junto a la sesión.  
   Rationale: la UI necesita el número durante la conversación.  
   Alternativa ID solo al close: no se puede mostrar a tiempo.

2. **Contador en archivo + CSV de cierres**  
   - `CONSULTATION_SEQ_PATH` (default `data/consulta_seq.txt`): entero, incrementado bajo lock.  
   - `CONSULTATION_LOG_PATH` (default `data/consultas.csv`): append al `end_session`.  
   Columnas: `id,closed_at,nombre,telefono,interes,origen,reason`.  
   Rationale: CSV para Excel; el seq file evita re-escanear y permite huecos si hay crash antes del close (aceptable).  
   Alternativa SQLite: más de lo pedido.

3. **Origen explícito, no inferido del UUID**  
   `ask(session_id, message, origin="web"|"cli")`. FastAPI manda `web` (query/body opcional, default `web` en `/chat`). CLI manda `cli`. Gradio, si se usa, `gradio`.  
   Redes: mismo campo, valores nuevos después.

4. **Contacto significativo**  
   `has_contact(summary)`: nombre o teléfono no vacíos y distintos de `No provisto` / `Sin identificar` (case-insensitive). Interés ignorado para el gate.

5. **Formato de mail**  
   Asunto: `Nueva consulta TIA #{id} — {nombre} / {telefono} / {interes}` omitiendo segmentos vacíos.  
   Cuerpo: ID, Contacto, Intereses, Origen, Log.  
   Si no hay PING, el CSV igual se escribe.

6. **API**  
   `ChatResponse`: `reply` + `consulta_id: int`.  
   UI: texto muted tipo `#12` en el header (junto al título) o en el toolbar, `font-size` chico, sin competir con “Nueva consulta”.

7. **Timezone**  
   `closed_at` en `America/Argentina/Buenos_Aires` ISO-like `YYYY-MM-DD HH:MM`.

8. **CSV fuera de git**  
   `data/` en `.gitignore`. Path configurable para el CT (volumen persistente).

## Risks / Trade-offs

- [Huecos de ID si el proceso muere entre assign y close] → Aceptado; el correlativo sigue siendo cota de volumen.  
- [Dos workers Uvicorn] → Lock de archivo; staging es un proceso.  
- [LLM etiqueta “Hola” como nombre] → El gate usa los mismos placeholders; tests con “Hola” solo MUST NOT ping.  
- [CSV con PII en disco del CT] → Mismo nivel que el mail; no exponer `/static`. Runbook: permisos de archivo.  
- [Recrear el CT borra el seq] → Runbook: path en volumen o backup.

## Migration Plan

1. Código + tests (cierre sin contacto = CSV sí, mail no; con contacto = ambos).  
2. `.env.example` + gitignore `data/`.  
3. Staging: directorio persistente, restart `tia.service`.  
4. UI: primer `/chat` pinta `#N`.

Rollback: revertir; el CSV acumulado se conserva.

## Open Questions

- Ninguno bloqueante.
