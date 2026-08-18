## ADDED Requirements

### Requirement: Knowledge documents WhatsApp as primary public contact
La base de conocimiento MUST documentar el WhatsApp de consultas de TRAMA como canal público **prioritario** para inscripción y turnos, con el número `+54 11 6956-6115` y el horario **lunes a viernes de 09 a 21 hs**. MUST NOT afirmar que no hay WhatsApp ni teléfono de consultas si esos datos están cargados. Instagram y Facebook MAY permanecer como canales secundarios en la sección de redes.

#### Scenario: Contact block lists WhatsApp first with hours
- **WHEN** se lee el bloque de contacto para inscripción/turnos en knowledge
- **THEN** aparece el WhatsApp de consultas con el número y el horario lunes–viernes 09–21, y no el texto de que no hay WhatsApp

#### Scenario: Social networks remain documented
- **WHEN** se consulta la sección de redes
- **THEN** siguen figurando Instagram y Facebook de TRAMA (y Maternar si aplica), sin reemplazar al WhatsApp como canal prioritario de inscripción/turnos

## MODIFIED Requirements

### Requirement: Service booking copy defers formalization to TRAMA team
En fichas de servicios con cita, el texto de reserva en knowledge MUST indicar que la formalización del turno la coordina el equipo de TRAMA, MUST citar el canal público **prioritario** documentado (WhatsApp de consultas con número y horario cuando estén en la base), MUST NOT instruir a “coordinar directamente” el cierre del turno solo con la profesional como sustituto de ese flujo, y MAY nombrar a las profesionales como quienes atienden / cuya agenda se acuerda vía el equipo. MUST NOT dejar como único canal público las redes si el WhatsApp de consultas está cargado.

#### Scenario: Massage reservation wording avoids direct booking shortcut
- **WHEN** se lee el bloque de disponibilidad/reserva o copy de reserva de Masajes
- **THEN** no indica al lector que cierre el turno coordinando directamente con la profesional al margen del equipo/canal documentado

#### Scenario: Massage formalization cites WhatsApp
- **WHEN** se lee el bloque de formalización de Masajes
- **THEN** el canal público citado es el WhatsApp de consultas (número y horario de la base), no solo Instagram/Facebook
