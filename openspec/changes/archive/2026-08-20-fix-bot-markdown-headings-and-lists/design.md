## Context

`renderBotMarkdown` en `app/static/index.html` cubre negrita, listas pegadas y links. No parsea headings (`#`–`######`), así que `### Descripción` se ve con los numerales. Las listas ordenadas se cortan en cada línea en blanco: TIA suele poner `1.` en cada opción (o un renglón vacío entre ítems) y cada `<ol>` arranca otra vez en 1.

Constraint: mismo HTML, `createElement`/`textContent`, sin CDN.

## Goals / Non-Goals

**Goals:**
- Títulos `#`…`######` sin numerales, con marca de sección (viñeta/▸ + negrita).
- Varios `1.` (o `1.` / `2.`) con o sin líneas vacías = **un** `<ol>` numerado 1, 2, 3.
- Lo mismo para viñetas `-` / `*` separadas por blancos.

**Non-Goals:**
- Cambiar el prompt para que TIA no use `###` o `1.`.
- Markdown anidado, tablas, `h1` de página.
- Extraer el parser a un `.js` aparte (salvo que los tests lo pidan; con strings en GET `/` alcanza).

## Decisions

1. **Headings antes que listas**  
   `^#{1,6}\s+` → quitar hashes, un `<p class="md-heading">` con inline (`**`, links). CSS: `font-weight: 600`, `::before { content: "▸ "; color: var(--accent); }`. No usar `<h1>`–`<h6>` dentro de la burbuja (romperían la jerarquía de la página).  
   Rationale: el usuario pidió viñeta/similar, no un título de documento.  
   Alternativa `<h3>` estilizado: peor para a11y del chrome.

2. **Listas atraviesan líneas vacías**  
   Al consumir `ul`/`ol`, `skipBlanks` y seguir si la siguiente línea no vacía sigue siendo el mismo tipo de lista. Cortar ante heading, párrafo u otro tipo de lista.  
   El número del Markdown se ignora (`1.` repetido es normal en LLMs); el `<ol>` numera solo.  
   Rationale: un `<ol start="1">` por ítem es exactamente el bug.  
   Alternativa: `list-style: none` y pintar el dígito del MD — fallaría igual con todos `1.`.

3. **`## 1. Yoga prenatal` es heading, no ítem**  
   Porque el check de heading va primero. El texto visible queda `▸ 1. Yoga prenatal` (el “1.” es parte del nombre de la ficha en knowledge). Aceptable.

4. **Tests**  
   GET `/`: `md-heading`, `#{1,6}`, y que el loop de `ol` no exija líneas contiguas (token `trim() === ""` dentro del consume, o `skipBlanks` si existe).

## Risks / Trade-offs

- [Un `1.` suelto después de un párrafo se une al ol anterior si solo hay blancos] → Correcto para “opciones”; un heading en el medio corta.  
- [▸ + heading largo en 360px] → `overflow-wrap` ya está en `.bubble`.  
- [TIA escribe `#algo` sin espacio] → CommonMark exige espacio; no parsear, queda texto.

## Migration Plan

Editar `index.html` + tests. Hard refresh. Rollback: revertir el parser.

## Open Questions

Ninguna. Si el ▸ no convence en staging, se cambia el `content` del `::before` sin tocar el parser.
