## ADDED Requirements

### Requirement: Admin receives PING email on session end
Al finalizar una sesión, el sistema MUST enviar un email a `ADMIN_EMAIL` con formato PING: asunto `Nueva consulta TIA — {nombre}` (o equivalente cuando el nombre no esté disponible), y cuerpo que MUST incluir Contacto (nombre y teléfono), Intereses y el Log completo de la conversación usuario/asistente. El remitente MUST usar la cuenta SMTP configurada (`MAIL_FROM` / `SMTP_USER`), que MAY ser distinta de `ADMIN_EMAIL`.

#### Scenario: Formal session end sends PING
- **WHEN** el usuario cierra formalmente la conversación
- **THEN** el sistema envía un email PING a `ADMIN_EMAIL` con contacto, intereses y log

#### Scenario: Subject uses contact name when available
- **WHEN** la sesión finaliza y hay un nombre de contacto identificado
- **THEN** el asunto del email incluye ese nombre tras el prefijo `Nueva consulta TIA —`

#### Scenario: Missing contact data is explicit
- **WHEN** la sesión finaliza sin nombre y/o teléfono provistos
- **THEN** el email indica claramente que esos datos no fueron provistos y igualmente incluye el log disponible

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
