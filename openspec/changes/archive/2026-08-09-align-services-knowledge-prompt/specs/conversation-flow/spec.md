## ADDED Requirements

### Requirement: Service answers use fiche fields without inventing a schedule
Cuando el usuario consulta un servicio con cita documentado en knowledge, TIA MUST afirmar que el servicio existe si está listado, MUST usar los campos cargados (tipos, profesionales, sala, precio, seña, modalidad de agenda), MUST NOT inventar franjas horarias fijas si knowledge indica que se acuerda disponibilidad, y MUST pegar el canal de contacto concreto de la base cuando derive a redes.

#### Scenario: User asks massage prices
- **WHEN** el usuario pregunta por precios de masajes y la ficha tiene valor y seña
- **THEN** TIA confirma que hay masajes, informa precio y seña, explica que el horario se acuerda / formaliza el equipo, e incluye el canal de knowledge si ofrece redes

#### Scenario: No fixed schedule in knowledge
- **WHEN** knowledge dice que la agenda se acuerda según disponibilidad
- **THEN** TIA no inventa días u horas concretas de atención
