## ADDED Requirements

### Requirement: Heuristic activity keywords include chi kung
La heurística de respaldo de intereses del PING MUST tratar `chi kung`, `chi-kung` y `qigong` como keywords de actividad, igual que las demás de `_ACTIVITY_KEYWORDS`. MUST NOT usar un token demasiado genérico (por ejemplo solo `chi`).

#### Scenario: User mentions chi kung and heuristic fills interest
- **WHEN** el resumen inteligente omite intereses y el texto del usuario contiene “chi kung”
- **THEN** el campo Intereses del resumen final incluye chi kung y MUST NOT quedar en placeholder de no detectado

#### Scenario: Hyphenated or qigong spelling is detected
- **WHEN** el texto del usuario contiene “chi-kung” o “qigong” y la heurística corre para intereses
- **THEN** Intereses refleja esa actividad y MUST NOT quedar vacío por la variante ortográfica
