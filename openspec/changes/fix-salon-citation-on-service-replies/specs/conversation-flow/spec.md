## MODIFIED Requirements

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
