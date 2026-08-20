## MODIFIED Requirements

### Requirement: Assistant bubbles render a safe Markdown subset
Las burbujas del asistente MUST mostrar un subset de Markdown de forma legible: párrafos/saltos de línea, negrita `**texto**`, headings `#`–`######` (sin mostrar los numerales; con marca de sección tipo viñeta), listas con `- ` / `* ` o `1. `, y URLs `http://` / `https://` como enlaces. Ítems de una lista ordenada MUST numerarse en secuencia (1, 2, 3…) en un solo listado aunque el texto source repita `1.` o deje líneas en blanco entre ítems. MUST construir el DOM con nodos y `textContent` (o equivalente que no interprete HTML del modelo). MUST NOT asignar el reply crudo a `innerHTML`. Las burbujas de usuario y de sistema MUST seguir como texto plano. MUST NOT cargar librerías Markdown ni sanitizers por CDN.

#### Scenario: Bot reply shows bold and a list
- **WHEN** el asistente responde con negrita Markdown y una lista con viñetas
- **THEN** la burbuja bot muestra negrita y una lista HTML, no los marcadores crudos `**` y `- ` como único formato visible

#### Scenario: Bot reply autolinks https URLs
- **WHEN** el reply del asistente incluye una URL `https://`
- **THEN** esa URL se muestra como enlace visitables (p. ej. `target="_blank"`)

#### Scenario: User bubble stays plain text
- **WHEN** el usuario envía un mensaje que contiene `**asteriscos**`
- **THEN** la burbuja de usuario muestra el texto literal, sin convertirlo a negrita

#### Scenario: Raw HTML in the reply is not executed
- **WHEN** el reply del asistente contiene etiquetas HTML (p. ej. `<script>` o `<img>`)
- **THEN** esas etiquetas se muestran como texto o se escapan; MUST NOT ejecutarse como HTML

#### Scenario: Heading hashes are not shown
- **WHEN** el reply del asistente incluye una línea `### Descripción` (u otro heading `#`–`######`)
- **THEN** la burbuja muestra el título de sección sin los caracteres `#`, con un estilo distinto al párrafo (p. ej. viñeta + negrita)

#### Scenario: Repeated 1. items become a single numbered list
- **WHEN** el reply lista varias opciones cada una con `1.` y/o con una línea vacía entre ítems
- **THEN** la burbuja muestra una sola lista ordenada con numeración consecutiva (1, 2, 3…), no varios listados que arrancan todos en 1
