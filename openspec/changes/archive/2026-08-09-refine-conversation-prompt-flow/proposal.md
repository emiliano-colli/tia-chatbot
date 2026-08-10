## Why

En pruebas reales TIA vuelve a pedir nombre/teléfono ya dados, no ancla “mañana” con la tool de fecha, prioriza el discurso de formalización sin aportar valor informativo, usa lenguaje tipo “registré tu consulta”, pide identificación demasiado temprano ante síntomas, y no ofrece los canales de contacto que sí están en knowledge. Eso genera fricción y respuestas pobres aunque los límites de booking ya existan.

## What Changes

- Refinar el system prompt para: no re-pedir datos ya aportados en la conversación; timing más tardío del pedido de ID; lenguaje sin “registré” operativo; plantilla útil al pedir turno/inscripción (informar → anclar fecha → derivar + canal); ofrecer redes/canal de TRAMA cuando existan en knowledge.
- Reforzar el uso obligatorio de `get_current_datetime` ante “hoy/mañana/esta semana” (y typos obvios) y verbalizar el día concreto.
- **Fuera de alcance de este change:** completar fichas de masajes/kinesiología/precios en knowledge (punto 3; lo hará el equipo de contenido).

## Capabilities

### New Capabilities
- `conversation-flow`: Flujo conversacional de identificación, memoria de datos, timing, lenguaje y respuestas útiles al derivar turnos/inscripciones.

### Modified Capabilities
- `current-datetime-tool`: reforzar que referencias relativas como “mañana” MUST disparar la tool y anclarse a una fecha concreta en la respuesta.
- `assistant-scope`: al derivar inscripción/turno, MUST ofrecer canal de contacto de knowledge cuando exista (redes u otro), sin inventar.

## Impact

- Principalmente `src/prompts/system_prompt.md`
- Tests de contenido del prompt (y/o escenarios documentados)
- Sin cambios de tools, SMTP ni knowledge de precios/horarios de servicios
