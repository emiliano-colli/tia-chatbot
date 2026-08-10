# services-knowledge

## Purpose

Contrato de estructura y contenido de la Agenda de Servicios en la base de conocimiento, y criterios para que el copy de reserva quede alineado al flujo del equipo TRAMA.

## Requirements

### Requirement: Services agenda uses a minimum service fiche template
La base de conocimiento MUST organizar `# AGENDA DE SERVICIOS` con ítems `## N. Nombre` cuya ficha mínima incluya: Descripción, Requisitos, Profesionales, Disponibilidad y reserva, y Valores. MUST NOT exigir la misma plantilla de horarios fijos que la Agenda de Actividades grupales. La numeración MAY reiniciar en 1 dentro de la agenda de servicios.

#### Scenario: Massage fiche follows the template
- **WHEN** se consulta la ficha de Masajes en la base de conocimiento
- **THEN** incluye los bloques mínimos de servicio (descripción, requisitos, profesionales, disponibilidad/reserva, valores)

### Requirement: Service booking copy defers formalization to TRAMA team
En fichas de servicios con cita, el texto de reserva en knowledge MUST indicar que la formalización del turno la coordina el equipo de TRAMA (y el canal público documentado en la base), MUST NOT instruir a “coordinar directamente” el cierre del turno solo con la profesional como sustituto de ese flujo, y MAY nombrar a las profesionales como quienes atienden / cuya agenda se acuerda vía el equipo.

#### Scenario: Massage reservation wording avoids direct booking shortcut
- **WHEN** se lee el bloque de disponibilidad/reserva o copy de reserva de Masajes
- **THEN** no indica al lector que cierre el turno coordinando directamente con la profesional al margen del equipo/canal documentado

### Requirement: Loaded service operational facts are present when known
Si un servicio tiene precio, seña, duración, sala o tipos cargados en knowledge, esos datos MUST figurar en la ficha bajo los bloques correspondientes (p. ej. seña junto a Valores) de forma explícita para que el asistente pueda citarlos.

#### Scenario: Massage price and deposit are in Valores
- **WHEN** se consulta Valores de Masajes
- **THEN** aparecen el precio de sesión y la condición de seña del 50%
