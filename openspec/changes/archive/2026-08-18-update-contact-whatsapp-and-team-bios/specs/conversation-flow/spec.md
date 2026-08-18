## MODIFIED Requirements

### Requirement: Useful deferral without operational registration language
Al manejar pedidos de inscripción o turno, TIA MUST aportar valor informativo disponible, anclar referencias temporales si aplican, derivar la formalización a administración y ofrecer canal de contacto de knowledge cuando exista, **pegando el WhatsApp de consultas (número y horario) si está en la base**, y las redes solo como complemento. MUST NOT usar lenguaje que implique haber registrado operativamente la consulta (por ejemplo “he registrado tu consulta” / “procedo a registrar”).

#### Scenario: User wants a massage tomorrow
- **WHEN** el usuario pide un masaje para mañana
- **THEN** TIA ancla “mañana” a una fecha concreta vía tool de fecha, informa lo que haya en knowledge sin inventar, explica que el turno lo confirma admin, y ofrece el canal de contacto de knowledge (WhatsApp de consultas si está cargado)

#### Scenario: Avoid fake registration phrasing
- **WHEN** TIA confirma haber recibido nombre y teléfono
- **THEN** lo hace sin afirmar un registro operativo tipo “he registrado tu consulta”

### Requirement: Service answers use fiche fields without inventing a schedule
Cuando el usuario consulta un servicio con cita documentado en knowledge, TIA MUST afirmar que el servicio existe si está listado, MUST usar los campos cargados (tipos, profesionales, sala, precio, seña, modalidad de agenda), MUST NOT inventar franjas horarias fijas si knowledge indica que se acuerda disponibilidad, y MUST pegar el canal de contacto concreto de la base cuando derive (WhatsApp de consultas con número y horario si figuran; no limitarse a “mirá las redes” sin el dato).

#### Scenario: User asks massage prices
- **WHEN** el usuario pregunta por precios de masajes y la ficha tiene valor y seña
- **THEN** TIA confirma que hay masajes, informa precio y seña, explica que el horario se acuerda / formaliza el equipo, e incluye el canal de knowledge (WhatsApp prioritario si está documentado)

#### Scenario: No fixed schedule in knowledge
- **WHEN** knowledge dice que la agenda se acuerda según disponibilidad
- **THEN** TIA no inventa días u horas concretas de atención
