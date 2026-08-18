## Context

Tras `update-chat-ui-copy-and-mobile`, el chat ya no panea en horizontal. En `<480px` el toolbar pasa a `flex-direction: column` pero `.toolbar span` sigue con `flex: 1 1 12rem`. En columna `12rem` es altura: ~192px de vacío entre el hint y “Nueva consulta”/composer. En celular el footer se siente como media pantalla.

Constraint: un archivo HTML, sin framework. La Cursor rule `.cursor/rules/static-chat-ui.mdc` ya está en el working tree para no repetir el patrón.

## Goals / Non-Goals

**Goals:**
- Footer compacto en ~360px: hint, “Nueva consulta” e input juntos, sin bloque vacío.
- El área de mensajes recupera el espacio vertical.
- Documentar el criterio en la rule de `app/static/**`.

**Non-Goals:**
- No tocar copy, JS, API, Gradio ni el header.
- No esconder el hint ni el botón de nueva consulta.
- No rediseñar el layout header / chat / footer.

## Decisions

1. **Anular el basis en el media query, no en el default**  
   En `@media (max-width: 480px)`: `.toolbar span { flex: 0 0 auto; }`.  
   Rationale: en desktop el `12rem` sigue sirviendo para que hint y botón compartan fila.  
   Alternativa sacar `flex-basis` del default: el wrap en fila queda peor en anchos medios.

2. **Apretar gaps/padding solo en el breakpoint móvil**  
   Reducir `footer` padding y `toolbar` `gap`/`margin-bottom` bajo 480px lo justo para que el chrome no “respire” de más.  
   Alternativa achicar también en desktop: innecesario.

3. **Rule de Cursor, no skill**  
   `.cursor/rules/static-chat-ui.mdc` con `globs: app/static/**`.  
   Rationale: el criterio tiene que aplicarse solo al tocar la UI estática.  
   Alternativa skill `/compact-chat-chrome`: extra paso; esto es una invariante.

## Risks / Trade-offs

- [El hint + botón + composer siguen ocupando varias líneas] → Aceptado; compactar huecos, no ocultar controles.  
- [Teclado iOS sigue tapando el input] → Fuera de alcance; el reporte es el vacío entre hint e input.

## Migration Plan

1. CSS en `index.html` + confirmar la rule.  
2. `git pull` + restart `tia.service` en el CT.  
3. Celular o iframe 360px: sin hueco de ~12rem; footer al contenido.

Rollback: revertir el CSS (la rule puede quedarse).

## Open Questions

- Ninguno bloqueante.
