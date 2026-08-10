## ADDED Requirements

### Requirement: PING interests flag enrollment or appointment requests
Cuando el diálogo indica que la persona solicitó inscripción a una actividad o turno/reserva de un servicio, el resumen de Intereses del email PING MUST incluir una marca explícita de esa solicitud (por ejemplo junto al nombre de la actividad/servicio), sin exigir un campo nuevo en el mail.

#### Scenario: Enrollment request reflected in interests
- **WHEN** la sesión finaliza tras un pedido claro de inscripción a una actividad identificada
- **THEN** el campo Intereses del PING menciona esa actividad y que se solicitó inscripción

#### Scenario: Appointment request reflected in interests
- **WHEN** la sesión finaliza tras un pedido claro de turno para un servicio identificado
- **THEN** el campo Intereses del PING menciona ese servicio y que se solicitó turno
