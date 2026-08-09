## 1. LLM session summary

- [x] 1.1 Implementar resumen estructurado (nombre, teléfono, intereses) vía OpenAI sobre el diálogo user/TIA, con prompt estricto y parseo JSON seguro
- [x] 1.2 Integrar el resumen LLM en el armado del PING / `end_session`, con fallback heurístico si falla la llamada o el parseo

## 2. Tests and verification

- [x] 2.1 Actualizar/agregar tests del caso real (nombre+tel juntos; interés vía menú `8` / Yoga Postparto) con LLM mockeado
- [x] 2.2 Ejecutar tests unitarios relevantes y ajustar si hace falta
