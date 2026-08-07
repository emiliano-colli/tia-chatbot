## Context

`TiaChatbot.ask()` hoy hace un único `chat.completions.create` sin tools. El system prompt + knowledge se fijan al inicio de sesión. El cronograma de TRAMA está en Buenos Aires y las consultas usan lenguaje relativo (“hoy”, “mañana”, “esta semana”), pero el modelo no tiene reloj.

Decisiones ya acordadas: tool on-demand; TZ fija `America/Buenos_Aires`; formato español con día de semana + fecha + hora; uso en toda interpretación temporal; prompt que prohíbe inventar la fecha.

## Goals / Non-Goals

**Goals:**
- Exponer `get_current_datetime` como tool de OpenAI.
- Ejecutar un loop mínimo de tool-calling en `ask()` hasta obtener respuesta de texto.
- Guiar al modelo vía system prompt para llamar la tool ante interpretación temporal.
- Formatear la salida en español con timezone de Buenos Aires, sin dependencias nuevas.

**Non-Goals:**
- Inyectar la fecha en el system prompt en cada turno (alternativa A descartada).
- Otras tools (cupos, clima, etc.).
- Persistencia de timezone por usuario o configuración multi-zona.
- Cambiar contratos HTTP de FastAPI / Gradio / CLI.
- Librerías nuevas de i18n o dateutil.

## Decisions

1. **Tool on-demand vía OpenAI function calling**  
   - Rationale: el modelo decide cuándo necesita la fecha; no paga tokens de “ahora” en cada mensaje.  
   - Alternativa: inyección fija cada turno — más simple pero menos alineada al pedido.

2. **Módulo dedicado `src/tools/datetime_tool.py` (o similar)**  
   - Contiene: definición del schema de la tool, función que calcula/formatea, y registro exportable para el chatbot.  
   - Rationale: mantiene `chatbot.py` como orchestrator y facilita test unitario del formato/TZ.  
   - Alternativa: todo inline en `chatbot.py` — más acoplado.

3. **Timezone fija `ZoneInfo("America/Buenos_Aires")`**  
   - Rationale: ubicación de TRAMA; evita drift si el host corre en UTC.  
   - En Windows, Python 3.9+ con `tzdata` puede ser necesario; si el entorno falla al resolver la zona, documentar/instalar `tzdata` solo si hace falta (excepción justificada a “no libs nuevas”). Preferir stdlib primero.

4. **Formato humano en español**  
   - Ejemplo objetivo: `viernes 7 de agosto de 2026, 16:19` (día + fecha + hora).  
   - Implementación: nombres de días/meses en español vía mapa local o `locale` si es fiable; preferir mapa explícito para evitar dependencia de locale del OS.

5. **Loop de tools con tope pequeño (p. ej. 3 iteraciones)**  
   - Flujo: create → si `tool_calls` → append assistant + tool results → create de nuevo → hasta `content` o tope.  
   - Rationale: evita loops infinitos; esta tool no debería necesitar más de una llamada.

6. **Prompt**  
   - Agregar regla: ante “hoy/mañana/esta semana” u otra interpretación temporal, llamar `get_current_datetime`; no inventar la fecha; cruzar resultado con el cronograma.

## Risks / Trade-offs

- [El modelo no llama la tool] → Mitigación: instrucción explícita en system prompt + descripción clara de la tool; tests manuales con prompts temporales.
- [ZoneInfo falla en Windows sin tzdata] → Mitigación: probar en el venv; si falla, agregar `tzdata` a `requirements.txt` con justificación.
- [Más latencia / costo por 2 llamadas LLM] → Mitigación: solo en preguntas temporales; aceptable para MVP.
- [Locale del OS inconsistente] → Mitigación: mapas fijos ES para día/mes.

## Migration Plan

1. Implementar tool + loop + prompt.
2. Tests unitarios del formateo.
3. Smoke manual: “¿qué día es hoy?”, “¿hay yoga mañana?”.
4. Rollback: revert del change (sin migración de datos).

## Open Questions

- Ninguna bloqueante. Pendiente solo verificar en implementación si hace falta `tzdata` en Windows.
