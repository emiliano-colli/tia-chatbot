## Why

El PING de la consulta #9 extraía bien nombre y teléfono (`emiliano 1167462412`) pero dejaba Intereses en `Ver log / no detectado` aunque el usuario preguntó por yoga y precios. El LLM de resumen trata un JSON válido con `intereses: null` como éxito y no completa con la heurística; el prompt del extractor es demasiado conservador cuando hay interés de familia (yoga) sin menú ni “me inscribo”.

## What Changes

- Completar **por campo** el resumen PING: si el LLM omite nombre, teléfono o intereses, rellenar ese hueco con la heurística (keywords / regex) en lugar de dejar el placeholder.
- Hacer el prompt del extractor **explícito**: preguntar por una actividad (“tienen clases de yoga”), pedir precios/horarios de lo ya hablado, o nombrar varias variantes sin elegir una, **sí cuenta** como interés; no exigir menú numérico ni pedido de inscripción para llenar el campo.
- Cuando el diálogo nombra una familia (p. ej. yoga) y no una clase puntual, el campo MUST reflejar esa familia (p. ej. `yoga`), no `null`.
- Mantener las marcas `solicitó inscripción` / `solicitó turno` cuando el diálogo las muestre; no inventarlas si solo hubo consulta informativa.
- Cubrir con un test el transcript real (yoga → precios → nombre+tel) además del caso de menú `8`.

## Capabilities

### New Capabilities

- (ninguna)

### Modified Capabilities

- `admin-email-notification`: el resumen de Intereses MUST usarse aunque el LLM devuelva `null` si el diálogo identifica la actividad; merge heurístico por campo vacío; el extractor MUST tratar preguntas y pedidos de detalle como interés, no solo menú/inscripción.

## Impact

- `src/notifications/ping.py` (`build_session_summary`, `_SUMMARY_SYSTEM_PROMPT`, heurística de keywords)
- `tests/test_admin_notification.py` (caso yoga+precios+contacto; merge LLM null + keyword)
- CSV de cierre y asunto/cuerpo PING: mismo contrato de campos; el valor de `interes` deja de quedar en placeholder cuando el log lo identifica
- Sin cambios de SMTP, gate de contacto, UI ni prompt conversacional de TIA
