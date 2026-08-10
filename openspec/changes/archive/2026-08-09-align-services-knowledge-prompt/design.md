## Context

TIA carga todo `cronograma.md` en el system context. La Agenda de Actividades usa fichas con horarios fijos y abonos; la Agenda de Servicios (Masajes) usa cita previa, tipos de sesión, seña y copy de marketing que invita a “coordinar directamente” con la profesional. El system prompt ya exige informar → anclar fecha → admin + canal de knowledge → ID, pero no aclara cómo leer fichas de servicio sin grilla horaria ni cómo resolver el conflicto de “reserva directa”.

## Goals / Non-Goals

**Goals:**
- Contrato mínimo de ficha bajo `# AGENDA DE SERVICIOS`.
- Masajes alineado a ese contrato y al flujo admin/redes.
- Prompt que obligue a usar precio/seña/tipos/sala cuando existan y prohíba tratar “coordinar con profesional” como cierre de turno por TIA.

**Non-Goals:**
- Completar kinesio, psicología, lactancia o Agenda de Eventos.
- Unificar plantillas Actividades ↔ Servicios.
- Cambiar tools, PING, modelo LLM o loader de knowledge.
- Reescritura editorial completa del tono marketing (solo el bloque de reserva y typos que afecten claridad).

## Decisions

1. **Plantilla de servicios distinta a actividades**  
   - Campos: Descripción, Requisitos, Profesionales, Disponibilidad y reserva, Valores.  
   - Rationale: cita previa ≠ clase semanal; forzar “Horarios” fijos invita a inventar.  
   - Alternativa: mismos subtítulos que actividades → rechazada.

2. **Numeración reinicia en 1 por agenda**  
   - Rationale: el modelo ancla por sección + nombre, no por ID global.  
   - Alternativa: numeración global A/S/E → innecesaria para el LLM.

3. **Knowledge es fuente de verdad del proceso de reserva de servicios**  
   - En Masajes: formaliza equipo TRAMA; canal = redes documentadas; profesionales informativos (quién atiende), no “cerrá el turno con ellas vía TIA”.  
   - Rationale: alinea PING/admin y evita canales inventados.  
   - Alternativa: WhatsApp de cada profesional → no hay datos cargados.

4. **Prompt: regla explícita para servicios con cita**  
   - Mencionar datos cargados aunque falte grilla; no inventar slots; seña/precio si están en Valores.  
   - Rationale: fallos recientes fueron omisión + “solo mirá redes”, no falta de schema estricto.

5. **Tests**  
   - Asserts de prompt (servicios/cita, seña o Valores, no reserva directa).  
   - Asserts mínimos de knowledge Masajes (precio, seña, sin “coordinar directamente” como instrucción al usuario vía copy conflictivo).  
   - Sin tests E2E de LLM.

## Risks / Trade-offs

- [El modelo igual omite seña] → Mitigación: seña bajo Valores + mención en prompt.  
- [Marketing vs admin confunde a usuarias] → Mitigación: copy de knowledge dice que el equipo pone en contacto con la profesional.  
- [Plantilla no usada en próximos servicios] → Mitigación: documentar en spec `services-knowledge`; stubs fuera de alcance.  
- [Typos residuales] → Mitigación: corregir los de la ficha Masajes tocada en este change.

## Migration Plan

1. Editar `cronograma.md` (Masajes + nota salones).  
2. Editar `system_prompt.md`.  
3. Ajustar tests.  
4. Reiniciar proceso `main.py` para recargar knowledge/prompt.  
Rollback: revertir esos archivos.

## Open Questions

- Ninguno bloqueante: kinesio/eventos se cargan después con la misma plantilla.
