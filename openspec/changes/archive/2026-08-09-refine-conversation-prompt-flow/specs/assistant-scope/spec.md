## MODIFIED Requirements

### Requirement: Enrollment requests are deferred with contact path
Cuando el usuario solicite inscripción o turno, TIA MUST: (1) aportar información útil disponible sobre el servicio/actividad sin inventar datos faltantes, (2) explicar que la formalización la hace administración, (3) ofrecer un canal de contacto de TRAMA si está disponible en la base de conocimiento (por ejemplo redes oficiales), y (4) asegurar que la consulta quede para seguimiento (identificación / cierre con PING). Si no hay canal en la base de conocimiento, MUST NOT inventarlo y MUST indicar que el equipo contactará con los datos relevados.

#### Scenario: Knowledge has a contact channel
- **WHEN** el usuario pide inscripción o turno y la base de conocimiento incluye un canal de contacto de TRAMA
- **THEN** TIA menciona ese canal además de explicar la derivación a administración

#### Scenario: Knowledge has no contact channel
- **WHEN** el usuario pide inscripción o turno y no hay canal de contacto en la base de conocimiento
- **THEN** TIA explica la derivación a administración sin inventar un número o WhatsApp, e indica que lo contactarán con los datos de la consulta

#### Scenario: Deferral still provides available information
- **WHEN** el usuario pide turno o inscripción
- **THEN** TIA no se limita solo al aviso de formalización: comparte la información disponible en knowledge o declara con honestidad si falta un dato
