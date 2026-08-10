## Why

TIA a veces ofrece o simula formalizar inscripciones y turnos aunque no tiene herramientas ni autoridad para cupo o pago. Eso genera expectativas falsas. Hay que limitar el chat a información y derivación a administración, para clases y servicios por igual.

## What Changes

- Actualizar el system prompt (enfoque C): reglas explícitas de alcance + reescritura del paso de identificación para eliminar lenguaje de “confirmación de inscripción / horario asignado”.
- Ante pedido de inscripción o turno: explicar que lo confirma el equipo (cupo/pago), ofrecer canal de contacto de TRAMA si está en la base de conocimiento, y dejar el lead registrado vía el flujo de cierre/PING existente.
- Ajustar el prompt de resumen del PING para marcar, sin complejidad extra, cuando la persona solicitó inscripción o turno (p. ej. en el campo intereses).
- Misma regla para actividades grupales y servicios con cita (masaje, kinesiología, etc.).

## Capabilities

### New Capabilities
- `assistant-scope`: Límites de lo que TIA puede hacer vs. lo que queda en administración (información vs. formalización de turnos/inscripciones).

### Modified Capabilities
- `admin-email-notification`: el resumen de intereses del PING MUST reflejar, cuando aplique, que se solicitó inscripción o turno.

## Impact

- Prompt: `src/prompts/system_prompt.md`
- Resumen PING: `src/notifications/ping.py` (instrucciones del LLM de resumen)
- Knowledge: solo si hace falta asegurar un dato de contacto TRAMA visible para derivar (sin inventar canales)
- Sin nuevas tools ni dependencias
- Sin cambio de SMTP/timeout
