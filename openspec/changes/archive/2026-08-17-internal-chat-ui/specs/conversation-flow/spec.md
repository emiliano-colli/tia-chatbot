## ADDED Requirements

### Requirement: Farewell messages close session inside ask
When `TiaChatbot.ask()` receives a user message that matches the centralized farewell detection (`is_session_end_message`), the system MUST call `end_session` for that session id (triggering admin PING when configured), MUST NOT send the farewell text to the LLM as a normal turn, and MUST return a fixed farewell reply to the caller.

#### Scenario: Chat API receives farewell
- **WHEN** `POST /chat` receives a body whose message is a recognized farewell phrase
- **THEN** the session is ended once, the response is the standard farewell text, and no LLM completion is required for that turn

#### Scenario: Farewell after prior messages
- **WHEN** the user had an active conversation and then sends a farewell-only message
- **THEN** the farewell closes the session and the PING reflects the prior dialogue

#### Scenario: Non-farewell messages unchanged
- **WHEN** the user message is not a recognized farewell
- **THEN** `ask()` proceeds with the normal LLM flow
