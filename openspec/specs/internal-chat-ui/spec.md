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
