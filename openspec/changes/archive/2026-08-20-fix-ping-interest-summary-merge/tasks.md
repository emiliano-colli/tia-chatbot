## 1. Extractor prompt

- [x] 1.1 Actualizar `_SUMMARY_SYSTEM_PROMPT` para que pregunta por actividad, pedido de precios/horarios y familia sin elección cuenten como interés, y para no marcar inscripción/turno si no está en el diálogo

## 2. Per-field merge

- [x] 2.1 En `build_session_summary`, calcular siempre la heurística y rellenar nombre, teléfono o intereses solo cuando el LLM dejó placeholder y la heurística tiene valor

## 3. Tests

- [x] 3.1 Agregar test del transcript yoga → precios → nombre+tel con LLM `intereses: null` y aserción de que Intereses contiene yoga
- [x] 3.2 Agregar test de que un interés específico del LLM no se pisa con keywords
- [x] 3.3 Aserción de que el prompt del extractor incluye las reglas nuevas
- [x] 3.4 Ejecutar `tests/test_admin_notification.py` y ajustar si hace falta
