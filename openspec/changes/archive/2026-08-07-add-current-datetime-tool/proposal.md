## Why

TIA responde preguntas sobre actividades y horarios del cronograma, pero el modelo no conoce el día/hora reales. Sin eso, interpreta mal “hoy”, “mañana” o “esta semana” y puede inventar la fecha. Hace falta una herramienta on-demand para anclar respuestas temporales a la hora real de Buenos Aires.

## What Changes

- Agregar una tool OpenAI `get_current_datetime` que devuelve fecha, hora y día de la semana en español, timezone `America/Buenos_Aires`.
- Extender `TiaChatbot.ask()` con un loop de tool-calling: ejecutar la tool cuando el modelo la solicite y devolver la respuesta final.
- Actualizar el system prompt para obligar el uso de la fecha actual en interpretaciones temporales y prohibir inventar la fecha.
- Agregar tests unitarios del formateo/timezone de la tool (y cobertura mínima del flujo si es práctico con mocks).

## Capabilities

### New Capabilities
- `current-datetime-tool`: Tool on-demand de fecha/hora actual y su uso en respuestas con interpretación temporal.

### Modified Capabilities
- (ninguna)

## Impact

- Código: `src/chatbot.py` (tool loop), nuevo módulo pequeño para la tool (p. ej. `src/tools/` o similar), `src/prompts/system_prompt.md`
- Tests: nuevos o extendidos en `tests/`
- API/CLI/Gradio: sin cambio de contratos HTTP; el comportamiento conversacional mejora en preguntas temporales
- Dependencias: ninguna nueva (stdlib + OpenAI SDK existente)
