## Context

El parser de `[foto](…)` funciona. Knowledge tiene Sala Calma en la ficha de masajes y en `# SALONES`. El prompt pide la plantilla, pero está en “REGLAS DE COMPORTAMIENTO” (“si informás…”) y el **ejemplo de tono de masajes** no nombra salón ni media. TIA copió ese ejemplo: tipos, $50.000, seña, Gaby/Ivi, WhatsApp, ID — cero Calma.

Constraint: prompt + knowledge + tests de contenido. Sin tool nuevo ni player.

## Goals / Non-Goals

**Goals:**
- Ante detalle de un servicio/actividad con salón en knowledge, la respuesta nombra el salón y pega `foto · recorrido` aunque nadie preguntó “dónde”.
- El ejemplo de masajes del prompt deja de contradecir esa regla.

**Non-Goals:**
- Forzar media en un saludo o “¿qué es TRAMA?”.
- Completar fichas de kinesio/psico/lactancia.
- Inyectar links en Python (el modelo sigue armando el Markdown).

## Decisions

1. **Meter salón+media en el paso 1 Informar**  
   Junto a tipos/precio/seña/sala: “si `# SALONES` tiene Foto/Video de ese salón, cerrá con la plantilla”.  
   Rationale: esa plantilla es la que TIA sí sigue (WhatsApp, seña). La regla suelta al final se ignora.  
   Alternativa: tool que appendea links — más código para un fallo de prompt.

2. **Reescribir el ejemplo de masajes**  
   Incluir `Se desarrolla en Sala Calma.` y `[foto](/static/salones/calma.jpg) · [recorrido](/static/salones/calma.mp4)` después de la info útil, antes del WhatsApp/ID.  
   Rationale: el paste del usuario es ese ejemplo.  
   Alternativa: borrar el ejemplo — peor; el modelo necesita un patrón positivo.

3. **Nota `# SALONES`: “también al informar el servicio”**  
   Una línea: no hace falta que pregunten por el salón.  
   Rationale: knowledge se carga en el system; refuerza el prompt.

4. **Tests de strings, no LLM live**  
   Assert del ejemplo: `Sala Calma`, `[foto](/static/salones/calma.jpg)`, `[recorrido](`.  
   Rationale: mismo estilo que WhatsApp en `test_system_prompt.py`.

## Risks / Trade-offs

- [Listar 6 clases en Tierra = un par foto/recorrido, no seis] → La regla “un par por salón” ya existe; dejarla en Informar.  
- [El modelo sigue omitiendo] → El ejemplo es el palanca; si falla en staging, el siguiente paso sería un post-check (fuera de este change).  
- [Respuestas un poco más largas] → Aceptable: dos links cortos, no un párrafo de salón.

## Migration Plan

Editar prompt + nota knowledge + tests. Reiniciar el proceso para recargar system. Rollback: revertir esos tres archivos.

## Open Questions

Ninguna. El fallo está reproducido con el paste de masajes.
