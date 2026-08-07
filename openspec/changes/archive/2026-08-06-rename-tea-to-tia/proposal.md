## Why

Este repositorio es una copia de TEA-Chatbot / Téa, pero el producto ahora se llama **TIA** (abreviatura de Trama IA). Hay que alinear código, UI, prompt y documentación con el nuevo nombre para evitar inconsistencias de marca e identidad del asistente.

## What Changes

- Renombrar la clase de dominio `TeaChatbot` a `TiaChatbot` y actualizar imports, tests y entrypoints.
- Reemplazar referencias visibles al usuario (`Téa`, `Téa Chatbot`, etc.) por **TIA** / **TIA Chatbot** (títulos sin guión).
- Actualizar la identidad en `system_prompt.md` para que el asistente se presente como TIA.
- Actualizar documentación del proyecto (`README.md`, `openspec/project.md`) con el naming nuevo.
- **BREAKING**: el símbolo público `TeaChatbot` deja de existir (sin alias de compatibilidad; el consumo es solo interno al repo).

## Capabilities

### New Capabilities
- `product-identity`: Naming e identidad de marca del asistente (producto, UI, prompt y símbolos de código).

### Modified Capabilities
- (ninguna — no hay specs principales aún en `openspec/specs/`)

## Impact

- Código: `src/chatbot.py`, `main.py`, `gradio_app.py`, `app/api.py`, `tests/test_chatbot.py`
- Prompt: `src/prompts/system_prompt.md`
- Docs: `README.md`, `openspec/project.md`
- API: título FastAPI (`title=...`); sin cambio de rutas ni contratos de request/response
- Dependencias: ninguna nueva
