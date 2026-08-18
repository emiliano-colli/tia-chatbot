## ADDED Requirements

### Requirement: Header tagline lists main offerings
The internal chat page header MUST show the subtitle `Preguntame sobre clases de yoga, entrenamiento funcional, talleres, servicios de salud, bienestar y más 🌿`. MUST NOT keep the previous shorter tagline that only mentioned talleres and servicios.

#### Scenario: Root HTML includes expanded tagline
- **WHEN** a client requests `GET /`
- **THEN** the HTML contains `Preguntame sobre clases de yoga, entrenamiento funcional, talleres, servicios de salud, bienestar y más 🌿`

### Requirement: Chat page is usable on a narrow viewport
The chat page MUST present title, subtitle, new-conversation control, message input and send control without requiring horizontal panning on a typical phone viewport (~360px wide). Text MUST wrap; header and footer controls MUST remain reachable in the layout.

#### Scenario: Narrow viewport keeps chrome reachable
- **WHEN** the chat page is viewed at approximately 360px width
- **THEN** the title, subtitle, “Nueva consulta” control and send control are visible without horizontal scrolling
