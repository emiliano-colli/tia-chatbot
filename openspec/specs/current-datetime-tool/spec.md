# current-datetime-tool

## Purpose

Proveer fecha/hora actual en Buenos Aires vía tool on-demand y usarla para interpretaciones temporales en el chatbot.

## Requirements

### Requirement: Current datetime tool returns Buenos Aires time in Spanish
El sistema MUST exponer una herramienta `get_current_datetime` que, al ejecutarse, MUST devolver la fecha y hora actuales en timezone `America/Buenos_Aires`, incluyendo el día de la semana en español, la fecha y la hora. MUST NOT depender de inventar o hardcodear una fecha de ejemplo en runtime.

#### Scenario: Tool output includes weekday date and time
- **WHEN** se ejecuta `get_current_datetime`
- **THEN** el resultado incluye día de la semana en español, fecha y hora correspondientes a `America/Buenos_Aires`

#### Scenario: Timezone is fixed to Buenos Aires
- **WHEN** el host del proceso está en otra zona horaria
- **THEN** el valor reportado por la tool sigue siendo el de `America/Buenos_Aires`

### Requirement: Chatbot invokes datetime tool for temporal interpretation
Cuando la consulta del usuario requiere interpretar referencias temporales relativas (por ejemplo “hoy”, “mañana”, “esta semana”) u otra interpretación temporal para responder, el asistente MUST obtener la fecha/hora actual mediante la tool `get_current_datetime` y MUST NOT inventar la fecha. El runtime del chatbot MUST ejecutar las tool calls del modelo y continuar hasta una respuesta de texto final.

#### Scenario: Relative day question triggers tool use path
- **WHEN** el usuario pregunta algo que depende de “hoy” u otra referencia temporal relativa
- **THEN** el flujo de `ask()` permite al modelo solicitar `get_current_datetime`, ejecuta la tool y produce una respuesta de texto anclada a ese resultado

#### Scenario: Non-temporal question can answer without inventing a date
- **WHEN** el usuario hace una pregunta que no requiere interpretación temporal
- **THEN** el sistema puede responder sin inventar una fecha actual

### Requirement: System prompt mandates real datetime for temporal answers
El prompt de sistema MUST instruir al asistente a usar la fecha actual (vía la tool) para interpretar “hoy”, “mañana”, “esta semana” y referencias temporales similares (incluyendo typos obvios), MUST prohibir inventar la fecha, y MUST indicar que la respuesta verbalice el día/fecha concreta obtenida.

#### Scenario: Prompt contains temporal tool guidance
- **WHEN** se carga el system prompt
- **THEN** incluye instrucciones para usar la fecha actual en interpretaciones temporales y no inventar la fecha

#### Scenario: Prompt requires stating the concrete day
- **WHEN** se carga el system prompt
- **THEN** indica que, tras usar la tool, se debe expresar el día o fecha concreta (por ejemplo al interpretar “mañana”)
