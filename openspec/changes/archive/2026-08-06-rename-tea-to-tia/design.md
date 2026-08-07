## Context

El repo local y remoto ya se llaman `tia-chatbot`, pero el código y la documentación siguen usando **Tea** / **Téa** (legado de TEA-Chatbot). El rename es transversal (dominio, CLI, API title, Gradio entrypoint, tests, prompt, docs) pero no cambia arquitectura ni dependencias.

Convenciones del proyecto: `PascalCase` para clases, `snake_case` para variables; cambios mínimos y localizados.

## Goals / Non-Goals

**Goals:**
- Unificar la identidad del producto como **TIA** (Trama IA).
- Usar **TIA Chatbot** en títulos y copy de producto (sin guión).
- Renombrar símbolos internos a `TiaChatbot` / `tia` según convenciones Python.
- Actualizar prompt y docs para que no queden referencias a Téa/Tea.

**Non-Goals:**
- Renombrar el repositorio GitHub (ya es `tia-chatbot`).
- Introducir alias de compatibilidad `TeaChatbot`.
- Cambiar rutas HTTP, schemas de request/response o comportamiento conversacional más allá del nombre.
- Explicar obligatoriamente “TIA = Trama IA” en el prompt (opcional; no bloqueante).
- Renombrar carpetas o archivos (no hay módulos `tea_*`).

## Decisions

1. **Clase `TiaChatbot` (sin guión, PascalCase)**  
   - Rationale: TIA es sigla; en identificadores Python se compacta a `Tia` + `Chatbot`.  
   - Alternativa rechazada: `TIAChatbot` (todo mayúsculas rompe el estilo PascalCase del repo).

2. **Títulos visibles: `TIA Chatbot` (espacio, sin guión)**  
   - Rationale: preferencia de producto acordada.  
   - El kebab `tia-chatbot` queda solo para path/URL de repo.

3. **UI / mensajes CLI / prompt: `TIA`**  
   - Rationale: es la abreviatura que el usuario ve como nombre del asistente.  
   - Alternativa rechazada: “Tía” (homófono incorrecto; no es el significado).

4. **Sin alias `TeaChatbot`**  
   - Rationale: consumo solo interno al monorepo; alias alarga deuda.  
   - Alternativa: alias deprecado — innecesario para este MVP.

5. **Búsqueda dirigida, no replace global de `tea`**  
   - Targets: `TeaChatbot`, `Téa`, `Tea Chatbot`, variable `tea` en entrypoints.  
   - Rationale: evita falsos positivos (`create`, etc.).

## Risks / Trade-offs

- [Referencias residuales a Téa/Tea] → Mitigación: checklist de grep post-cambio en `.py`/`.md` del proyecto (excluir `.cursor` skills genéricos y `venv`).
- [Tests rotos por import viejo] → Mitigación: actualizar `tests/test_chatbot.py` en el mismo change.
- [Prompt sigue presentando Téa si se olvida] → Mitigación: task explícita sobre `system_prompt.md`.

## Migration Plan

1. Aplicar renames en código y tests.
2. Actualizar prompt y docs.
3. Verificar con grep que no queden `TeaChatbot` / `Téa` en fuentes del producto.
4. Ejecutar test básico si el entorno lo permite.
5. Rollback: revert del commit (cambio puramente textual/símbolos).

## Open Questions

- Ninguna bloqueante. Opcional futuro: mencionar “TIA = Trama IA” en el prompt de identidad.
