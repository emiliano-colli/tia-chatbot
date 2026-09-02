## ADDED Requirements

### Requirement: Lactancia answers use schedule dual WhatsApp and consultorio media
Cuando el usuario consulta el Consultorio de Lactancia, TIA MUST afirmar que el servicio existe, MUST citar la grilla documentada (martes y jueves 08:00–12:00, miércoles 10:00–13:00, viernes 14:00–18:00), MUST explicar demanda espontánea y turnos programados, MUST nombrar Consultorio y cerrar con `[foto](/static/salones/consultorio.jpg) · [recorrido](/static/salones/consultorio.mp4)` si esas líneas están en `# SALONES`, MUST citar el WhatsApp de Natalia en sus días y el de TRAMA/Carolina como canal general y del miércoles, MUST citar `$50.000` y seña del 50% cuando hable de **reservar un turno programado**, y MUST NOT exigir seña para una llegada espontánea en horario de atención. MUST NOT inventar quién atiende un día que no esté en la ficha. MUST NOT inventar BIO de Natalia.

#### Scenario: User asks lactancia hours and how to come
- **WHEN** el usuario pregunta horarios o si puede acercarse al Consultorio de Lactancia
- **THEN** TIA da la grilla, explica que puede venir en demanda espontánea en esos horarios (avisar por WhatsApp es recomendable, no un requisito) y cita ambos canales según el día

#### Scenario: User asks to book a lactancia appointment
- **WHEN** el usuario pide un turno programado de lactancia
- **THEN** TIA informa precio `$50.000`, seña del 50%, Consultorio + `foto · recorrido`, y pega Natalia y/o TRAMA según la ficha, sin confirmar el turno

#### Scenario: Walk-in now does not get deposit pitch as a blocker
- **WHEN** el usuario dice que va ahora en un horario de atención documentado
- **THEN** TIA no presenta la seña como requisito de esa llegada espontánea y puede sugerir avisar por el WhatsApp del día
