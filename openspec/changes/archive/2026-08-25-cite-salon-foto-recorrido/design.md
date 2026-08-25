## Context

`# SALONES` ya tiene Foto/Video en `/static/salones/…`. El loader omite líneas si el archivo no está. El prompt pide pegar esas rutas tal cual. `appendInline` autolinkea `http(s):` y `/static/…` mostrando **el href** como texto. En el globo queda `/static/salones/aire.mp4`, largo y sin decir si es imagen o recorrido.

Copy acordada (opción A): la info útil primero; el salón en una frase; los links solo `foto` y `recorrido`, sin repetir el nombre.

Constraint: un HTML, `createElement`/`textContent`, sin CDN, sin `innerHTML` del reply.

## Goals / Non-Goals

**Goals:**
- Texto visible del enlace = `foto` o `recorrido`, no la ruta.
- Plantilla de citación en prompt (+ nota en `# SALONES`).
- Href permitidos: `http(s):` y `/static/…` (mismo criterio de seguridad que el autolink actual).

**Non-Goals:**
- Reproductor `<video>` o `<img>` en la burbuja.
- Completar fichas de kinesio/psico/lactancia.
- URLs absolutas / WhatsApp media.
- Cambiar nombres de archivo en `/static/salones/`.

## Decisions

1. **Markdown `[label](href)` en `appendInline`, antes que autolink**  
   Token `\[([^\]]+)\]\(([^)]+)\)`. El `<a>` usa `textContent = label` y `href` solo si el destino es `https?:` o empieza con `/static/`. Si no, el match queda texto plano.  
   Rationale: es el subset que TIA ya “sabe” escribir; el label corto es el punto de este change.  
   Alternativa: CSS/`title` sobre la URL cruda — sigue ocupando una línea. Alternativa: `textContent` hardcodeado en JS según extensión — frágil si el modelo no pega la ruta.

2. **Plantilla en el prompt, no lógica extra en Python**  
   TIA arma `[foto](/static/…jpg) · [recorrido](/static/…mp4)` después de nombrar el salón. Si falta Foto o Video en knowledge (loader), no inventa ese link. Varias actividades del mismo salón → un solo par. Virtual → nada.  
   Rationale: el mapa salón→archivo ya está en knowledge; no hace falta un tool.  
   Alternativa: el backend inyecta los links — más código para un copy de tres palabras.

3. **Autolink de rutas sueltas se mantiene**  
   Si el modelo se olvida del `[foto](…)` y pega `/static/…`, sigue siendo clickeable (texto = path). Peor UX, no 404 de parser.  
   Rationale: red de seguridad. Tests del prompt cubren la forma canónica.

4. **Separador ` · ` (espacio-punto medio-espacio)**  
   Una línea, dos links. No una lista `-` (compite con horarios).

## Risks / Trade-offs

- [El modelo escribe `foto` sin Markdown] → Autolink no aplica a la palabra “foto”; se ve texto muerto. Mitigación: ejemplo literal en el prompt.  
- [Href `javascript:` dentro de `[]()` ] → Rechazar; pintar como texto.  
- [TIA pone `Foto de Sala Aire` otra vez] → El prompt dice no repetir el nombre en el link.  
- [Solo existe foto, no video] → Un solo link `foto`; no inventar recorrido.

## Migration Plan

Editar parser + prompt + nota `# SALONES` + tests. Hard refresh de la UI. Rollback: revertir esos archivos; los MP4/JPG no se tocan.

## Open Questions

Ninguna. Copy A cerrada con el usuario.
