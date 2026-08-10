## MODIFIED Requirements

### Requirement: System prompt mandates real datetime for temporal answers
El prompt de sistema MUST instruir al asistente a usar la fecha actual (vía la tool) para interpretar “hoy”, “mañana”, “esta semana” y referencias temporales similares (incluyendo typos obvios), MUST prohibir inventar la fecha, y MUST indicar que la respuesta verbalice el día/fecha concreta obtenida.

#### Scenario: Prompt contains temporal tool guidance
- **WHEN** se carga el system prompt
- **THEN** incluye instrucciones para usar la fecha actual en interpretaciones temporales y no inventar la fecha

#### Scenario: Prompt requires stating the concrete day
- **WHEN** se carga el system prompt
- **THEN** indica que, tras usar la tool, se debe expresar el día o fecha concreta (por ejemplo al interpretar “mañana”)
