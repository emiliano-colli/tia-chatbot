## ADDED Requirements

### Requirement: Assistant bubbles render a safe Markdown subset
Las burbujas del asistente MUST mostrar un subset de Markdown de forma legible: párrafos/saltos de línea, negrita `**texto**`, listas con `- ` / `* ` o `1. `, y URLs `http://` / `https://` como enlaces. MUST construir el DOM con nodos y `textContent` (o equivalente que no interprete HTML del modelo). MUST NOT asignar el reply crudo a `innerHTML`. Las burbujas de usuario y de sistema MUST seguir como texto plano. MUST NOT cargar librerías Markdown ni sanitizers por CDN.

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

### Requirement: Chat shell stays in the visual viewport when the mobile keyboard opens
La página de chat MUST usar un layout de columna a la altura del viewport (`100dvh` / alto visible) con `overflow` del documento oculto. Header y footer/composer MUST permanecer visibles (no scrollearse fuera con la página). `#chat` MUST ser la única región con scroll vertical (`min-height: 0`). Al abrir el teclado en pantalla, al enfocar el input y al agregar una burbuja, la última burbuja MUST quedar en el área visible de `#chat` (p. ej. `visualViewport` + scroll al final). MUST NOT depender de un framework CSS.

#### Scenario: Last bubble remains visible after typing on a phone
- **WHEN** el usuario enfoca el campo de mensaje en un viewport estrecho y se abre el teclado en pantalla
- **THEN** el título permanece en pantalla y la última burbuja del historial sigue visible encima del composer, no oculta detrás del teclado ni fuera del scroll del documento

#### Scenario: Chat region is the only vertical scroller
- **WHEN** hay más mensajes de los que caben entre header y footer
- **THEN** el usuario scrollea el historial dentro de `#chat` sin desplazar header y composer con el documento
