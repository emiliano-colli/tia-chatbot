## Why

La base y el prompt dicen que el canal público son solo Instagram/Facebook y que **no hay WhatsApp**, así que TIA deriva inscripciones y turnos a redes y se niega a dar un número que el equipo ya usa. Hace falta priorizar el WhatsApp de consultas (con horario) y, en paralelo, dar a TIA una ficha BIO del equipo empezando por Caro Losada, para que pueda presentar a las personas del espacio sin inventar.

## What Changes

- Sustituir el bloque de “no hay WhatsApp / solo redes” en knowledge por el **WhatsApp de consultas** como canal prioritario: **+54 11 6956-6115**, **lunes a viernes de 09 a 21 hs**.
- Dejar Instagram/Facebook como canales secundarios (siguen en Redes), no como el camino principal de inscripción/turnos.
- Alinear el copy de **Masajes / formalización** y el **system prompt** para pegar número + horario cuando se derive, y dejar de instruir “no inventes WhatsApp” como si el dato no existiera (sigue vigente no inventar **otros** números).
- Crear una sección **BIO del equipo** en knowledge, empezando por Caro Losada con el texto provisto (creadora de Maternar y TRAMA). Otras bios se agregan cuando haya copy; no inventarlas.

## Capabilities

### New Capabilities

- `team-bios`: sección de bios del equipo en la base de conocimiento; TIA cita lo cargado (empezando por Caro Losada) y no inventa biografías faltantes.

### Modified Capabilities

- `services-knowledge`: el canal público de inscripción/turnos en knowledge es el WhatsApp de consultas (número + horario); las fichas de reserva (p. ej. Masajes) apuntan a ese canal, no solo a redes.
- `assistant-scope`: al derivar inscripción/turno, TIA MUST priorizar el WhatsApp documentado (número y franja horaria) frente a redes; MUST NOT afirmar que no hay WhatsApp si está en la base.
- `conversation-flow`: al pegar canal de contacto, MUST usar el dato concreto de WhatsApp (+ horario) cuando figure en knowledge; redes solo como complemento.

## Impact

- `src/knowledge/cronograma.md` (contacto, Masajes, nueva sección BIO)
- `src/prompts/system_prompt.md` (derivación: WhatsApp primero; no contradecir la base)
- Specs delta de las capabilities listadas
- Tests de knowledge/prompt que hoy asumen “solo Instagram” o “no inventes WhatsApp” como ausencia de número
- Sin cambios de API, CSV, PING ni UI
