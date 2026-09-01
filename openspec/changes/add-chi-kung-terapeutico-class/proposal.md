## Why

TRAMA ya dicta Chi Kung Terapéutico (Marta Pistasoli, Sala Tierra, cuatro horarios, precios de abono) y TIA no lo tiene en la agenda ni en `# EQUIPO`. Quien pregunta por chi kung, Qi Gong o por Marta no recibe horarios, precio ni BIO: o TIA inventa o dice que no está.

## What Changes

- Agregar `## 11. Chi Kung Terapéutico` en `# AGENDA DE ACTIVIDADES GRUPALES` (plantilla de clases: descripción, requisitos, profesora, horarios, valores).
- Salón **Sala Tierra**; valores 4 clases `$50.000` / 8 clases `$78.000` / suelta o prueba `$15.000`.
- Incluir la actividad en el listado corto de Actividades del contexto.
- Ficha BIO de Marta Pistasoli (solo copy provisto + Instagram URL); Caro sigue primera. Sin inventar títulos ni WhatsApp propio.
- Keyword de PING `chi kung` (y alias `qigong` / `chi-kung`) para que el interés no quede “no detectado”.
- Fuera de alcance: mover Esfero Yoga de horario/salón, BIO de otras profesoras, WhatsApp de Marta.

## Capabilities

### New Capabilities

- Ninguna.

### Modified Capabilities

- `team-bios`: MUST incluir ficha de Marta Pistasoli cuando hay copy cargado; MUST NOT inventar voz en primera persona ni trayectoria extra.
- `admin-email-notification`: la heurística de intereses MUST reconocer chi kung / chi-kung / qigong como actividad.

## Impact

- `src/knowledge/cronograma.md` (contexto, `# EQUIPO`, ficha 11)
- `src/notifications/ping.py` (`_ACTIVITY_KEYWORDS`)
- Specs delta `team-bios` y `admin-email-notification`
- Tests de knowledge y de keywords PING
- Sin cambios de API, UI ni prompt (la plantilla de salón/media ya cubre Tierra)
