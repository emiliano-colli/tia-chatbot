## MODIFIED Requirements

### Requirement: Session contact summary interprets full dialog
Al finalizar una sesión, el sistema MUST construir el resumen de Contacto e Intereses interpretando el diálogo completo (mensajes de usuario y asistente), de modo que detecte nombre y teléfono aunque se provean en un mismo mensaje sin frases tipo “me llamo”, e intereses expresados por pregunta sobre una actividad o familia de actividades, pedido de detalle (horarios, precios, requisitos), selección de menú, confirmación de inscripción u otras referencias en la conversación. Si el resumen inteligente omite un campo (null, vacío o placeholder) y una heurística de respaldo obtiene un valor no vacío para ese mismo campo, el sistema MUST usar el valor heurístico en ese campo y MUST NOT descartar los demás campos ya extraídos. Si un dato no puede determinarse por ninguna de las dos vías, MUST usar una marca explícita de no provisto / no detectado. El fallo del resumen MUST NOT impedir escribir el CSV de cierre. El PING MUST enviarse en este fallo solo si la heurística de respaldo obtiene nombre o teléfono.

#### Scenario: Name and phone in one user message
- **WHEN** el usuario envía un mensaje con nombre y teléfono juntos (por ejemplo `Emiliano 1167462412`)
- **THEN** el resumen del PING incluye ese nombre y ese teléfono

#### Scenario: Interest chosen via menu option
- **WHEN** el usuario elige una actividad por número de menú (por ejemplo `8` correspondiente a Yoga Postparto) y/o confirma inscripción
- **THEN** el campo Intereses del PING refleja esa actividad (no un vacío genérico si el diálogo la identifica)

#### Scenario: Interest from activity question and prices without enrollment
- **WHEN** el usuario pregunta si hay clases de una actividad (por ejemplo yoga), pide precios y entrega nombre y teléfono, sin elegir una variante ni pedir inscripción
- **THEN** el campo Intereses del PING nombra esa actividad o familia (por ejemplo yoga) y MUST NOT quedar en placeholder de no detectado

#### Scenario: Intelligent summary null interest filled from heuristic
- **WHEN** el resumen inteligente devuelve nombre y teléfono válidos pero intereses vacío o null, y el texto del usuario contiene una keyword de actividad (por ejemplo “yoga”)
- **THEN** el resumen final conserva ese nombre y teléfono y completa Intereses con el valor heurístico

#### Scenario: Specific LLM interest is not overwritten
- **WHEN** el resumen inteligente ya identifica una actividad concreta (por ejemplo “Yoga Postparto — solicitó inscripción”)
- **THEN** el campo Intereses conserva ese valor y MUST NOT reemplazarlo por un keyword genérico

#### Scenario: Summary failure still allows notification
- **WHEN** falla la generación del resumen inteligente y la heurística no encuentra nombre ni teléfono
- **THEN** el sistema completa el cierre escribiendo el CSV y MUST NOT enviar PING

## ADDED Requirements

### Requirement: Extractor treats informational interest as detectable
El prompt o instrucciones del extractor de resumen MUST indicar que una pregunta sobre existencia de una actividad, o un pedido de precios/horarios/requisitos de lo ya hablado, cuenta como interés aunque no haya menú numérico ni pedido de inscripción o turno. Si el diálogo nombra varias variantes de una familia y el usuario no elige una, el campo Intereses MUST registrar la familia, no un vacío. Las marcas de inscripción o turno MUST aparecer solo cuando el diálogo muestra esa solicitud.

#### Scenario: Family named when no class picked
- **WHEN** TIA lista varias clases de una familia (por ejemplo Yoga Prenatal, Postparto y Hatha) y el usuario no elige una
- **THEN** Intereses refleja la familia (por ejemplo yoga) y no un placeholder de no detectado

#### Scenario: Enrollment flag only when requested
- **WHEN** el usuario consultó información de una actividad y dio contacto pero no pidió inscribirse ni turno
- **THEN** Intereses no incluye la marca de solicitó inscripción ni solicitó turno
