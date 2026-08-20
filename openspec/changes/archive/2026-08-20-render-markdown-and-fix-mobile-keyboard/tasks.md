## 1. Layout móvil (teclado)

- [x] 1.1 Fijar `html/body` a `100dvh`, `overflow: hidden`; header/footer `flex-shrink: 0`; `#chat` con `flex: 1; min-height: 0; overflow-y: auto`
- [x] 1.2 Añadir `interactive-widget=resizes-content` al meta viewport
- [x] 1.3 Listener de `visualViewport` (alto visible + scroll al final) al resize, al focus del input y tras `appendBubble` (incl. delay corto para iOS)

## 2. Markdown subset

- [x] 2.1 Parser en `index.html`: párrafos, `**negrita**`, listas `-`/`*`/`1.`, autolink `http(s)://`; DOM con `createElement`/`textContent`; sin `innerHTML` del reply
- [x] 2.2 `appendBubble`: bot usa el parser; user/system siguen en texto plano; CSS de `.bubble.bot` para `p/ul/ol/a/strong` (sin `pre-wrap` en bot)
- [x] 2.3 Links con `target="_blank"` y `rel="noopener noreferrer"`

## 3. Tests y rule

- [x] 3.1 Tests de GET `/`: viewport meta, `visualViewport`, `min-height: 0`, presencia del renderer y ausencia de `innerHTML` sobre el reply
- [x] 3.2 Actualizar `.cursor/rules/static-chat-ui.mdc` (shell de viewport + no `innerHTML` del mensaje)
