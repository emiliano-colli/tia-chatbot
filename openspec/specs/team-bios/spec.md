# team-bios

## Purpose

Fichas BIO del equipo en la base de conocimiento, y cómo TIA las usa al presentar a las personas del espacio sin inventar datos faltantes.

## Requirements

### Requirement: Knowledge includes a team bios section starting with Caro Losada
La base de conocimiento MUST incluir una sección de bios del equipo (p. ej. `# EQUIPO`) con una ficha para cada persona que tenga copy cargado. MUST comenzar por Carolina Losada ("Caro"), creadora de Maternar y TRAMA, con el texto de primera persona provisto por el equipo (partera, profe de yoga, doula y puericultora; TRAMA como espacio de movimiento consciente). MUST NOT inventar bios para profesionales nombradas en las agendas que aún no tengan ficha. MAY omitir headings vacíos hasta que haya texto.

#### Scenario: Caro bio is present with provided copy
- **WHEN** se consulta la sección de equipo / bios en knowledge
- **THEN** figura Caro Losada con el texto que la identifica como creadora de Maternar y TRAMA, partera, profe de yoga, doula y puericultora, y la descripción de TRAMA como espacio de movimiento consciente

#### Scenario: Missing bios are not fabricated in knowledge
- **WHEN** una profesional aparece en una agenda (p. ej. Tamara Lourenco) y no hay ficha BIO cargada
- **THEN** knowledge no inventa una biografía para esa persona

### Requirement: Assistant uses loaded bios and does not invent others
Cuando el usuario pregunte quién es una persona del espacio, TIA MUST usar la ficha BIO de knowledge si existe. Si no hay BIO, MUST limitarse a hechos ya cargados (p. ej. qué clase o servicio figura a su nombre) y MUST NOT inventar trayectoria, títulos o presentación personal.

#### Scenario: User asks who Caro is
- **WHEN** el usuario pregunta por Caro / Carolina Losada
- **THEN** TIA responde con la información de la BIO cargada (creadora de Maternar y TRAMA y roles documentados), sin contradecir Comunidad Maternar

#### Scenario: User asks about someone without a bio
- **WHEN** el usuario pregunta por una profesional sin ficha BIO
- **THEN** TIA no inventa una biografía y, si aplica, solo menciona el rol que conste en la agenda
