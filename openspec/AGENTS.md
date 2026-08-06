# AGENTS.md

## Propósito
Este repositorio contiene un chatbot simple en Python para TRAMA y Comunidad Maternar. El objetivo de este archivo es guiar a cualquier agente de IA que trabaje aquí para mantener coherencia con el proyecto, su arquitectura actual y sus restricciones de negocio.

## Reglas de trabajo

### 1. Respetar la arquitectura actual
- Mantener la estructura modular actual: `src/` para la lógica principal, `app/` para adaptadores de interfaz y `tests/` para validaciones.
- No introducir cambios de arquitectura grandes ni patrones complejos (hexagonal, DDD, CQRS, repositorios, inyección profunda de dependencias) salvo que el pedido explícitamente lo requiera.
- Preferir cambios pequeños, localizados y fáciles de entender.

### 2. No introducir librerías nuevas sin justificación
- No agregar dependencias nuevas salvo que sean estrictamente necesarias para cumplir el requerimiento.
- Si se necesita una librería nueva, justificar por qué no se puede resolver con lo ya existente y actualizar `requirements.txt`.
- Evitar soluciones sobre-diseñadas o paquetes innecesarios.

### 3. Preguntar si hay dudas
- Si un cambio puede afectar el comportamiento esperado, la API, la configuración, la seguridad o el diseño general, preguntar antes de implementar.
- Cuando la intención del usuario sea ambigua, aclarar primero en vez de asumir.

### 4. Si tocas contratos, actualiza specs
- Si cambias contratos de API, formatos de entrada/salida, estructura de datos, prompts, comportamiento visible del chatbot o variables de entorno, actualizar también la documentación relevante.
- En este repo, eso implica revisar al menos `README.md`, `project.md` y, cuando corresponda, `tests/`.

### 5. Mantener compatibilidad y simplicidad
- No romper el flujo actual de consola, Gradio ni FastAPI salvo que se pida explícitamente.
- Priorizar cambios que preserven el funcionamiento del MVP y no introduzcan complejidad innecesaria.
- Mantener el código legible, explícito y alineado con las convenciones del proyecto.

## Convenciones del repositorio
- Usar `snake_case` para archivos, funciones y variables.
- Usar `PascalCase` para clases.
- Mantener nombres claros y descriptivos.
- Respetar la separación de responsabilidades actual entre chatbot, prompts, knowledge, configuración y utilidades.

## Prohibiciones
- No introducir nuevas librerías ni frameworks sin una justificación clara y sin actualizar `requirements.txt`.
- No reescribir la arquitectura del proyecto para adoptar patrones complejos como hexagonal, DDD, CQRS o repositorios si no se solicita explícitamente.
- No cambiar el flujo actual de consola, Gradio o FastAPI sin validar el impacto sobre el comportamiento esperado.
- No modificar contratos de API, prompts, variables de entorno o formatos de respuesta sin actualizar la documentación correspondiente.
- No hardcodear secretos, claves API o datos sensibles.
- No realizar cambios grandes por gusto cuando el pedido corresponde a una mejora o corrección pequeña y local.

## Calidad y pruebas
- Si se cambia lógica de negocio o comportamiento observable, agregar o actualizar pruebas en `tests/`.
- No introducir pruebas frágiles ni mocks innecesarios cuando se pueda validar el comportamiento real.
- Si un cambio no se puede probar fácilmente, dejarlo documentado y explicar la limitación.

## Configuración y secretos
- No hardcodear secretos ni claves API.
- Usar variables de entorno y respetar la configuración existente en `.env` y `src/config.py`.
- No exponer datos sensibles en logs, respuestas o documentación.

## Flujo recomendado para cambios
1. Entender el pedido y el alcance real.
2. Revisar el módulo afectado y el contexto del proyecto.
3. Implementar el cambio de forma mínima y coherente.
4. Actualizar tests y documentación si el cambio afecta comportamiento o contratos.
5. Verificar que no se rompió la funcionalidad existente.
