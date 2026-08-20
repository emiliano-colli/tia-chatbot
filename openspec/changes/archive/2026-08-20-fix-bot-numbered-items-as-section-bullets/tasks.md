## 1. Parser y CSS

- [x] 1.1 Dejar de crear `<ol>` en `renderBotMarkdown`; cada `^\d+\. ` es `.md-section` + `p.md-item` (viñeta `•`)
- [x] 1.2 Anidar en esa sección las líneas `-`/`*` siguientes (Horarios / días); cortar ante heading, otro `1.` o párrafo
- [x] 1.3 CSS de `.md-section` / `.md-item` (indent de la ul hija; `•` distinto del ▸ de `###`)

## 2. Prompt y tests

- [x] 2.1 Pista en `system_prompt.md`: actividades con horarios = `###` o `**Nombre:**` + `-`, no `1.` por clase
- [x] 2.2 Tests GET `/`: `md-section` o `md-item`; el renderer no hace `createElement("ol")`
