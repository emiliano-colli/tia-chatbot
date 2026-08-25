## MODIFIED Requirements

### Requirement: Assistant bubbles render a safe Markdown subset
Las burbujas del asistente MUST mostrar un subset de Markdown de forma legible: párrafos/saltos de línea, negrita `**texto**`, headings `#`–`######` (sin mostrar los numerales; con marca de sección tipo viñeta), listas con `- ` / `* `, líneas que empiezan con `1. ` / `2. ` como **títulos de bloque con viñeta** (no como lista ordenada HTML), URLs `http://` / `https://` **y paths del mismo origen `/static/…`** como enlaces, y enlaces Markdown `[label](href)` cuyo **texto visible es el `label`**. El `href` de un `[label](href)` MUST aceptarse solo si es `http://`, `https://` o un path que empieza con `/static/`; cualquier otro esquema MUST quedar como texto plano. MUST NOT usar `<ol>` (marcadores 1, 2, 3 del navegador) para esas líneas numeradas. Si después de un `1.` vienen viñetas `-`, MUST mostrarlas como sublista indentada de ese bloque. MUST construir el DOM con nodos y `textContent`. MUST NOT asignar el reply crudo a `innerHTML`. Las burbujas de usuario y de sistema MUST seguir como texto plano. MUST NOT cargar librerías Markdown ni sanitizers por CDN.

#### Scenario: Bot reply shows bold and a list
- **WHEN** el asistente responde con negrita Markdown y una lista con viñetas
- **THEN** la burbuja bot muestra negrita y una lista HTML, no los marcadores crudos `**` y `- ` como único formato visible

#### Scenario: Bot reply autolinks https URLs
- **WHEN** el reply del asistente incluye una URL `https://`
- **THEN** esa URL se muestra como enlace visitables (p. ej. `target="_blank"`)

#### Scenario: Bot reply autolinks same-origin static paths
- **WHEN** el reply del asistente incluye un path `/static/salones/tierra.jpg` (u otro archivo bajo `/static/`)
- **THEN** ese path se muestra como enlace visitable en el mismo origen (p. ej. `target="_blank"`)

#### Scenario: Bot reply shows markdown link labels
- **WHEN** el reply incluye `[foto](/static/salones/aire.jpg) · [recorrido](/static/salones/aire.mp4)`
- **THEN** la burbuja muestra dos enlaces cuyo texto visible es `foto` y `recorrido` (no las rutas), con `href` a esos paths, `target="_blank"`

#### Scenario: Unsafe markdown href stays plain text
- **WHEN** el reply incluye `[x](javascript:alert(1))` u otro href que no es `http(s):` ni `/static/`
- **THEN** no se crea un enlace navegable a ese href; el fragmento se muestra como texto

#### Scenario: User bubble stays plain text
- **WHEN** el usuario envía un mensaje que contiene `**asteriscos**`
- **THEN** la burbuja de usuario muestra el texto literal, sin convertirlo a negrita

#### Scenario: Raw HTML in the reply is not executed
- **WHEN** el reply del asistente contiene etiquetas HTML (p. ej. `<script>` o `<img>`)
- **THEN** esas etiquetas se muestran como texto o se escapan; MUST NOT ejecutarse como HTML

#### Scenario: Heading hashes are not shown
- **WHEN** el reply del asistente incluye una línea `### Descripción` (u otro heading `#`–`######`)
- **THEN** la burbuja muestra el título de sección sin los caracteres `#`, con un estilo distinto al párrafo (p. ej. viñeta + negrita)

#### Scenario: Numbered class names are not fake ordered lists
- **WHEN** el reply lista varias actividades cada una con `1.` y debajo viñetas `- Horarios:` y días (patrón “tienen yoga”)
- **THEN** cada actividad se muestra con una viñeta de sección (no un `1.` de `<ol>` que se reinicia) y los horarios como sublista de esa actividad

#### Scenario: Consecutive 1. lines without nested dashes use bullets
- **WHEN** el reply tiene varias líneas `1.` seguidas (con o sin líneas en blanco) y no hay `<ol>`
- **THEN** se muestran como bloques con viñeta, no como una lista ordenada 1, 2, 3 del navegador
