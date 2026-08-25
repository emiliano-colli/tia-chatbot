## 1. Parser de links con label

- [x] 1.1 En `appendInline`, parsear `[label](href)` antes que autolink; `<a textContent=label>` solo si href es `http(s):` o `/static/`; otro esquema = texto plano
- [x] 1.2 Mantener autolink de URLs y `/static/…` sueltos; `target="_blank"` + `rel="noopener noreferrer"`
- [x] 1.3 Actualizar `.cursor/rules/static-chat-ui.mdc`: subset incluye `[label](href)` seguro

## 2. Citación en prompt y knowledge

- [x] 2.1 Prompt: plantilla info útil → nombrar salón → `[foto](path) · [recorrido](path)`; no repetir el nombre en el label; no inventar si falta Foto/Video; un par por salón; virtual sin media
- [x] 2.2 Nota en `# SALONES`: misma plantilla de citación (paths siguen siendo la fuente del href)

## 3. Tests

- [x] 3.1 GET `/`: el parser incluye el token `[label](href)`
- [x] 3.2 Tests de prompt/knowledge: labels `foto` / `recorrido` y Markdown `[foto](`/`[recorrido](`
