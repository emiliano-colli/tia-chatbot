## 1. Domain and entrypoints

- [x] 1.1 Renombrar clase `TeaChatbot` → `TiaChatbot` en `src/chatbot.py`
- [x] 1.2 Actualizar imports e instancias en `main.py` (clase + variable `tea` → `tia` + mensajes CLI `TIA`)
- [x] 1.3 Actualizar imports e instancias en `gradio_app.py` y `app/api.py` (incl. título FastAPI `TIA Chatbot API`)
- [x] 1.4 Actualizar `tests/test_chatbot.py` para usar `TiaChatbot`

## 2. Identity and documentation

- [x] 2.1 Actualizar `src/prompts/system_prompt.md`: nombre del asistente a `TIA`
- [x] 2.2 Actualizar `README.md` a título/producto `TIA Chatbot`
- [x] 2.3 Actualizar `openspec/project.md`: reemplazar Tea/Téa/`TeaChatbot` por TIA / TIA Chatbot / `TiaChatbot`

## 3. Verification

- [x] 3.1 Grep en fuentes del producto (excl. `venv`, `.cursor`) para confirmar ausencia de `TeaChatbot`, `Téa` y branding Tea/TEA residual
- [x] 3.2 Ejecutar el test básico del chatbot si el entorno virtual y dependencias lo permiten
