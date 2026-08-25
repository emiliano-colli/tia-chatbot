## Why

TIA ya puede pegar paths de foto y video de cada salón, pero el chat muestra la ruta cruda (`/static/salones/aire.mp4`) y el prompt no fija un copy corto. Eso ocupa lugar, no distingue imagen de recorrido y pelea con horarios, precios y quién da la clase — que es lo importante.

## What Changes

- Citar media de salón con la plantilla acordada: primero la información útil; luego el salón; luego dos links cortos **`foto · recorrido`** (el nombre del salón no se repite en los links si ya está en la frase).
- Renderizar Markdown `[texto](href)` en burbujas del bot para que se lea `foto` / `recorrido` y no la ruta.
- Ajustar prompt (y, si hace falta, una línea en `# SALONES`) para que TIA use esa citación solo cuando knowledge tiene Foto y/o Video de ese salón; no inventar URLs; no repetir el mismo par si varias actividades van al mismo salón; clases virtuales sin media.
- Fuera de alcance: fichas nuevas de kinesio/psico/lactancia, player de video en la burbuja, URLs absolutas para WhatsApp.

## Capabilities

### New Capabilities

- Ninguna.

### Modified Capabilities

- `internal-chat-ui`: las burbujas del bot MUST parsear enlaces Markdown `[label](href)` (http(s) y `/static/…`) y mostrar el `label` como texto clickeable, no el href.
- `conversation-flow`: al informar una actividad o servicio con salón y media en knowledge, TIA MUST citar foto/recorrido con la plantilla breve (info útil → salón → `foto · recorrido`).

## Impact

- `app/static/index.html` (`renderBotMarkdown` / `appendInline`)
- `.cursor/rules/static-chat-ui.mdc`
- `src/prompts/system_prompt.md`
- `src/knowledge/cronograma.md` (solo copy de citación en `# SALONES` si hace falta; paths ya existen)
- Tests de UI y de contenido del prompt
- Specs `internal-chat-ui` y `conversation-flow`
