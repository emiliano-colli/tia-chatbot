## Why

Las respuestas de TIA llegan en Markdown y la UI las pinta como texto crudo (`**negrita**`, listas con `-`), así que se leen mal en el navegador. En celular, al abrir el teclado se scrollea la página entera: se pierde el header y la última burbuja queda fuera del área visible.

## What Changes

- Renderizar un **subset de Markdown** solo en burbujas del bot (párrafos, `**negrita**`, listas `-`/`1.`, links `https://…`) con nodos DOM seguros, sin librería ni CDN.
- Dejar burbujas de usuario y sistema como texto plano.
- Fijar el layout a viewport: header y composer visibles; solo `#chat` scrollea; la última burbuja queda a la vista al escribir y al llegar una respuesta (CSS + `visualViewport` + `scrollIntoView`).
- Sin cambios de API, prompt ni backend.

## Capabilities

### New Capabilities

- Ninguna.

### Modified Capabilities

- `internal-chat-ui`: las respuestas del asistente se muestran con formato legible (subset Markdown); en teclado móvil el chrome de título y el composer permanecen en el viewport y el historial scrollea dejando la última burbuja visible.

## Impact

- `app/static/index.html` (CSS, viewport meta, parser subset, listener de viewport)
- `.cursor/rules/static-chat-ui.mdc` (layout de teclado + no `innerHTML` del reply)
- Tests de la página estática (`tests/test_internal_chat_ui.py`)
- Spec `internal-chat-ui`
