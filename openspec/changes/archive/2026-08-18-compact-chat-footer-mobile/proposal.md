## Why

En celular el footer del chat interno deja un hueco grande entre el hint de despedida y el input: el toolbar pasa a columna y hereda `flex-basis: 12rem` pensado como ancho, que se vuelve altura (~192px). El área de escribir ocupa cerca de media pantalla y el chat se achica.

## What Changes

- Compactar el chrome inferior en viewports estrechos: el footer MUST huguear su contenido; sin vacío grande entre “Escribí chau…” y el composer.
- En el media query de columna, anular el `flex-basis` del hint (`flex: 0 0 auto`) y apretar padding/gaps del footer si hace falta.
- Dejar una Cursor rule en `.cursor/rules/static-chat-ui.mdc` para que futuros edits de `app/static/**` no reintroduzcan el mismo patrón.
- Sin cambios de copy, JS, API ni Gradio.

## Capabilities

### New Capabilities

- Ninguna.

### Modified Capabilities

- `internal-chat-ui`: en viewport de celular el footer MUST permanecer compacto; el hint, “Nueva consulta” y el composer MUST quedar juntos, sin un bloque vacío entre el hint y el input.

## Impact

- `app/static/index.html` (CSS del toolbar/footer en el breakpoint móvil)
- `.cursor/rules/static-chat-ui.mdc` (rule de chrome compacto)
- `openspec/specs/internal-chat-ui/spec.md` (requisito de footer compacto)
- Sin backend, tests de API ni dependencias nuevas
