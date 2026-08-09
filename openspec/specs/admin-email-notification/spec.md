# admin-email-notification

## Purpose

Notificar por email al admin de TRAMA al finalizar una sesión (cierre formal o timeout), con formato PING: contacto, intereses y log. El resumen de contacto/intereses se interpreta desde el diálogo completo.

## Requirements

### Requirement: Admin receives PING email on session end
Al finalizar una sesión, el sistema MUST enviar un email a `ADMIN_EMAIL` con formato PING: asunto `Nueva consulta TIA — {nombre}` (o equivalente cuando el nombre no esté disponible), y cuerpo que MUST incluir Contacto (nombre y teléfono), Intereses y el Log completo de la conversación usuario/asistente. Contacto e Intereses MUST basarse en el resumen de sesión interpretado del diálogo completo. El remitente MUST usar la cuenta SMTP configurada (`MAIL_FROM` / `SMTP_USER`), que MAY ser distinta de `ADMIN_EMAIL`.

#### Scenario: Formal session end sends PING
- **WHEN** el usuario cierra formalmente la conversación
- **THEN** el sistema envía un email PING a `ADMIN_EMAIL` con contacto, intereses y log

#### Scenario: Subject uses contact name when available
- **WHEN** la sesión finaliza y hay un nombre de contacto identificado en el diálogo
- **THEN** el asunto del email incluye ese nombre tras el prefijo `Nueva consulta TIA —`

#### Scenario: Missing contact data is explicit
- **WHEN** la sesión finaliza sin nombre y/o teléfono identificables en el diálogo
- **THEN** el email indica claramente que esos datos no fueron provistos y igualmente incluye el log disponible

### Requirement: Session contact summary interprets full dialog
Al finalizar una sesión, el sistema MUST construir el resumen de Contacto e Intereses interpretando el diálogo completo (mensajes de usuario y asistente), de modo que detecte nombre y teléfono aunque se provean en un mismo mensaje sin frases tipo “me llamo”, e intereses expresados por selección de menú, confirmación de inscripción u otras referencias en la conversación. Si un dato no puede determinarse, MUST usar una marca explícita de no provisto / no detectado.

#### Scenario: Name and phone in one user message
- **WHEN** el usuario envía un mensaje con nombre y teléfono juntos (por ejemplo `Emiliano 1167462412`)
- **THEN** el resumen del PING incluye ese nombre y ese teléfono

#### Scenario: Interest chosen via menu option
- **WHEN** el usuario elige una actividad por número de menú (por ejemplo `8` correspondiente a Yoga Postparto) y/o confirma inscripción
- **THEN** el campo Intereses del PING refleja esa actividad (no un vacío genérico si el diálogo la identifica)

#### Scenario: Summary failure still allows notification
- **WHEN** falla la generación del resumen inteligente
- **THEN** el sistema igualmente puede completar el cierre con PING usando valores explícitos de dato no disponible y el log completo

### Requirement: Inactivity timeout ends session and notifies
El sistema MUST rastrear la última actividad por sesión y MUST finalizar automáticamente sesiones cuya inactividad alcance `SESSION_TIMEOUT_MINUTES` (configurable vía entorno). Ese cierre MUST disparar el mismo flujo de notificación PING que el cierre formal.

#### Scenario: Idle session times out
- **WHEN** una sesión supera `SESSION_TIMEOUT_MINUTES` sin actividad
- **THEN** el sistema cierra esa sesión y envía el email PING al admin

#### Scenario: Timeout duration comes from environment
- **WHEN** se configura `SESSION_TIMEOUT_MINUTES` en el entorno
- **THEN** el umbral de inactividad usado por el sistema refleja ese valor

### Requirement: SMTP credentials come from environment
La configuración de envío (host, puerto, usuario, contraseña de aplicación, remitente, destinatario admin y timeout) MUST leerse desde variables de entorno / `.env`. Secretos MUST NOT hardcodearse en el código fuente.

#### Scenario: Missing SMTP config fails safely on send
- **WHEN** falta configuración SMTP requerida al intentar notificar
- **THEN** el sistema registra el error y MUST NOT exponer secretos; el fallo de envío MUST NOT tumbar de forma no controlada el proceso de chat principal
