## MODIFIED Requirements

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
Al finalizar una sesión, el sistema MUST construir el resumen de Contacto e Intereses interpretando el diálogo completo (mensajes de usuario y asistente), de modo que detecte nombre y teléfono aunque se provean en un mismo mensaje sin frases tipo “me llamo”, e intereses expresados por selección de menú, confirmación de inscripción u otras referencias en la conversación. Si un dato no puede determinarse, MUST usar una marca explícita de no provisto / no detectado. El fallo del resumen MUST NOT impedir escribir el CSV de cierre. El PING MUST enviarse en este fallo solo si la heurística de respaldo obtiene nombre o teléfono.

#### Scenario: Name and phone in one user message
- **WHEN** el usuario envía un mensaje con nombre y teléfono juntos (por ejemplo `Emiliano 1167462412`)
- **THEN** el resumen del PING incluye ese nombre y ese teléfono

#### Scenario: Interest chosen via menu option
- **WHEN** el usuario elige una actividad por número de menú (por ejemplo `8` correspondiente a Yoga Postparto) y/o confirma inscripción
- **THEN** el campo Intereses del PING refleja esa actividad (no un vacío genérico si el diálogo la identifica)

#### Scenario: Summary failure still allows notification
- **WHEN** falla la generación del resumen inteligente y la heurística no encuentra nombre ni teléfono
- **THEN** el sistema completa el cierre escribiendo el CSV y MUST NOT enviar PING

### Requirement: Inactivity timeout ends session and notifies
El sistema MUST rastrear la última actividad por sesión y MUST finalizar automáticamente sesiones cuya inactividad alcance `SESSION_TIMEOUT_MINUTES` (configurable vía entorno). Ese cierre MUST escribir el CSV de consulta y MUST disparar el PING solo si hay contacto significativo, igual que el cierre formal.

#### Scenario: Idle session times out
- **WHEN** una sesión supera `SESSION_TIMEOUT_MINUTES` sin actividad
- **THEN** el sistema cierra esa sesión, registra la fila CSV y envía el email PING al admin solo si hay nombre o teléfono

#### Scenario: Timeout duration comes from environment
- **WHEN** se configura `SESSION_TIMEOUT_MINUTES` en el entorno
- **THEN** el umbral de inactividad usado por el sistema refleja ese valor
