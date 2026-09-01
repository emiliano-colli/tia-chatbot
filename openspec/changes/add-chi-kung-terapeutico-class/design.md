## Context

La agenda grupal termina en `## 10. Hatha Yoga`. Chi Kung Terapéutico no existe en knowledge. Marta Pistasoli no está en `# EQUIPO`. El detector PING no tiene keyword de chi kung.

El equipo confirmó: **Sala Tierra**, valores iguales a Hatha / Movimiento Integrado (`$50.000` / `$78.000` / `$15.000`). Inscripción sigue por WhatsApp TRAMA 6115.

Constraint: knowledge + keyword PING + tests. Sin API, UI ni prompt (Tierra ya tiene `foto · recorrido` en `# SALONES`).

## Goals / Non-Goals

**Goals:**
- Ficha `## 11. Chi Kung Terapéutico` con plantilla de clases.
- Cuatro horarios de 1 h, Sala Tierra, precios de abono/prueba.
- BIO de Marta (tercera persona, Instagram URL).
- Keywords PING para chi kung / chi-kung / qigong.
- “chi kung terapéutico” en el listado de Actividades del contexto.

**Non-Goals:**
- Cambiar horario o salón de Esfero Yoga (miércoles 16:15 Tierra).
- BIO de Tami, Marilina u otras.
- WhatsApp o handle de Marta en la ficha de la clase.
- Emoji, CTA “te esperamos”, o `@marti_…` suelto en la agenda.

## Decisions

1. **`## 11` después de Hatha, no reordenar**  
   Misma numeración creciente.  
   Rationale: TIA y tests citan “10. Hatha Yoga”; no romper menús mentales.  
   Alternativa: insertar por temática (movimiento suave junto a Hatha) → renumerar todo.

2. **Plantilla de clase, no de servicio**  
   Descripción, Requisitos, Profesora, Horarios, Valores. Nota de salón como Hatha (`> Todas las clases se dictan en **Sala Tierra**.`).  
   Rationale: es actividad grupal con cita previa de la nota general de la agenda.  
   Alternativa: ficha tipo masajes → TIA la trataría como servicio con seña.

3. **Copy sin emoji ni handle; alias en descripción**  
   Una línea: también se nombra Chi-Kung o Qi Gong.  
   Rationale: TIA matchea preguntas variadas; knowledge no usa `@` en fichas.  
   Instagram de Marta solo en BIO, URL completa.

4. **BIO en tercera persona, después de Caro**  
   Texto: dicta Chi Kung en TRAMA; enamorada de la disciplina y así la transmite; Instagram `https://www.instagram.com/marti_chikungterapeutico/`.  
   Rationale: el copy del equipo no está en primera persona; inventar “Soy Marta…” viola team-bios.  
   Caro verbatim se queda primera.

5. **Valores copiados del dato del equipo**  
   4 clases `$50.000`, 8 clases `$78.000`, suelta/prueba `$15.000`. Sin seña (no es servicio con cita).  
   Los cuatro horarios son turnos de la misma actividad; TIA no inventa un “pack mañana vs tarde”.

6. **Keywords PING**  
   Agregar `"chi kung"`, `"chi-kung"`, `"qigong"` a `_ACTIVITY_KEYWORDS`.  
   `"chi kung"` cubre “chi kung terapéutico”. No hace falta tocar el prompt del extractor (ya generaliza familias).

7. **Overlap miércoles Tierra: documentar, no “arreglar”**  
   Esfero Yoga mié 16:15–17:15 (default Tierra) y Chi Kung mié 16:30–17:30 (Tierra explícito) se pisan 15 min. El equipo eligió Tierra.  
   Rationale: no mover otra ficha sin pedido. Queda como riesgo operativo, no de TIA.

## Risks / Trade-offs

- [TIA no reconoce “qi gong” con espacio] → Keyword `qigong` cubre pegado; `chi kung` cubre la forma local. Si aparece “qi gong” seguido, el LLM del PING igual puede nombrarlo; la heurística no. Aceptable.  
- [Overlap Tierra miércoles] → TIA citará ambos en Tierra; el cupo físico lo resuelve el equipo.  
- [BIO inventada si se parafrasea de más] → Copy mínimo, tests de strings de Marta + URL.  
- [Keyword `chi` sola] → No agregar: demasiado genérico.

## Migration Plan

1. Editar `cronograma.md` y `_ACTIVITY_KEYWORDS`.  
2. Tests de knowledge + keyword.  
3. Restart del servicio para recargar knowledge.

Rollback: revertir esos archivos.

## Open Questions

Ninguna bloqueante. El roce de Tierra el miércoles queda informado al equipo, fuera de este change.
