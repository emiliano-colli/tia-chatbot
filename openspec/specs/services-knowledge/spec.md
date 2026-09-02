# services-knowledge

## Purpose

Contrato de estructura y contenido de la Agenda de Servicios en la base de conocimiento, y criterios para que el copy de reserva quede alineado al flujo del equipo TRAMA.

## Requirements

### Requirement: Services agenda uses a minimum service fiche template
La base de conocimiento MUST organizar `# AGENDA DE SERVICIOS` con ítems `## N. Nombre` cuya ficha mínima incluya: Descripción, Requisitos, Profesionales, Disponibilidad y reserva, y Valores. MUST NOT exigir la misma plantilla de horarios fijos que la Agenda de Actividades grupales. La numeración MAY reiniciar en 1 dentro de la agenda de servicios.

#### Scenario: Massage fiche follows the template
- **WHEN** se consulta la ficha de Masajes en la base de conocimiento
- **THEN** incluye los bloques mínimos de servicio (descripción, requisitos, profesionales, disponibilidad/reserva, valores)

### Requirement: Knowledge documents WhatsApp as primary public contact
La base de conocimiento MUST documentar el WhatsApp de consultas de TRAMA como canal público **prioritario** para inscripción y turnos, con el número `+54 11 6956-6115` y el horario **lunes a viernes de 09 a 21 hs**. MUST NOT afirmar que no hay WhatsApp ni teléfono de consultas si esos datos están cargados. Instagram y Facebook MAY permanecer como canales secundarios en la sección de redes.

#### Scenario: Contact block lists WhatsApp first with hours
- **WHEN** se lee el bloque de contacto para inscripción/turnos en knowledge
- **THEN** aparece el WhatsApp de consultas con el número y el horario lunes–viernes 09–21, y no el texto de que no hay WhatsApp

#### Scenario: Social networks remain documented
- **WHEN** se consulta la sección de redes
- **THEN** siguen figurando Instagram y Facebook de TRAMA (y Maternar si aplica), sin reemplazar al WhatsApp como canal prioritario de inscripción/turnos

### Requirement: Service booking copy defers formalization to TRAMA team
En fichas de servicios con cita, el texto de reserva en knowledge MUST indicar que la formalización del turno la coordina el equipo de TRAMA, MUST citar el canal público **prioritario** documentado (WhatsApp de consultas con número y horario cuando estén en la base), MUST NOT instruir a “coordinar directamente” el cierre del turno solo con la profesional como **sustituto** de ese flujo, y MAY nombrar a las profesionales como quienes atienden / cuya agenda se acuerda vía el equipo. Si la ficha declara WhatsApp de profesional, MUST citarlo como canal **adicional** (con los días o el contexto de la ficha), no como único canal. MUST NOT dejar como único canal público las redes si el WhatsApp de consultas está cargado.

#### Scenario: Massage reservation wording avoids direct booking shortcut
- **WHEN** se lee el bloque de disponibilidad/reserva o copy de reserva de Masajes
- **THEN** no indica al lector que cierre el turno coordinando directamente con la profesional al margen del equipo/canal documentado

#### Scenario: Massage formalization cites WhatsApp
- **WHEN** se lee el bloque de formalización de Masajes
- **THEN** el canal público citado es el WhatsApp de consultas (número y horario de la base), no solo Instagram/Facebook

#### Scenario: Lactancia additional WhatsApp does not replace TRAMA
- **WHEN** se lee Disponibilidad y reserva de Consultorio de Lactancia
- **THEN** el WhatsApp de Natalia aparece junto al de TRAMA, y el texto no presenta a Natalia como único canal de cierre del turno

### Requirement: Loaded service operational facts are present when known
Si un servicio tiene precio, seña, duración, sala o tipos cargados en knowledge, esos datos MUST figurar en la ficha bajo los bloques correspondientes (p. ej. seña junto a Valores) de forma explícita para que el asistente pueda citarlos.

#### Scenario: Massage price and deposit are in Valores
- **WHEN** se consulta Valores de Masajes
- **THEN** aparecen el precio de sesión y la condición de seña del 50%

### Requirement: Lactancia consultorio fiche is in the services agenda
La base de conocimiento MUST incluir en `# AGENDA DE SERVICIOS` la ficha `## 2. Consultorio de Lactancia: Atención de Demanda Espontánea y Turnos Programados` con los bloques mínimos de servicio (Descripción, Requisitos, Profesionales, Disponibilidad y reserva, Valores). MUST documentar: modalidad de demanda espontánea y turnos programados; lugar Consultorio; días y horarios martes y jueves 08:00–12:00, miércoles 10:00–13:00, viernes 14:00–18:00; Natalia (martes, jueves y viernes) con WhatsApp `+54 11 3198-9930`; Carolina Losada (miércoles y consultas generales) con el WhatsApp de TRAMA `+54 11 6956-6115`; precio de 1 consulta ~1 hora `$50.000`; seña del 50% para reservar turno programado. MUST NOT exigir seña para demanda espontánea. MUST NOT inventar una ficha BIO de Natalia. MUST NOT usar el handle `@trama.lomas` ni emojis en la ficha.

#### Scenario: Lactancia fiche follows the service template
- **WHEN** se consulta la ficha 2 en `# AGENDA DE SERVICIOS`
- **THEN** incluye Descripción, Requisitos, Profesionales, Disponibilidad y reserva, y Valores, con grilla, ambos profesionales y ambos WhatsApp

#### Scenario: Programmed booking lists price and deposit
- **WHEN** se lee Valores de Consultorio de Lactancia
- **THEN** aparecen 1 consulta ~1 hora a `$50.000` y seña del 50% para reservar el turno

#### Scenario: Walk-in does not require deposit in knowledge
- **WHEN** se lee Disponibilidad y reserva / Valores de lactancia
- **THEN** la seña está atada a reservar turno programado, no a la demanda espontánea en horario de atención

### Requirement: Service fiche may list a professional WhatsApp in addition to TRAMA
Cuando una ficha de servicio declara el WhatsApp de una profesional (número y cuándo usarlo), knowledge MUST dejarlo en esa ficha **además** del canal público general de TRAMA (`+54 11 6956-6115`). MUST NOT presentar el WhatsApp de la profesional como único canal ni como reemplazo del 6115. MUST NOT listar números de profesionales que no estén cargados. En servicios sin WhatsApp de profesional (p. ej. Masajes), el canal público MUST seguir siendo solo el de consultas TRAMA.

#### Scenario: Lactancia lists Natalia WhatsApp plus TRAMA
- **WHEN** se lee Profesionales o Disponibilidad de Consultorio de Lactancia
- **THEN** figuran `+54 11 3198-9930` para Natalia en sus días y `+54 11 6956-6115` como canal TRAMA / Carolina, no uno en vez del otro

#### Scenario: Massage fiche still has only TRAMA WhatsApp
- **WHEN** se lee la formalización de Masajes
- **THEN** el canal público citado sigue siendo el WhatsApp de consultas TRAMA, sin un WhatsApp de Gaby o Ivi
