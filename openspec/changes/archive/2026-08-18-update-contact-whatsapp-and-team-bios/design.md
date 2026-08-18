## Context

Hoy el bloque de contacto en `src/knowledge/cronograma.md` (y el copy de Masajes) dice que el canal público son Instagram/Facebook y que **no hay WhatsApp**. El system prompt refuerza “no inventes WhatsApp”. Eso era correcto cuando el número no estaba en la base; ahora el equipo quiere que TIA priorice el WhatsApp de consultas.

La formalización (cupo, turno, seña) sigue en el equipo de TRAMA: el WhatsApp es el **canal público para escribir**, no un booking automático ni un atajo “coordiná con la profe”.

En paralelo, knowledge nombra profesoras y profesionales pero no tiene una ficha BIO. La primera copy es de Caro Losada (creadora de Maternar y TRAMA).

Constraint: cambio localizado en knowledge + prompt + tests; sin APIs, UI ni PING.

## Goals / Non-Goals

**Goals:**
- WhatsApp de consultas como canal **prioritario** de inscripción/turnos: `+54 11 6956-6115`, lunes a viernes 09–21 hs.
- Redes (IG/FB de TRAMA y Maternar) quedan **secundarias**, no desaparecen.
- TIA pega número y horario al derivar; deja de decir que no hay WhatsApp.
- Sección BIO del equipo con Caro Losada verbatim; TIA usa esa ficha y no inventa bios faltantes.

**Non-Goals:**
- Integrar WhatsApp Business / webhooks / chat en WA.
- Inventar bios de Tami, Marilina, Alexandra, Gladys, Cielo, Gaby, Ivi u otras.
- Horario de fin de semana o teléfono de administración distinto al dado.
- Que TIA cierre turnos o inscripciones por WhatsApp.
- Cambiar PING, CSV, API o la UI.

## Decisions

1. **Un solo bloque canónico de contacto, más copys alineados**  
   Reemplazar el blockquote bajo `### Redes Sociales` por WhatsApp primero (número + días/horario) y redes como complemento. Actualizar el párrafo de **Formalización** en Masajes para el mismo canal.  
   Rationale: TIA lee todo el markdown; si Masajes sigue diciendo “solo redes”, el modelo puede ignorar el bloque nuevo.  
   Alternativa: solo editar líneas 52–55 → riesgo de respuestas mixtas.

2. **Formato del número como lo dio el equipo**  
   Conservar `+54 11 6956-6115`. No inventar un segundo teléfono. Un `wa.me/541169566115` MAY ir junto al número (mismo canal, clickeable); no es obligatorio.  
   Horario: **lunes a viernes, 09 a 21 hs**. MUST NOT afirmar atención sábado/domingo. Si preguntan fuera de franja, TIA puede decir el horario documentado y que escriban igual / esperen en esa ventana — sin inventar SLA.

3. **Prioridad al derivar (prompt)**  
   Orden: (1) WhatsApp + horario, (2) redes con URL concreta si hace falta un canal extra. Seguir: no inventar emails ni otros números. Quitar la frase que implica “no hay WhatsApp en la base”.  
   La regla “si no hay canal, no inventar” permanece por si el dato se borra.

4. **Sección `# EQUIPO` (bios) después del contexto / contacto, antes de las agendas**  
   Caro primero, texto de primera persona **verbatim** (incluyendo el trébol). Encabezado con nombre completo y apodo si ya se usa en clases (`Carolina Losada ("Caro")`) para cruzar con las fichas.  
   Comunidad Maternar (fundadora) se deja; la BIO la complementa, no la contradice.  
   **No** listar al resto del equipo con “bio pendiente”: un heading vacío invita al LLM a rellenar. Otras bios = nuevos `###` cuando haya copy.

5. **Qué puede decir TIA de alguien sin BIO**  
   Puede citar el rol en la agenda (p. ej. Tami da tal clase). MUST NOT armar trayectoria, títulos o tono personal que no estén en knowledge.

6. **Tests de string, no de LLM live**  
   Knowledge: número, “WhatsApp”, Lunes–Viernes / 09 / 21, BIO de Caro, ausencia de “No hay WhatsApp”. Prompt: pegar WhatsApp/horario; no contradecir. Masajes: canal WhatsApp, no “solo redes”.

## Risks / Trade-offs

- [TIA trata el WhatsApp como reserva instantánea] → Prompt + specs: formaliza el equipo; el WA es para escribir en el horario indicado.  
- [Confusión Caro vs administración] → El número es de **consultas TRAMA**, no el celular personal de una profe.  
- [Preguntas por gente sin BIO] → Spec: solo hechos de agenda; no inventar.  
- [wa.me vs número con guiones] → Si se agrega el link, debe ser el mismo 541169566115.

## Migration Plan

1. Editar `cronograma.md` y `system_prompt.md`.  
2. Ajustar tests de knowledge/prompt.  
3. Redeploy / restart del servicio para recargar knowledge (hoy se carga al iniciar).  

Rollback: revertir esos archivos.

## Open Questions

- ¿Incluir `wa.me` además del número? Default en apply: **sí**, mismo canal, una línea extra.  
- Próximas bios (Tami, etc.): fuera de este change hasta que haya texto.
