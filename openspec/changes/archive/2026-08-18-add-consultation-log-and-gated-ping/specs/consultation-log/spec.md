## ADDED Requirements

### Requirement: Each consultation gets a correlative integer id
The system MUST assign a unique monotonically increasing integer consultation id on the first user message of a session. The browser/CLI session UUID MUST remain unchanged. The same integer MUST be reused for the rest of that session until it is closed.

#### Scenario: First message allocates next id
- **WHEN** a new session receives its first user message
- **THEN** the system assigns the next unused integer id and returns it to the client

#### Scenario: Later messages keep the same id
- **WHEN** the same session sends another message
- **THEN** the consultation id is unchanged

### Requirement: Closed consultations are appended to a CSV log
On every successful `end_session` (formal, timeout, or reset), the system MUST append one CSV row with at least: id, close datetime, name, phone, interest, origin, and close reason. Consultations without contact data MUST still be logged.

#### Scenario: Greeting-only session is logged
- **WHEN** a session that only contains a greeting is closed
- **THEN** a CSV row is written with that consultation id and empty/placeholder contact fields

#### Scenario: Contact session is logged
- **WHEN** a session with name or phone is closed
- **THEN** a CSV row is written including those fields and the consultation id

### Requirement: Consultation origin is recorded per channel
The system MUST store an origin value for each consultation. The web chat MUST use `web` and the CLI MUST use `cli`. The CSV `origen` column MUST keep that value so later social-network channels can reuse the same field.

#### Scenario: Web chat is tagged web
- **WHEN** a consultation started via `POST /chat` from the internal web UI is closed
- **THEN** the CSV origin field is `web`

#### Scenario: CLI chat is tagged cli
- **WHEN** a consultation started from the CLI is closed
- **THEN** the CSV origin field is `cli`

### Requirement: Consultation id is shown discreetly to the user
The web chat UI MUST display the consultation id in a small, low-emphasis control once it is known (for example `#12` in muted type). MUST NOT present it as a primary heading or system bubble. The CLI MUST print the id once when it is assigned.

#### Scenario: Web UI shows muted id after first reply
- **WHEN** the web client receives a `consulta_id` from `POST /chat`
- **THEN** a compact muted label with that id is visible in the page chrome
