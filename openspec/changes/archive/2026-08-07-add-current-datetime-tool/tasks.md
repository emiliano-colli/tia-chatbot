## 1. Datetime tool module

- [x] 1.1 Crear `src/tools/datetime_tool.py` con `get_current_datetime()` usando `ZoneInfo("America/Buenos_Aires")` y formato español (día + fecha + hora)
- [x] 1.2 Exportar el schema OpenAI de la tool `get_current_datetime` (sin parámetros) y un dispatcher para ejecutarla por nombre
- [x] 1.3 Verificar `ZoneInfo` en el venv Windows; si falla, agregar `tzdata` a `requirements.txt` con justificación

## 2. Chatbot tool loop and prompt

- [x] 2.1 Extender `TiaChatbot.ask()` para enviar `tools`, manejar `tool_calls` (tope de iteraciones) y devolver el `content` final
- [x] 2.2 Actualizar `src/prompts/system_prompt.md` con la regla de usar la tool para interpretaciones temporales y no inventar la fecha

## 3. Tests and verification

- [x] 3.1 Agregar test unitario del formateo/timezone de `get_current_datetime` (día en español, zona BA)
- [x] 3.2 Ejecutar tests relevantes y smoke manual breve si el entorno lo permite
