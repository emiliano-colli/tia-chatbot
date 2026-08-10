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
Al manejar pedidos de inscripción o turno, TIA MUST aportar valor informativo disponible, anclar referencias temporales si aplican, derivar la formalización a administración y ofrecer canal de contacto de knowledge cuando exista. MUST NOT usar lenguaje que implique haber registrado operativamente la consulta (por ejemplo “he registrado tu consulta” / “procedo a registrar”).

#### Scenario: User wants a massage tomorrow
- **WHEN** el usuario pide un masaje para mañana
- **THEN** TIA ancla “mañana” a una fecha concreta vía tool de fecha, informa lo que haya en knowledge sin inventar, explica que el turno lo confirma admin, y ofrece canal de contacto si está en knowledge

#### Scenario: Avoid fake registration phrasing
- **WHEN** TIA confirma haber recibido nombre y teléfono
- **THEN** lo hace sin afirmar un registro operativo tipo “he registrado tu consulta”

### Requirement: Service answers use fiche fields without inventing a schedule
Cuando el usuario consulta un servicio con cita documentado en knowledge, TIA MUST afirmar que el servicio existe si está listado, MUST usar los campos cargados (tipos, profesionales, sala, precio, seña, modalidad de agenda), MUST NOT inventar franjas horarias fijas si knowledge indica que se acuerda disponibilidad, y MUST pegar el canal de contacto concreto de la base cuando derive a redes.

#### Scenario: User asks massage prices
- **WHEN** el usuario pregunta por precios de masajes y la ficha tiene valor y seña
- **THEN** TIA confirma que hay masajes, informa precio y seña, explica que el horario se acuerda / formaliza el equipo, e incluye el canal de knowledge si ofrece redes

#### Scenario: No fixed schedule in knowledge
- **WHEN** knowledge dice que la agenda se acuerda según disponibilidad
- **THEN** TIA no inventa días u horas concretas de atención
