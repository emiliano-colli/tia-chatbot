# internal-chat-ui

## Purpose

UI web estática servida por FastAPI para que testers internos chateen en paralelo con TIA, cada browser con su propio `session_id`, sin Gradio ni autenticación en esta iteración.

## Requirements

### Requirement: Internal chat page is served at root
The application MUST expose a browser chat UI at `GET /` on the same FastAPI app that serves `/chat`, so internal testers can use one URL without a separate Gradio process.

#### Scenario: Root returns chat page
- **WHEN** a client requests `GET /`
- **THEN** the response is an HTML chat page suitable for sending messages to TIA

### Requirement: Each browser gets an independent session id
The chat UI MUST assign a unique session identifier per browser profile using `localStorage` (key `tia_session_id`), generating a new UUID when absent, and MUST send that id on every `POST /chat` request.

#### Scenario: Two browsers chat in parallel
- **WHEN** two browsers each load `/` and send messages
- **THEN** they use different session ids and do not share conversation history on the server

#### Scenario: Reload keeps server session
- **WHEN** a user reloads the page without clearing storage
- **THEN** the same `tia_session_id` is reused for subsequent messages

### Requirement: Minimal in-page history without persistence
The UI MUST show user and assistant messages for the current page visit only in memory (DOM/JS). It MUST NOT persist message bubbles in `localStorage`. A full page reload MAY show an empty message area while the server session remains if the session id was preserved.

#### Scenario: Reload clears visible history
- **WHEN** the user reloads the page
- **THEN** the on-screen message list is empty even if the session id in storage is unchanged

### Requirement: Branding uses locally served logo
The chat page MUST display TRAMA branding using a logo asset served from `/static/` on the same host. It MUST NOT depend on a hotlinked external CDN URL at runtime.

#### Scenario: Logo loads from static path
- **WHEN** the chat page is rendered
- **THEN** the logo image source is a path under `/static/` on the application origin

### Requirement: New conversation control
The UI MUST offer a way to start a fresh conversation (e.g. “Nueva consulta”) that calls `POST /end/{session_id}` when a session exists, clears `tia_session_id` from storage, and resets the visible chat.

#### Scenario: User starts new conversation
- **WHEN** the user activates the new-conversation control
- **THEN** the current session is ended via the API when applicable, storage is cleared, and the UI is reset

### Requirement: Farewell clears client session
After a successful farewell response from the chat flow, the UI MUST clear `tia_session_id` and the visible messages, and indicate that the user may write again to start a new conversation.

#### Scenario: User says farewell
- **WHEN** the user sends a recognized farewell phrase and receives the farewell reply
- **THEN** local session storage is cleared and the chat area is reset for a new conversation

### Requirement: Chat page shows consultation id discreetly
After the first successful `POST /chat` of a session, the internal chat page MUST display the returned `consulta_id` in a compact muted label in the page chrome (header or toolbar). MUST NOT use a chat bubble or a heading for that id.

#### Scenario: Id label appears after first reply
- **WHEN** the web client receives a numeric `consulta_id` in the chat response
- **THEN** a small muted `#` + id label is visible without requiring horizontal pan on a phone viewport

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

### Requirement: Chat shell stays in the visual viewport when the mobile keyboard opens
La página de chat MUST usar un layout de columna a la altura del viewport (`100dvh` / alto visible) con `overflow` del documento oculto. Header y footer/composer MUST permanecer visibles (no scrollearse fuera con la página). `#chat` MUST ser la única región con scroll vertical (`min-height: 0`). Al abrir el teclado en pantalla, al enfocar el input y al agregar una burbuja, la última burbuja MUST quedar en el área visible de `#chat` (p. ej. `visualViewport` + scroll al final). MUST NOT depender de un framework CSS.

#### Scenario: Last bubble remains visible after typing on a phone
- **WHEN** el usuario enfoca el campo de mensaje en un viewport estrecho y se abre el teclado en pantalla
- **THEN** el título permanece en pantalla y la última burbuja del historial sigue visible encima del composer, no oculta detrás del teclado ni fuera del scroll del documento

#### Scenario: Chat region is the only vertical scroller
- **WHEN** hay más mensajes de los que caben entre header y footer
- **THEN** el usuario scrollea el historial dentro de `#chat` sin desplazar header y composer con el documento
