## Context

Al cerrar la sesión, `build_session_summary` llama al LLM con el diálogo completo y, si el JSON parsea, **usa esos tres campos tal cual**. La heurística (keywords en mensajes del usuario + regex de nombre/tel) solo corre si la llamada falla.

En producción (consulta #9) el LLM extrajo `Emiliano` y `1167462412` pero devolvió `intereses: null`. El usuario había escrito “tienen clases de yoga ?” y “precios”. El placeholder `Ver log / no detectado` salió en el mail. La heurística habría puesto `yoga`, pero no se ejecutó.

El prompt del extractor está sesgado al caso menú (`8` → Yoga Postparto) e inscripción. Ante una familia de actividades sin elección ni “me inscribo”, `gpt-4o-mini` elige `null` por “no inventes”.

## Goals / Non-Goals

**Goals:**
- Si el LLM deja un campo vacío y la heurística tiene valor, usar el valor heurístico en ese campo.
- Que el extractor trate pregunta + pedido de detalle (precios/horarios) como interés de familia, sin exigir menú ni inscripción.
- Cubrir el transcript #9 con un test (LLM mockeado con `intereses: null`).

**Non-Goals:**
- Cambiar SMTP, gate de contacto (`has_contact`), timeout, UI o el prompt conversacional de TIA.
- Expandir la heurística a mensajes de TIA (riesgo de marcar todo el cronograma).
- Inferir una clase puntual (Prenatal vs Hatha) cuando el usuario no la eligió.
- Inventar “solicitó inscripción/turno” en consultas solo informativas.
- Logging del JSON del extractor (útil, fuera de este cambio).

## Decisions

1. **Merge por campo, no all-or-nothing**  
   Siempre calcular la heurística (barata, local). Si el LLM devolvió JSON:
   - para `nombre`, `telefono`, `intereses`: si el valor LLM es placeholder (`null`, vacío, `No provisto`, `Ver log / no detectado`, etc.), sustituir por el valor heurístico **si este no es placeholder**.
   - si el LLM ya trajo un valor (p. ej. `Yoga Postparto — solicitó inscripción`), no pisarlo con keywords (`yoga`).  
   Rationale: el LLM sigue siendo mejor para menú `8` y nombre sin “me llamo”; la heurística tapa el hueco de #9.  
   Alternativa rechazada: “si intereses es null, descartar todo el JSON y usar solo heurística” — perderíamos el nombre `Emiliano`.

2. **Prompt del extractor más explícito**  
   Añadir reglas:
   - Preguntar si hay una actividad (“tienen clases de yoga”) **es** interés.
   - Pedir precios, horarios o requisitos de lo ya hablado **es** interés, aunque el mensaje sea una sola palabra (`precios`).
   - Si hay varias variantes (Prenatal / Postparto / Hatha) y no eligió una, poner la **familia** (`yoga` o `clases de yoga`), no `null`.
   - Inscripción/turno solo si el diálogo lo muestra; no marcarlos en una consulta informativa.
   Rationale: el modelo era conservador porque las únicas reglas positivas eran menú e inscripción.  
   Alternativa rechazada: solo merge, sin tocar el prompt — el merge cubre #9 (keyword en el usuario) pero no el caso “usuario dice precios” sin haber escrito “yoga”.

3. **Heurística de interés sin cambio de fuente**  
   Seguir buscando `_ACTIVITY_KEYWORDS` solo en texto del **usuario**.  
   Rationale: TIA a menudo lista muchas actividades; escanear al asistente inflaría falsos positivos. El prompt cubre el caso en que el keyword está solo en la respuesta de TIA.

4. **Tests con mock, no API real**  
   - History tipo #9 + LLM `{intereses: null}` → `interests` contiene `yoga`.  
   - LLM con interés específico → no se pisa.  
   - Aserción de fragmentos nuevos en `_SUMMARY_SYSTEM_PROMPT` (pregunta / familia / no exigir inscripción).  
   Reutilizar `_mock_llm_client` de `tests/test_admin_notification.py`.

## Risks / Trade-offs

- [Keyword genérico pisa un `null` correcto, p. ej. el usuario dijo “yoga” en broma] → Mitigación: el mail sigue incluyendo el Log; el admin ve el contexto. Preferible un falso positivo de `yoga` a `no detectado`.
- [LLM escribe “no se puede determinar” en vez de `null`] → Mitigación: tratar frases equivalentes como placeholder en el merge (mismo set que `_MISSING_INTEREST` o ampliarlo).
- [Doble fuente: prompt vs merge] → Mitigación: el prompt reduce cuántas veces hace falta el merge; el merge es la red. No son excluyentes.

## Migration Plan

1. Merge + prompt en `src/notifications/ping.py`.
2. Tests del transcript #9 y de no-pisar.
3. Deploy/restart del proceso; el siguiente PING usa la lógica nueva (sin migración de CSV viejo).
4. Rollback: revert del archivo; el cierre de sesión sigue funcionando con el comportamiento anterior.

## Open Questions

- Ninguna bloqueante. Si más adelante el admin quiere “Yoga Prenatal / Postparto / Hatha” en vez de `yoga` cuando no eligió clase, se puede afinar el prompt sin cambiar el merge.
