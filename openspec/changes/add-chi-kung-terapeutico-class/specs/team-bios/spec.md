## ADDED Requirements

### Requirement: Knowledge includes Marta Pistasoli bio for Chi Kung
La sección `# EQUIPO` MUST incluir una ficha `### Marta Pistasoli` **después** de Carolina Losada, con el copy cargado: dicta Chi Kung Terapéutico en TRAMA; está enamorada de la disciplina y así la transmite; Instagram `https://www.instagram.com/marti_chikungterapeutico/`. MUST NOT reescribir esa ficha en primera persona. MUST NOT inventar títulos, años de práctica, WhatsApp ni otros canales. MUST NOT agregar bios de otras profesoras en este cambio.

#### Scenario: Marta bio is present after Caro
- **WHEN** se consulta `# EQUIPO`
- **THEN** figura Marta Pistasoli después de Carolina Losada, con Chi Kung Terapéutico y la URL de Instagram, sin un heading `Soy Marta`

#### Scenario: Marta bio does not invent extra credentials
- **WHEN** se lee la ficha de Marta Pistasoli
- **THEN** no aparecen títulos, teléfono propio ni trayectoria que no estén en el copy provisto

### Requirement: Assistant uses Marta bio when asked who she is
Cuando el usuario pregunte quién es Marta / Marta Pistasoli, TIA MUST usar la ficha BIO cargada (Chi Kung en TRAMA, tono de la disciplina, Instagram si preguntan redes) y MUST NOT inventar una biografía más larga.

#### Scenario: User asks who Marta is
- **WHEN** el usuario pregunta por Marta Pistasoli
- **THEN** TIA responde con el copy de knowledge (Chi Kung Terapéutico en TRAMA y que transmite la disciplina con entusiasmo) sin inventar títulos
