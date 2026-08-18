## Context

La UI interna es un único `app/static/index.html` servido en `GET /`. Ya tiene `meta viewport`, pero el CSS usa filas flex sin wrap: el bloque de título no puede encoger (`min-width: auto`) y el toolbar (`hint` + “Nueva consulta”) queda en una sola línea. En un celular (~360px) hay que panear para leer el header o alcanzar el botón.

El subtítulo actual es `Preguntame sobre talleres, servicios y más 🌿`. El copy nuevo es más largo, así que sin wrap el overflow empeora.

Constraint: cero build, sin framework, un archivo. El canal de testers es esta página, no Gradio.

## Goals / Non-Goals

**Goals:**
- Mostrar el subtítulo ampliado en el header.
- Que título, subtítulo, “Nueva consulta” y “Enviar” sean alcanzables en viewport estrecho sin scroll horizontal.
- Cambios mínimos, localizados en el HTML/CSS existente.

**Non-Goals:**
- No tocar Gradio, API, JS de sesión ni Nginx.
- No introducir CSS framework ni archivos `.css` separados.
- No rediseñar la UI (seguir: header / chat / footer).
- No optimizar teclado iOS más allá de no forzar zoom al enfocar el input (`font-size` ≥ 16px, ya presente).

## Decisions

1. **Copy exacto, sin acento nuevo**  
   Texto: `Preguntame sobre clases de yoga, entrenamiento funcional, talleres, servicios de salud, bienestar y más 🌿`.  
   Rationale: coincide con el pedido y con el estilo actual (`Preguntame`).  
   Alternativa “Pregúntame”: rechazada para no mezclar un cambio ortográfico no pedido.

2. **CSS en el mismo `index.html`**  
   Ajustar el `<style>` existente.  
   Rationale: un solo asset estático, despliegue idéntico.  
   Alternativa archivo CSS aparte: más movimiento para el mismo resultado.

3. **Wrap en flex, no layout distinto**  
   - Header: el contenedor del título con `flex: 1; min-width: 0` para que el subtítulo envuelva.  
   - Toolbar: `flex-wrap: wrap` (y columna bajo ~480px) para que “Nueva consulta” baje si no cabe.  
   - Composer: el input con `min-width: 0` para que no empuje “Enviar”.  
   - `html, body { overflow-x: hidden }` como red de seguridad.  
   - `min-height: 100dvh` (con fallback `100vh`) para la barra del browser móvil.  
   Rationale: corrige la causa (flex que no encoge) sin rediseñar.  
   Alternativa media queries que escondan el hint: rechazada; el hint de despedida sigue siendo útil.

4. **Verificación por markup + revisión visual**  
   El test de `GET /` afirma el subtítulo nuevo. El “sin paneo horizontal” se valida a ojo en DevTools (~360px) o en un celular de staging.  
   Rationale: no hay harness de browser en el repo; no vale la pena agregar uno para este cambio.

## Risks / Trade-offs

- [Subtítulo largo ocupa 3–4 líneas en celular] → Trade-off aceptado; priorizar copy completo sobre header compacto.  
- [Teclado iOS sigue tapando el composer en algunos Safari] → Fuera de alcance; el reporte actual es paneo horizontal, no teclado.  
- [Gradio queda con copy viejo] → Aceptado; no es el canal de testers internos.

## Migration Plan

1. Editar `app/static/index.html` y el test de `GET /`.  
2. `git pull` + restart `tia.service` en el CT.  
3. Abrir `/` en celular o en DevTools 360px: título y botones visibles sin scroll horizontal.

Rollback: revertir el HTML (un archivo).

## Open Questions

- Ninguno bloqueante.
