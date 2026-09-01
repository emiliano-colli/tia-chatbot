## Context

`# AGENDA DE SERVICIOS` hoy tiene solo Masajes. El Consultorio de Lactancia aparece en el contexto general, en `# SALONES` (lugar + `consultorio.jpg` / `.mp4`) y en la nota de la agenda de servicios, pero **sin ficha**. TIA no puede citar horarios, precio, seña ni a Natalia.

El canal público default sigue siendo el WhatsApp de consultas TRAMA (`+54 11 6956-6115`). En este servicio el equipo quiere, **además**, el WhatsApp de Natalia los días que atiende. El 6115 de Carolina **es** el mismo número general: no hay un tercer teléfono.

Constraint: knowledge + prompt + tests de string. Sin API, UI ni PING. Formalización sigue fuera de TIA.

## Goals / Non-Goals

**Goals:**
- Ficha `## 2. Consultorio de Lactancia` con la plantilla de servicios.
- Grilla, modalidad (espontánea y programada), profesionales, dos WhatsApp, $50.000 y seña 50% para turno reservado.
- Prompt: si la ficha declara WhatsApp de profesional, citarlo **además** del 6115.
- Al informar el servicio: Consultorio + `foto · recorrido` (paths ya en `# SALONES`).

**Non-Goals:**
- BIO de Natalia (solo rol, días y WhatsApp).
- Fichas de kinesio o psicología.
- Cambiar el default 6115 en Masajes u otras agendas.
- Que TIA reserve, cobre seña o escriba a WhatsApp.
- Player de video, URLs absolutas, o nuevos archivos en `/static/salones/`.

## Decisions

1. **Misma plantilla que Masajes; horarios van en Disponibilidad**  
   Bloques: Descripción, Requisitos, Profesionales, Disponibilidad y reserva, Valores.  
   No dejar una sección suelta “Contacto y Coordinación”: los números viven en Profesionales y se recuerdan en Disponibilidad.  
   Rationale: TIA ya sigue esa forma en Masajes.  
   Alternativa: copiar el borrador con headings extra → el modelo mezcla campos.

2. **Copy de knowledge sin handle ni emoji**  
   “TRAMA Lomas”, no `@trama.lomas` ni 💛. Tono cálido sí: no sola, espontánea o turno, embarazo → lactancia, red de sostén.  
   Rationale: el resto de `cronograma.md` no usa handle/emoji en fichas.  
   Alternativa: pegar el borrador verbatim → TIA puede citar Instagram como si fuera dato operativo.

3. **Dos números, no tres**  
   | Canal | Número | Uso |  
   |---|---|---|  
   | TRAMA / Carolina | `+54 11 6956-6115` (`wa.me/541169566115`) | Default siempre; miércoles 10–13; consultas generales cualquier día (lun–vie 09–21). |  
   | Natalia | `+54 11 3198-9930` (`wa.me/541131989930`) | Solo este servicio, mar/jue 08–12 y vie 14–18. |  
   Rationale: Carolina no suma un celular distinto; Natalia sí es un canal extra **declarado**.  
   Alternativa: solo 6115 → contradice al equipo. Solo Natalia esos días y ocultar TRAMA → pierde el default.

4. **Prompt: “además”, no “en vez de”**  
   Una regla corta junto a la de WhatsApp de consultas: si la ficha del servicio lista WhatsApp de profesional (número + cuándo), pegalo **además** del 6115; no inventes números que no estén en knowledge; no digas que hay que coordinar el cierre **solo** con la profesional como sustituto del canal TRAMA.  
   Rationale: hoy “priorizá el WhatsApp de consultas / no inventes otros números” hace que el modelo se coma el de Natalia o lo trate como invento.  
   Alternativa: solo knowledge, sin tocar prompt → alto riesgo de omitir Natalia.

5. **Espontánea vs seña**  
   Demanda espontánea: pueden acercarse en horario; avisar por WhatsApp es recomendable, no un requisito.  
   Seña 50% (`$50.000` la consulta): **para reservar turno programado**. No pedir seña a quien dice que va ahora en horario de atención.  
   Rationale: el texto del equipo ata la seña a “reservar el turno”.  
   Alternativa: seña siempre → TIA la pide en walk-in.

6. **Natalia sin `# EQUIPO`**  
   Puede figurar en la ficha. TIA no inventa BIO (regla ya existente).  
   Rationale: no hay copy de trayectoria.

7. **Tests de string**  
   Knowledge: heading `## 2. Consultorio de Lactancia`, grilla, ambos números + `wa.me`, Consultorio, `$50.000`, seña 50%, demanda espontánea.  
   Prompt: frase de WhatsApp de profesional **además** del de consultas.  
   No tests live de LLM.

## Risks / Trade-offs

- [TIA da solo el 6115] → Prompt + ficha con “además” y tests del número de Natalia.  
- [TIA da solo Natalia y esconde TRAMA] → Spec/prompt: el 6115 sigue disponible cualquier día.  
- [TIA inventa BIO o apellido de Natalia] → Sin ficha BIO; prompt existente.  
- [Seña en walk-in] → Knowledge: seña atada a reserva de turno.  
- [Confusión Carolina = 6115 vs “otro celular”] → En profesionales, el de Caro se etiqueta como WhatsApp de TRAMA.

## Migration Plan

1. Editar `cronograma.md` (ficha 2) y `system_prompt.md` (regla dual WhatsApp).  
2. Tests de knowledge/prompt.  
3. Restart del servicio para recargar knowledge.

Rollback: revertir esos archivos. `# SALONES` no cambia.

## Open Questions

Ninguna bloqueante. Quién cobra la seña (Natalia vs administración) no está en el borrador: TIA cita la condición de seña y el canal de la ficha, sin inventar medio de pago.
