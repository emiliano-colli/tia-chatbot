## Why

El Consultorio de Lactancia ya se nombra en el contexto y en `# SALONES`, pero no tiene ficha en `# AGENDA DE SERVICIOS`. TIA no puede citar horarios, precio, seña, profesionales ni el WhatsApp de Natalia sin inventar. Hace falta la ficha operativa y que un WhatsApp de profesional, cuando la ficha lo declara, se cite **además** del 6115 de TRAMA, no en su lugar.

## What Changes

- Agregar `## 2. Consultorio de Lactancia` con la plantilla de servicios (descripción, requisitos, profesionales, disponibilidad/reserva, valores).
- Documentar grilla (mar/jue 08–12, mié 10–13, vie 14–18), modalidad espontánea **y** turno programado, Consultorio + `foto · recorrido`, $50.000 / seña 50% para reservar turno.
- Profesionales: Natalia (mar/jue/vie, `+54 11 3198-9930`) y Carolina (miércoles y consultas generales; el 6115 **es** el WhatsApp de TRAMA).
- Ajustar prompt (y specs) para que, si una ficha declara WhatsApp de profesional, TIA lo pegue **además** del canal general; sigue vigente no inventar números que no estén en knowledge.
- Fuera de alcance: BIO de Natalia, kinesio/psico, player de video, cambiar el 6115 como default del resto de servicios.

## Capabilities

### New Capabilities

- Ninguna.

### Modified Capabilities

- `services-knowledge`: ficha 2 de lactancia en la agenda de servicios; un servicio MAY declarar WhatsApp de profesional además del canal general de TRAMA.
- `assistant-scope`: al informar o derivar un servicio cuya ficha lista WhatsApp de profesional, TIA MUST citarlo además del 6115; MUST NOT omitirlo por “priorizar solo consultas” ni tratarlo como sustituto del canal TRAMA.
- `conversation-flow`: respuestas de lactancia MUST usar grilla, dual WhatsApp y media del Consultorio; la seña aplica a turno programado, no a demanda espontánea.

## Impact

- `src/knowledge/cronograma.md` (ficha 2; sin tocar `# SALONES` salvo consistencia de copy)
- `src/prompts/system_prompt.md` (canal extra si la ficha lo declara)
- Specs delta de las capabilities listadas
- Tests de knowledge/prompt (ficha lactancia + número de Natalia + regla de dual WhatsApp)
- Sin cambios de API, CSV, PING ni UI
