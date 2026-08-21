# admin-email-notification

## Purpose

Notificar por email al admin de TRAMA al finalizar una sesión (cierre formal o timeout), con formato PING: contacto, intereses y log. El resumen de contacto/intereses se interpreta desde el diálogo completo.

## Requirements

### Requirement: Admin receives PING email on session end
Al finalizar una sesión **con al menos un dato de contacto significativo** (nombre o teléfono reales; placeholders como `No provisto` no cuentan), el sistema MUST enviar un email a `ADMIN_EMAIL` con formato PING. El asunto MUST incluir el ID de consulta y los datos disponibles de nombre, teléfono e interés (por ejemplo `Nueva consulta TIA #{id} — {nombre} / {telefono} / {interes}`). El cuerpo MUST incluir ID, Contacto (nombre y teléfono), Intereses, Origen y el Log completo de la conversación usuario/asistente. Contacto e Intereses MUST basarse en el resumen de sesión interpretado del diálogo completo. El remitente MUST usar la cuenta SMTP configurada (`MAIL_FROM` / `SMTP_USER`), que MAY ser distinta de `ADMIN_EMAIL`. Si no hay contacto significativo, el sistema MUST NOT enviar el email.

#### Scenario: Formal session end sends PING
- **WHEN** el usuario cierra formalmente la conversación y hay nombre o teléfono identificable
- **THEN** el sistema envía un email PING a `ADMIN_EMAIL` con ID, contacto, intereses, origen y log

#### Scenario: Subject uses contact name when available
- **WHEN** la sesión finaliza y hay un nombre de contacto identificado en el diálogo
- **THEN** el asunto del email incluye el ID de consulta y ese nombre (junto a teléfono e interés si están disponibles)

#### Scenario: Missing contact data is explicit
- **WHEN** la sesión finaliza sin nombre y/o teléfono identificables en el diálogo
- **THEN** el registro interno refleja esos campos como no provistos y el sistema MUST NOT enviar email PING

#### Scenario: Greeting-only session does not send PING
- **WHEN** la sesión finaliza y el diálogo no contiene nombre ni teléfono (por ejemplo solo “Hola”)
- **THEN** el sistema no envía email PING

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

### Requirement: Extractor treats informational interest as detectable
El prompt o instrucciones del extractor de resumen MUST indicar que una pregunta sobre existencia de una actividad, o un pedido de precios/horarios/requisitos de lo ya hablado, cuenta como interés aunque no haya menú numérico ni pedido de inscripción o turno. Si el diálogo nombra varias variantes de una familia y el usuario no elige una, el campo Intereses MUST registrar la familia, no un vacío. Las marcas de inscripción o turno MUST aparecer solo cuando el diálogo muestra esa solicitud.

#### Scenario: Family named when no class picked
- **WHEN** TIA lista varias clases de una familia (por ejemplo Yoga Prenatal, Postparto y Hatha) y el usuario no elige una
- **THEN** Intereses refleja la familia (por ejemplo yoga) y no un placeholder de no detectado

#### Scenario: Enrollment flag only when requested
- **WHEN** el usuario consultó información de una actividad y dio contacto pero no pidió inscribirse ni turno
- **THEN** Intereses no incluye la marca de solicitó inscripción ni solicitó turno

### Requirement: PING interests flag enrollment or appointment requests
Cuando el diálogo indica que la persona solicitó inscripción a una actividad o turno/reserva de un servicio, el resumen de Intereses del email PING MUST incluir una marca explícita de esa solicitud (por ejemplo junto al nombre de la actividad/servicio), sin exigir un campo nuevo en el mail.

#### Scenario: Enrollment request reflected in interests
- **WHEN** la sesión finaliza tras un pedido claro de inscripción a una actividad identificada
- **THEN** el campo Intereses del PING menciona esa actividad y que se solicitó inscripción

#### Scenario: Appointment request reflected in interests
- **WHEN** la sesión finaliza tras un pedido claro de turno para un servicio identificado
- **THEN** el campo Intereses del PING menciona ese servicio y que se solicitó turno

### Requirement: Inactivity timeout ends session and notifies
El sistema MUST rastrear la última actividad por sesión y MUST finalizar automáticamente sesiones cuya inactividad alcance `SESSION_TIMEOUT_MINUTES` (configurable vía entorno). Ese cierre MUST escribir el CSV de consulta y MUST disparar el PING solo si hay contacto significativo, igual que el cierre formal.

#### Scenario: Idle session times out
- **WHEN** una sesión supera `SESSION_TIMEOUT_MINUTES` sin actividad
- **THEN** el sistema cierra esa sesión, registra la fila CSV y envía el email PING al admin solo si hay nombre o teléfono

#### Scenario: Timeout duration comes from environment
- **WHEN** se configura `SESSION_TIMEOUT_MINUTES` en el entorno
- **THEN** el umbral de inactividad usado por el sistema refleja ese valor

### Requirement: SMTP credentials come from environment
La configuración de envío (host, puerto, usuario, contraseña de aplicación, remitente, destinatario admin y timeout) MUST leerse desde variables de entorno / `.env`. Secretos MUST NOT hardcodearse en el código fuente.

#### Scenario: Missing SMTP config fails safely on send
- **WHEN** falta configuración SMTP requerida al intentar notificar
- **THEN** el sistema registra el error y MUST NOT exponer secretos; el fallo de envío MUST NOT tumbar de forma no controlada el proceso de chat principal
