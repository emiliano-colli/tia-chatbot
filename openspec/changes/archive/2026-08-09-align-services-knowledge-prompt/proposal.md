## Why

La Agenda de Servicios (empezando por Masajes) ya tiene contenido útil, pero el copy de “coordiná directamente con la profesional” choca con el flujo del prompt (formaliza admin + canal de knowledge + identificación). Además, Actividades y Servicios no comparten la misma plantilla de campos; hace falta un contrato mínimo de ficha de servicio y reglas de respuesta para que TIA afirme el servicio, cite precio/seña/tipos cuando existan, y derive sin contradicciones.

## What Changes

- Definir y aplicar una plantilla mínima para ítems de `# AGENDA DE SERVICIOS` (Descripción, Requisitos, Profesionales, Disponibilidad y reserva, Valores).
- Alinear la ficha de Masajes: quitar “coordiná directamente”; formalización vía equipo TRAMA + redes de la base; tipografía/typos menores en esa ficha y nota de salones.
- Actualizar el system prompt: al informar servicios con cita, usar campos disponibles (tipos, precio, seña, sala) aunque no haya grilla horaria; no interpretar “coordinar con profesional” como que TIA reserva el turno.
- No inventar horarios fijos ni canales ausentes; no reestructurar la Agenda de Actividades grupales.
- No completar aún kinesio/psico/lactancia ni Agenda de Eventos (quedan fuera de alcance salvo dejar la plantilla documentada para uso futuro).

## Capabilities

### New Capabilities
- `services-knowledge`: Contrato de estructura y contenido de la Agenda de Servicios en la base de conocimiento, y cómo TIA debe leer esas fichas.

### Modified Capabilities
- `assistant-scope`: Derivación de turnos de servicios debe priorizar info útil de la ficha (precio/seña/tipos) y no sugerir que el asistente o el usuario “cierran” el turno solo con la profesional, fuera del flujo admin/canal documentado.
- `conversation-flow`: Respuestas sobre servicios con cita deben mencionar datos operativos cargados (p. ej. seña) y evitar lenguaje de reserva directa incompatible con el deferral.

## Impact

- `src/knowledge/cronograma.md` (Agenda de Servicios / Masajes).
- `src/prompts/system_prompt.md` (plantilla de información y derivación).
- Tests de contenido del prompt (y, si aplica, asserts mínimos sobre knowledge de masajes).
- Specs OpenSpec nuevas/delta; sin cambios de runtime de tools ni API.
