## ADDED Requirements

### Requirement: Professional WhatsApp from a service fiche is cited in addition to TRAMA
Cuando el usuario consulta o pide turno de un servicio cuya ficha en knowledge lista un WhatsApp de profesional (número y cuándo usarlo), TIA MUST pegar ese número **además** del WhatsApp de consultas de TRAMA. MUST NOT omitir el de la profesional porque el canal general sea “prioritario”. MUST NOT omitir el 6115 porque exista el de la profesional. MUST NOT inventar WhatsApp o teléfonos que no figuren en knowledge. MUST NOT afirmar que TIA ya coordinó o confirmó el turno con esa profesional.

#### Scenario: User asks about lactancia on a Natalia day
- **WHEN** el usuario pregunta por Consultorio de Lactancia o pide turno en martes, jueves o viernes
- **THEN** TIA cita el WhatsApp de Natalia documentado y también el de TRAMA (6115)

#### Scenario: User asks about lactancia without a specific day
- **WHEN** el usuario pregunta por lactancia sin indicar día
- **THEN** TIA explica la grilla, cita ambos canales según la ficha (Natalia en sus días; Carolina/TRAMA miércoles y consultas generales) y MUST NOT dar solo uno de los dos números

#### Scenario: Numbers not in knowledge are not invented
- **WHEN** el usuario pide el celular de una profesional que no tiene WhatsApp en la ficha (p. ej. Gaby en masajes)
- **THEN** TIA no inventa un número y deriva al WhatsApp de consultas TRAMA si está en la base

## MODIFIED Requirements

### Requirement: Enrollment requests are deferred with contact path
Cuando el usuario solicite inscripción o turno, TIA MUST: (1) aportar información útil disponible sobre el servicio/actividad sin inventar datos faltantes —incluyendo, para servicios con cita, tipos, precio, seña, duración o sala si están en knowledge—, (2) explicar que la formalización la hace administración / equipo de TRAMA, (3) ofrecer un canal de contacto de TRAMA si está disponible en la base de conocimiento, **priorizando el WhatsApp de consultas (número y horario) cuando figuren**, y las redes oficiales solo como complemento con el dato concreto de la base, (4) si la ficha del servicio declara WhatsApp de una profesional, citarlo **además** de ese canal TRAMA (no en su lugar), y (5) asegurar que la consulta quede para seguimiento (identificación / cierre con PING). Si no hay canal en la base de conocimiento, MUST NOT inventarlo y MUST indicar que el equipo contactará con los datos relevados. MUST NOT afirmar que no hay WhatsApp cuando el número está en knowledge. MUST NOT presentar el cierre del turno como una coordinación directa usuario–profesional **sustituyendo** ese flujo.

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

#### Scenario: Service fiche professional WhatsApp is additional
- **WHEN** el usuario pide turno de un servicio cuya ficha lista WhatsApp de profesional
- **THEN** TIA cita ese número además del WhatsApp de consultas TRAMA y MUST NOT presentar a la profesional como único canal de cierre
