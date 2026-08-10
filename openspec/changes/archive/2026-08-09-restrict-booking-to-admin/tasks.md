## 1. Prompt and knowledge

- [x] 1.1 Actualizar `system_prompt.md`: límites (solo información; no formalizar inscripción/turno), reescritura del paso de ID sin lenguaje de confirmación/asignación, derivación a admin + canal si existe en knowledge (clases y servicios)
- [x] 1.2 Revisar `cronograma.md` por canal de contacto TRAMA; agregar dato mínimo solo si hay información fiable, si no dejar el fallback del prompt

## 2. PING summary and verification

- [x] 2.1 Extender el prompt de resumen LLM del PING para marcar en intereses “solicitó inscripción” / “solicitó turno” cuando corresponda
- [x] 2.2 Ajustar/agregar test mockeado del resumen con pedido de inscripción y verificar que el system prompt ya no empuje confirmaciones falsas
