## Why

La página de chat interna (`GET /`) se usa desde el celular en staging, pero el layout no envuelve: hay que panear horizontalmente para ver el título, el subtítulo o los botones. Además el subtítulo actual no nombra las ofertas principales (yoga, entrenamiento funcional, salud y bienestar).

## What Changes

- Reemplazar el subtítulo del header por: `Preguntame sobre clases de yoga, entrenamiento funcional, talleres, servicios de salud, bienestar y más 🌿`.
- Ajustar el CSS de la misma página para que en viewports estrechos el header, el toolbar y el composer quepan sin scroll horizontal: texto que envuelve, controles que pasan a la siguiente línea, y el alto de viewport respete la barra del navegador móvil.
- Dejar Gradio fuera de alcance (sigue el copy viejo); el canal de testers internos es la UI estática de FastAPI.

## Capabilities

### New Capabilities

- Ninguna.

### Modified Capabilities

- `internal-chat-ui`: el header MUST mostrar el copy ampliado; la página MUST ser usable en viewports de celular sin desplazamiento horizontal para leer el título o alcanzar los botones.

## Impact

- `app/static/index.html` (copy del subtítulo + CSS; sin cambio de JS ni de API)
- `openspec/specs/internal-chat-ui/spec.md` (requisitos de copy y layout móvil)
- `tests/test_internal_chat_ui.py` (afirmar el subtítulo en el HTML servido, si el test ya inspecciona el markup)
- Sin cambios de backend, Gradio, Nginx ni dependencias
