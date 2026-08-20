## Why

En respuestas tipo “¿tienen yoga?”, cada clase se ve con **1.** en el navegador, pero ese número no está en el texto copiado: es el marcador CSS de `<ol>`. TIA escribe `1. Yoga Prenatal` y debajo `- Horarios:`; el parser cierra el `<ol>` en el primer ítem, abre un `<ul>`, y la clase siguiente es otro `<ol>` que otra vez arranca en 1.

## What Changes

- Dejar de pintar ítems `1.` / `2.` como lista ordenada en burbujas bot.
- Tratar cada línea numerada como **título de bloque** (viñeta distinta a `###`, p. ej. `•`) y anidar debajo las viñetas `-` de horarios (sub-orden indentado).
- Añadir una pista breve en el system prompt: actividades con horarios = título + `-`, no `1.` por clase.
- Caso de prueba: el patrón real de la respuesta de yoga (nombre de clase + `- Horarios:` + días).

## Capabilities

### New Capabilities

- Ninguna.

### Modified Capabilities

- `internal-chat-ui`: las líneas `1.` del asistente MUST NOT mostrarse como `<ol>` que reinicia en 1; MUST verse como sección con viñeta y los `-` siguientes como sublista.

## Impact

- `app/static/index.html` (parser + CSS; sin `<ol>` en bot)
- `src/prompts/system_prompt.md` (una regla de formato de listas)
- Tests GET `/` (tokens del parser: no crear `ol` para bot, o `md-section`)
- Spec `internal-chat-ui`
