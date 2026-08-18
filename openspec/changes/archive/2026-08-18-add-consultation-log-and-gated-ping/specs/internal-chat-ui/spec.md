## ADDED Requirements

### Requirement: Chat page shows consultation id discreetly
After the first successful `POST /chat` of a session, the internal chat page MUST display the returned `consulta_id` in a compact muted label in the page chrome (header or toolbar). MUST NOT use a chat bubble or a heading for that id.

#### Scenario: Id label appears after first reply
- **WHEN** the web client receives a numeric `consulta_id` in the chat response
- **THEN** a small muted `#` + id label is visible without requiring horizontal pan on a phone viewport
