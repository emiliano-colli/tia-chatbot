## MODIFIED Requirements

### Requirement: Enrollment requests are deferred with contact path
Cuando el usuario solicite inscripción o turno, TIA MUST: (1) aportar información útil disponible sobre el servicio/actividad sin inventar datos faltantes —incluyendo, para servicios con cita, tipos, precio, seña, duración o sala si están en knowledge, y si `# SALONES` tiene Foto y/o Video de esa sala, la plantilla `foto · recorrido` aunque el usuario no haya preguntado por el lugar—, (2) explicar que la formalización la hace administración / equipo de TRAMA, (3) ofrecer un canal de contacto de TRAMA si está disponible en la base de conocimiento, **priorizando el WhatsApp de consultas (número y horario) cuando figuren**, y las redes oficiales solo como complemento con el dato concreto de la base, y (4) asegurar que la consulta quede para seguimiento (identificación / cierre con PING). Si no hay canal en la base de conocimiento, MUST NOT inventarlo y MUST indicar que el equipo contactará con los datos relevados. MUST NOT afirmar que no hay WhatsApp cuando el número está en knowledge. MUST NOT presentar el cierre del turno como una coordinación directa usuario–profesional sustituyendo ese flujo.

#### Scenario: Knowledge has WhatsApp as primary contact
- **WHEN** el usuario pide inscripción o turno y la base incluye el WhatsApp de consultas
- **THEN** TIA menciona ese WhatsApp (número y horario documentados) además de explicar la derivación a administración, y MUST NOT decir que el único canal son las redes

#### Scenario: Knowledge has a contact channel
- **WHEN** el usuario pide inscripción o turno y la base de conocimiento incluye un canal de contacto de TRAMA
- **THEN** TIA menciona ese canal además de explicar la derivación a administración

#### Scenario: Knowledge has no contact channel
- **WHEN** el usuario pide inscripción o turno y no hay canal de contacto en la base de conocimiento
- **THEN** TIA explica la derivación a administración sin inventar un número o WhatsApp, e indica que lo contactarán con los datos de la consulta

#### Scenario: Deferral still provides available information
- **WHEN** el usuario pide turno o inscripción
- **THEN** TIA no se limita solo al aviso de formalización: comparte la información disponible en knowledge o declara con honestidad si falta un dato

#### Scenario: Service inquiry includes price and deposit when known
- **WHEN** el usuario pregunta por precios o turnos de un servicio (p. ej. masajes) y knowledge tiene precio y seña
- **THEN** TIA menciona esos datos además de derivar la formalización, y MUST NOT omitirlos solo porque no haya grilla horaria fija

#### Scenario: Massage info includes Calma and media without asking where
- **WHEN** el usuario pregunta por masajes (tipos, precio o turno) y no pregunta por el salón, y knowledge tiene Lugar Sala Calma con Foto y Video
- **THEN** TIA nombra Sala Calma y pega `foto · recorrido` (paths de `# SALONES`) además de tipos/precio/seña; MUST NOT omitirlos porque la pregunta no fue “dónde”
