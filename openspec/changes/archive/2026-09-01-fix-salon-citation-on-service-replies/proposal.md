## Why

La plantilla `foto · recorrido` ya está en knowledge y en el prompt, pero TIA no la usa al informar un servicio. En una consulta de masajes citó tipos, precio, seña, Gaby/Ivi y WhatsApp, y **omitió Sala Calma y los links**. Solo aparece si preguntás por los salones. El ejemplo de tono del prompt para masajes tampoco nombra salón ni media: el modelo copia ese patrón.

## What Changes

- Tratar salón + `foto · recorrido` como parte del **Informar** (paso 1 de la plantilla de inscripción/turno y de cualquier detalle de ficha), no como una regla extra “si hablás del salón”.
- Corregir el ejemplo de masajes del prompt para que incluya Sala Calma y `[foto](…) · [recorrido](…)`.
- Aclarar en spec que un pedido de info de masajes (u otra actividad/servicio con salón en knowledge) MUST nombrar el salón y pegar la media, aunque el usuario no haya preguntado por el lugar.
- Tests de contenido del prompt (ejemplo con Calma + `[foto]` / `[recorrido]`).
- Fuera de alcance: player en la burbuja, fichas nuevas, cambiar paths de `/static/salones/`.

## Capabilities

### New Capabilities

- Ninguna.

### Modified Capabilities

- `conversation-flow`: la citación de salón/media MUST aplicarse al informar un servicio o actividad (p. ej. masajes → Sala Calma + `foto · recorrido`), no solo cuando el usuario pregunta por salones.
- `assistant-scope`: al informar un servicio con cita, si knowledge tiene sala (y Foto/Video en `# SALONES`), MUST incluirlos en esa respuesta informativa; MUST NOT omitirlos porque el usuario no preguntó “dónde”.

## Impact

- `src/prompts/system_prompt.md` (plantilla Informar + ejemplo de masajes + regla de salones)
- `src/knowledge/cronograma.md` (nota de citación: “también al informar el servicio, no solo si preguntan el salón”)
- `tests/test_system_prompt.py`
- Specs `conversation-flow` y `assistant-scope`
