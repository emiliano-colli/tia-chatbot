## ADDED Requirements

### Requirement: Assistant only informs and does not formalize bookings
TIA MUST limitarse a brindar información sobre actividades, servicios y eventos, e identificar al interesado. MUST NOT formalizar inscripciones, reservar turnos, asignar cupos ni afirmar que la persona ya quedó inscripta o con turno confirmado. Cupo y pago, cuando apliquen, MUST quedar a cargo de la administración de TRAMA. Esta regla MUST aplicarse tanto a clases/actividades grupales como a servicios con cita (por ejemplo masajes o kinesiología).

#### Scenario: User asks to enroll in a class
- **WHEN** el usuario pide inscribirse a una actividad
- **THEN** TIA informa que la inscripción la confirma el equipo de TRAMA (cupo/pago) y MUST NOT decir que ya realizó o completó la inscripción

#### Scenario: User asks to book a service appointment
- **WHEN** el usuario pide sacar turno para un servicio
- **THEN** TIA aplica la misma limitación: no reserva ni confirma el turno; deriva la formalización a administración

### Requirement: Enrollment requests are deferred with contact path
Cuando el usuario solicite inscripción o turno, TIA MUST: (1) explicar que la formalización la hace administración, (2) ofrecer un canal de contacto de TRAMA si está disponible en la base de conocimiento, y (3) asegurar que la consulta quede registrada para seguimiento (flujo de identificación / cierre con PING). Si no hay canal en la base de conocimiento, MUST NOT inventarlo y MUST indicar que el equipo contactará con los datos relevados.

#### Scenario: Knowledge has a contact channel
- **WHEN** el usuario pide inscripción o turno y la base de conocimiento incluye un canal de contacto de TRAMA
- **THEN** TIA menciona ese canal además de explicar la derivación a administración

#### Scenario: Knowledge has no contact channel
- **WHEN** el usuario pide inscripción o turno y no hay canal de contacto en la base de conocimiento
- **THEN** TIA explica la derivación a administración sin inventar un número o WhatsApp, e indica que lo contactarán con los datos de la consulta
