## Context

Respuesta real a “Hola, tienen yoga?”: cada clase es `1. Yoga Prenatal: …` y debajo `- Horarios:` / días. El clipboard no trae el `1.` porque el parser lo mete en `<li>` de `<ol>` y el número lo pinta el `::marker` del browser. Los `-` cortan el `<ol>`, así que la clase siguiente es otro `<ol>` → otra vez **1.**

Unir `1.` separados solo por blancos no alcanza: el corte es una **ul en el medio**.

## Goals / Non-Goals

**Goals:**
- Ningún `1.` fantasma de CSS en nombres de clase.
- `1. Título` → viñeta de sección (sub-orden respecto de `###` / ▸).
- `- Horarios` y días → lista indentada **debajo** de ese título.
- Pista en el prompt para no usar `1.` por actividad.

**Non-Goals:**
- Implementar Markdown anidado completo (indent con espacios).
- Seguir usando `<ol>` con numeración 1, 2, 3 (TIA repite `1.` y mezcla `-`).
- Extraer el parser a un archivo aparte.

## Decisions

1. **No emitir `<ol>` en burbujas bot**  
   `^\d+\. ` se trata como título de bloque, no como lista ordenada.  
   Rationale: el número del MD no es un orden real; el browser miente.  
   Alternativa (anidar `<ol><li>clase<ul>horarios</ul></li></ol>`): más frágil y TIA igual manda todo `1.`.  
   Alternativa (CSS `list-style: none` en ol): seguiría siendo ol semántico raro.

2. **Bloque `.md-section`**  
   - Título: `<p class="md-item">` con `::before { content: "• "; }` (distinto del ▸ de `###`).  
   - Si las siguientes no vacías son `-` / `*`, un `<ul>` hijo del mismo `.md-section` (indent). Cortar ante heading, otro `1.`, o párrafo.  
   Varios `1.` seguidos sin `-` = varios `.md-item` (viñetas), no un ol.

3. **Prompt**  
   Una viñeta: si listás actividades con horarios debajo, usá `### Nombre` o `**Nombre:**` y `-` para horarios; no enumeres cada clase con `1.`

4. **Tests**  
   El HTML del parser no crea `document.createElement("ol")` (o no hay `"ol"` en esa función). Presencia de `md-section` / `md-item`. Comentario o string de fixture con `Yoga Prenatal` + `Horarios` opcional.

## Risks / Trade-offs

- [Se pierde 1, 2, 3 “de verdad”] → Aceptado; TIA no los usa bien.  
- [Un `1.` suelto en una frase rara se ve como viñeta] → Mismo umbral que hoy (`^\d+\. ` al inicio de línea).  
- [El modelo ignora el prompt] → El parser igual no pinta ol.

## Migration Plan

`index.html` + prompt + tests. Hard refresh. Rollback: revertir.

## Open Questions

Ninguna. El • vs otro glifo se puede cambiar solo en CSS.
