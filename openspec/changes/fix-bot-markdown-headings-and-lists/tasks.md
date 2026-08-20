## 1. Parser

- [x] 1.1 Detectar headings `#{1,6}` antes que listas; renderizar `<p class="md-heading">` sin los `#`, con `appendInline`
- [x] 1.2 Al armar `ul`/`ol`, saltar líneas vacías y seguir el mismo listado; cortar solo ante heading, párrafo u otro tipo de lista

## 2. Estilo y tests

- [x] 2.1 CSS `.bubble.bot .md-heading` con `▸` (`::before`) y negrita, sin `<h1>`–`<h6>`
- [x] 2.2 Tests GET `/`: `md-heading` y que el consume de listas atraviese blancos
