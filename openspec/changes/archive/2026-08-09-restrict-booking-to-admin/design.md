## Context

El system prompt habla de “confirmación de inscripción” y “horario asignado” como si TIA pudiera completarlos. En la práctica solo informa y el cierre envía un PING a admin. Usuarios que dicen “me quiero inscribir” reciben promesas falsas de registro. Se acordó enfoque C: reglas de alcance + reescritura del paso de ID; misma regla para clases y servicios; derivación con canal si está en knowledge; marca simple en intereses del PING.

## Goals / Non-Goals

**Goals:**
- Prohibir en prompt formalizar inscripción/turno o afirmar que ya quedó reservado/inscripto.
- Permitir informar (horarios, precios, requisitos) e identificar contacto.
- Ante pedido de inscripción/turno: explicar rol de admin (cupo/pago), dar contacto TRAMA si consta en knowledge, y asegurar que el lead quede para el PING.
- Marcar en el resumen LLM del PING “solicitó inscripción/turno” cuando el diálogo lo indique.
- Aplicar a clases y a servicios con cita.

**Non-Goals:**
- Tool o API de booking/pagos.
- Integración con agenda real.
- Cambiar SMTP, timeout o formato general del mail.
- Rediseñar el flujo de identificación (solo limpiar lenguaje engañoso).

## Decisions

1. **Prompt-first (C)**  
   - Sección nueva de límites + editar ID para no hablar de “confirmación de inscripción / horario asignado” como acto del bot.  
   - Rationale: el defecto es de instrucción, no de código de tools.

2. **Derivación dual**  
   - Mensaje: admin confirma cupo/pago + canal de contacto desde knowledge si existe.  
   - Si no hay WhatsApp/tel en knowledge: no inventar; decir que el equipo contactará con los datos ya tomados / dejar consulta registrada.

3. **PING: solo instrucción al resumen LLM**  
   - Extender `_SUMMARY_SYSTEM_PROMPT` para que `intereses` incluya sufijo tipo `— solicitó inscripción` o `— solicitó turno` cuando aplique.  
   - Rationale: sin campos nuevos ni schema extra.

4. **Knowledge de contacto**  
   - En apply: revisar `cronograma.md`; si falta un canal oficial, agregar un dato mínimo documentado (solo si el equipo lo confirma o ya existe en materiales). Si no hay dato fiable, el prompt usa el fallback “te contactan”.

## Risks / Trade-offs

- [El modelo igual promete inscripción] → Mitigación: ejemplos negativos explícitos (“no digas voy a registrarte”).
- [Sin canal en knowledge] → Mitigación: fallback a “el equipo te contactará”.
- [Marca PING inconsistente] → Mitigación: regla clara en prompt de resumen + test con mock LLM.

## Migration Plan

1. Editar system prompt.
2. Ajustar prompt de resumen PING.
3. Completar contacto en knowledge solo si hay dato.
4. Smoke conversacional: “me quiero inscribir” no debe afirmar inscripción hecha.
5. Rollback: revert de textos.

## Open Questions

- Ninguna bloqueante para el diseño. El dato concreto de WhatsApp/tel TRAMA se confirma en apply si falta en cronograma.
