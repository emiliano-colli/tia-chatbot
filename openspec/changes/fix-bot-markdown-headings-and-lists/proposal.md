## Why

El subset Markdown de las burbujas bot todavía deja `###` a la vista en títulos de actividad, y las listas numeradas se ven todas como `1.` porque TIA (o el parser) arranca un `<ol>` nuevo en cada ítem. Hay que tratar headings y listas como bloques reales para que se lean bien.

## What Changes

- Interpretar líneas `#` / `##` / `###` (hasta 6): quitar los numerales y mostrar el título con un estilo de sección (viñeta/marca + negrita), no como `h1` de página.
- Unir ítems `1.` / `2.` (y viñetas `-`) en **una sola lista** aunque haya renglones vacíos entre ellos, para que el navegador numere 1, 2, 3.
- Seguir sin `innerHTML` del reply, sin CDN y sin cambiar el prompt.

## Capabilities

### New Capabilities

- Ninguna.

### Modified Capabilities

- `internal-chat-ui`: el subset Markdown MUST incluir headings (sin mostrar `#`) y MUST numerar las listas ordenadas de forma consecutiva aunque el modelo repita `1.` o deje líneas en blanco entre ítems.

## Impact

- `app/static/index.html` (`renderBotMarkdown` + CSS de heading en `.bubble.bot`)
- Tests de GET `/` si conviene anclar tokens del parser (`isHeading`, `ol`)
- Spec `internal-chat-ui`
- Sin API, prompt ni dependencias
