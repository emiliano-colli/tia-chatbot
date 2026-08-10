## Context

Tras `restrict-booking-to-admin`, una charla real mostró fricción: re-pedido de datos, “mañana” sin tool de fecha, derivación sin valor informativo, lenguaje “registré”, ID demasiado temprano ante un síntoma, y omisión de Instagram/Facebook ya en knowledge. El punto 3 (fichas de servicios) queda fuera: lo completará el equipo de contenido.

## Goals / Non-Goals

**Goals (puntos 1, 2, 4, 5, 6, 7):**
1. No re-pedir nombre/tel si ya están en el historial de la conversación.
2. Ante “hoy/mañana/esta semana”, usar siempre `get_current_datetime` y verbalizar el día.
4. Al pedir turno/inscripción: informar lo disponible → anclar fecha si aplica → derivar a admin + canal.
5. Evitar lenguaje operativo tipo “registré / he registrado tu consulta”.
6. Pedir ID cuando hay interés concreto en un servicio/actividad o pedido de detalle operativo; no solo por un síntoma genérico.
7. Al derivar, ofrecer canal de knowledge (p. ej. redes TRAMA) cuando exista.

**Non-Goals:**
- Completar horarios/precios de masajes/kinesio en `cronograma.md` (punto 3).
- Nuevas tools o cambios de runtime salvo tests de prompt.
- Cambiar SMTP/PING/timeout.

## Decisions

1. **Solo prompt (+ tests de contenido)**  
   - Rationale: los fallos son de instrucción; la memoria de sesión ya está en el historial que ve el modelo.

2. **Editar secciones existentes**  
   - ID: timing + “si ya los dio, no los pidas de nuevo”.  
   - Límites / inscripción-turno: plantilla informar→fecha→derivar+canal.  
   - Comportamiento: reforzar tool fecha y verbalizar día; lenguaje sin “registré”.

3. **Specs**  
   - Nueva capability `conversation-flow`.  
   - Delta en `current-datetime-tool` (anclar día en respuesta).  
   - Delta en `assistant-scope` (ofrecer canal de forma consistente en la plantilla útil).

## Risks / Trade-offs

- [El modelo igual re-pide datos] → Mitigación: regla explícita + ejemplo negativo en prompt.
- [Pide ID demasiado tarde y da precios sin datos] → Mitigación: mantener “antes del detalle de horarios/precios/requisitos” salvo que ya los tenga.
- [Sin ficha de masaje (punto 3)] → Mitigación: honestidad “no tengo ese dato cargado”; no inventar.

## Migration Plan

1. Actualizar `system_prompt.md`.
2. Tests de presencia de reglas clave en el prompt.
3. Smoke manual opcional con el caso Obi Wan.
4. Rollback: revert del prompt.

## Open Questions

- Ninguna bloqueante.
