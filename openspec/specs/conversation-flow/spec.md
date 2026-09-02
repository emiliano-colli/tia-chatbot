# conversation-flow

## Purpose

Reglas de flujo conversacional de TIA: cuándo pedir identificación, cómo reutilizar datos ya dados y cómo derivar pedidos de inscripción/turno sin lenguaje de registro operativo falso.

## Requirements

### Requirement: Do not re-ask for contact data already provided
Si en el historial de la conversación el usuario ya proporcionó nombre y teléfono, TIA MUST NOT volver a pedirlos. MUST reconocerlos y continuar con la consulta.

#### Scenario: User already gave name and phone
- **WHEN** el usuario ya envió nombre y teléfono y luego pide un turno o más información
- **THEN** TIA no solicita de nuevo esos datos y continúa usando los ya dados

### Requirement: Identification timing after concrete interest
TIA MUST solicitar nombre y teléfono cuando hay interés concreto en una actividad/servicio o pedido de detalle (horarios, precios, requisitos, inscripción/turno). MUST NOT exigir identificación solo por un síntoma o malestar genérico sin interés explícito en un servicio.

#### Scenario: Symptom without service request
- **WHEN** el usuario menciona un malestar (por ejemplo dolor de espalda) sin pedir aún un servicio concreto ni detalle de precios/horarios
- **THEN** TIA puede orientar y ofrecer información sin exigir primero nombre y teléfono

#### Scenario: Concrete booking or detail request
- **WHEN** el usuario pide turno, inscripción o detalle de horarios/precios/requisitos de un servicio o actividad
- **THEN** TIA solicita identificación antes de ese detalle si aún no la tiene

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

### Requirement: Farewell messages close session inside ask
When `TiaChatbot.ask()` receives a user message that matches the centralized farewell detection (`is_session_end_message`), the system MUST call `end_session` for that session id (triggering admin PING when configured), MUST NOT send the farewell text to the LLM as a normal turn, and MUST return a fixed farewell reply to the caller.

#### Scenario: Chat API receives farewell
- **WHEN** `POST /chat` receives a body whose message is a recognized farewell phrase
- **THEN** the session is ended once, the response is the standard farewell text, and no LLM completion is required for that turn

#### Scenario: Farewell after prior messages
- **WHEN** the user had an active conversation and then sends a farewell-only message
- **THEN** the farewell closes the session and the PING reflects the prior dialogue

#### Scenario: Non-farewell messages unchanged
- **WHEN** the user message is not a recognized farewell
- **THEN** `ask()` proceeds with the normal LLM flow

### Requirement: Salon media is cited as foto and recorrido after useful info
Cuando TIA informa una actividad o servicio que knowledge asocia a un salón con líneas Foto y/o Video en `# SALONES`, MUST citar esa media **después** de la información útil (horario, precio, quién dicta o atiende, requisitos si aplican) y **después** de nombrar el salón. Esto MUST aplicarse también cuando el usuario pidió el servicio o la clase y **no** preguntó por el lugar ni por los salones. El texto visible de los enlaces MUST ser `foto` para la imagen y `recorrido` para el video, en una línea `foto · recorrido`, sin repetir el nombre del salón en el label. MUST usar Markdown `[foto](/static/…)` y `[recorrido](/static/…)` con los paths de knowledge. MUST NOT pegar la ruta como único texto del link. MUST NOT inventar un link si esa línea Foto o Video no está en knowledge. Si varias actividades de la misma respuesta van al mismo salón, MUST incluir el par una sola vez. Clases virtuales MUST NOT llevar foto ni recorrido.

#### Scenario: Activity in a salon with photo and video
- **WHEN** el usuario pide detalle de una clase que se dicta en Sala Aire y `# SALONES` tiene Foto y Video de Sala Aire
- **THEN** TIA da horario/precio/profe (u otros datos de la ficha), nombra Sala Aire, y cierra con enlaces `foto · recorrido` (labels, no paths crudos)

#### Scenario: Massage inquiry without asking about rooms
- **WHEN** el usuario pregunta por masajes (tipos, valores o disponibilidad) y no menciona salones
- **THEN** la respuesta nombra Sala Calma y incluye `[foto](/static/salones/calma.jpg) · [recorrido](/static/salones/calma.mp4)` (o las líneas Foto/Video vigentes de Calma)

#### Scenario: Same salon mentioned twice in one reply
- **WHEN** la respuesta lista dos actividades que se dictan en Sala Tierra
- **THEN** el par `foto · recorrido` de Tierra aparece una sola vez

#### Scenario: Missing video line is not invented
- **WHEN** knowledge tiene Foto de un salón pero no línea Video (archivo ausente o no cargado)
- **THEN** TIA incluye solo `foto` y MUST NOT inventar un recorrido ni otra URL

#### Scenario: Virtual class has no salon media
- **WHEN** el usuario pregunta por una clase virtual
- **THEN** TIA no pega foto ni recorrido de ningún salón para esa clase

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
