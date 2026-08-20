## Context

`app/static/index.html` es un solo archivo, sin framework. Las burbujas usan `textContent` + `white-space: pre-wrap`: seguro, pero el Markdown de TIA se ve crudo. El layout ya es header / `#chat` flex / footer, pero `min-height: 100dvh` deja scrollear el documento; al focus del input el browser empuja la página y en iOS el teclado no achica el layout viewport.

Constraint del repo: sin librerías nuevas ni CDN de runtime (el logo ya es local). XSS: hoy no hay `innerHTML` del reply.

## Goals / Non-Goals

**Goals:**
- Bot: negrita, listas, párrafos y links `https://` legibles.
- Usuario/sistema: texto plano.
- Header y composer fijos en el viewport visible; solo `#chat` scrollea; última burbuja a la vista al enviar, al recibir y al abrir el teclado.

**Non-Goals:**
- Markdown completo (tablas, HTML crudo, imágenes, headings).
- `marked` / `DOMPurify` / React.
- Renderizar HTML en el API o cambiar el prompt.
- Gradio.
- Garantía pixel-perfect en todos los WebViews de Instagram (se prueba Chrome Android + Safari iOS).

## Decisions

1. **Subset en el mismo HTML, solo `.bot`**  
   Parser pequeño + `document.createElement` / `textContent` en cada nodo. Autolink solo `https://` (y `http://`).  
   Rationale: cero deps, XSS acotado.  
   Alternativa CDN marked+DOMPurify: más MD, dos scripts externos, choca con “no CDN”.  
   Alternativa HTML en FastAPI: rompe CLI/PING y el contrato `reply: str`.

2. **Nunca `innerHTML` del reply crudo**  
   Ni `insertAdjacentHTML`. Lo no reconocido queda texto.  
   `**negrita**` en línea; bloques: líneas que empiezan con `- ` / `* ` → `<ul>`; `1. ` → `<ol>`; el resto → `<p>` o `<br>` entre párrafos.  
   Links: `target="_blank"` `rel="noopener noreferrer"`.  
   Quitar `pre-wrap` en `.bot` para que las listas no hereden espacios literales.

3. **Shell de viewport, no `position: fixed`**  
   - `html, body { height: 100%; height: 100dvh; overflow: hidden }`  
   - header/footer `flex-shrink: 0`  
   - `#chat { flex: 1; min-height: 0; overflow-y: auto }`  
   - meta: `interactive-widget=resizes-content` (Chrome Android).  
   Rationale: el flex ya existe; el bug es que el documento scrollea. Fixed es más frágil con safe-area.

4. **`visualViewport` + scroll de la última burbuja**  
   En `resize`/`scroll` de `visualViewport`: alinear `body` al alto visible (o padding inferior) y `scrollTop = scrollHeight` (o `scrollIntoView` del último `.bubble`). Repetir al `focus` del input y tras `appendBubble`, con un rAF o timeout corto (~250 ms) por la animación del teclado iOS.  
   Rationale: iOS ignora `interactive-widget`.  
   Alternativa solo CSS: insuficiente en Safari.

5. **Tests de string sobre el HTML**  
   Pytest no abre teclado real: assert de meta viewport, `visualViewport`, `min-height: 0`, función de render, y que no haya `innerHTML =` sobre el reply. Smoke de subset: un comentario o un helper testeable si se extrae; si queda inline, buscar tokens (`createElement`, `**`) en el archivo.

6. **Cursor rule**  
   Ampliar `static-chat-ui.mdc`: body no scrollea; `#chat` tiene `min-height: 0`; no pintar el reply con `innerHTML`.

## Risks / Trade-offs

- [MD raro (`***`, nested lists) queda feo] → Aceptado; fallback texto.  
- [XSS si alguien usa innerHTML “por apuro”] → Rule + review; solo createElement.  
- [iOS sigue tapando] → visualViewport + delay; probar en device.  
- [Toolbar del footer come alto con teclado] → ya está compacto en 480px; no esconder “Nueva consulta”.  
- [`interactive-widget` desconocido en browsers viejos] → se ignora; queda visualViewport.

## Migration Plan

1. Editar `index.html` + rule + tests de GET `/`.  
2. Probar desktop, Chrome Android, Safari iOS (teclado + un reply con lista y `**` + link wa.me).  
3. Restart no hace falta para estáticos si el archivo se sirve fresco; Ctrl+F5 en clientes.

Rollback: revertir `index.html`.

## Open Questions

Ninguna bloqueante. Headings `#` fuera de este corte; se agregan si TIA los usa mucho en staging.
