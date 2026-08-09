## Why

El PING al admin ya se envía, pero el resumen de contacto e intereses falla en conversaciones reales: nombres dados junto al teléfono (p. ej. `Emiliano 1167462412`) y elecciones de menú (`8` → Yoga Postparto) no se detectan con heurísticas. El admin recibe `No provisto` / `Ver log / no detectado` aunque el log sí tiene la información.

## What Changes

- Reemplazar (o complementar) la extracción heurística del resumen de sesión por un resumen estructurado generado con el LLM al cerrar la sesión.
- Obtener `nombre`, `telefono` e `intereses` a partir del diálogo completo (usuario + TIA), incluyendo selecciones numéricas e intención de inscripción.
- Mantener el formato PING y el envío SMTP; si el LLM falla, degradar a valores “No provisto” / mensaje explícito sin tumbar el cierre.
- Actualizar tests con el caso real observado (nombre+tel en un mensaje; interés vía opción de menú).

## Capabilities

### New Capabilities
- (ninguna)

### Modified Capabilities
- `admin-email-notification`: el resumen Contacto/Intereses del PING MUST interpretarse desde el diálogo completo de forma robusta (no solo keywords/regex frágiles).

## Impact

- Código: `src/notifications/ping.py` (y posiblemente un helper de resumen), `src/chatbot.py` (`end_session`), tests
- Dependencias: ninguna nueva (OpenAI SDK ya en uso)
- Canal email, timeout y SMTP: sin cambio de contrato
