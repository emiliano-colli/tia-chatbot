# Project Context - Tea Chatbot

## 1. Contexto general del producto

Este proyecto implementa un asistente virtual de consulta para TRAMA y Comunidad Maternar. Su objetivo es responder preguntas sobre talleres, servicios, cronograma y otros contenidos institucionales a partir de una base de conocimiento local y un prompt de sistema.

El producto se presenta en tres formas de interacción:
- CLI: ejecución por terminal mediante Python.
- Web UI: interfaz Gradio para chat en navegador.
- API: backend HTTP con FastAPI para integrar el chatbot en otros canales.

El proyecto está pensado como un MVP simple, orientado a demostrar el flujo de conversación con un modelo LLM y contenido de dominio cargado desde archivos Markdown.

## 2. Stack técnico

- Lenguaje: Python 3.x
- Frameworks principales:
  - OpenAI Python SDK para acceso al modelo GPT
  - FastAPI para la API HTTP
  - Gradio para la interfaz web conversational
  - Pydantic para validación de modelos de entrada/salida
- Servidor ASGI: Uvicorn
- Gestión de configuración: python-dotenv
- Herramientas de ejecución:
  - Python scripts (`main.py`, `gradio_app.py`)
  - Entorno virtual (`.venv`)
  - Instalación con `pip` y `requirements.txt`
- Pruebas: pytest (actualmente con un test básico de integración del chatbot)

### Herramientas de build / ejecución
- No hay un pipeline formal de build ni CI configurado en este momento.
- La ejecución se basa en scripts Python y dependencias instaladas por pip.

## 3. Arquitectura

La arquitectura actual es modular y sencilla, con separación básica entre:
- Presentación: CLI, Gradio y FastAPI
- Lógica de dominio: clase `TeaChatbot`
- Infraestructura: carga de configuración, prompts, knowledge base, logging y cliente OpenAI

### Estructura general
- `src/`: lógica principal del chatbot
  - `chatbot.py`: núcleo del flujo conversacional
  - `config.py`: configuración cargada desde variables de entorno
  - `knowledge/`: contenido base del dominio
  - `prompts/`: prompt de sistema
  - `utils/`: utilidades compartidas
- `app/`: adaptadores de interfaz HTTP
- `tests/`: pruebas
- `main.py`: entrada por consola
- `gradio_app.py`: entrada por interfaz Gradio

### Estilo arquitectónico
No se implementa una arquitectura formal tipo hexagonal ni clean architecture completa. El diseño es más cercano a una arquitectura modular en capas simple:
- Capa de presentación: entradas por consola, Gradio y API
- Capa de aplicación: `TeaChatbot`
- Capa de infraestructura: OpenAI, ficheros Markdown, logging, .env

## 4. Convenciones del proyecto

### Nombres
- Módulos y archivos en snake_case
- Clases en PascalCase
- Funciones y métodos en snake_case
- Constantes en MAYÚSCULAS cuando son globales

### Estructura de carpetas
- `src/` para el núcleo del sistema
- `app/` para adaptadores de interfaz
- `tests/` para pruebas
- `Datos/` parece ser un área de datos o recursos de apoyo, pero actualmente no está integrada de forma explícita en la lógica principal

### Manejo de errores
- Los errores de acceso al modelo se capturan en `TeaChatbot.ask()` y se traducen a un mensaje amigable para el usuario.
- La carga de archivos de prompt y conocimiento falla con `FileNotFoundError` si no existen.
- La configuración exige la presencia de `OPENAI_API_KEY` al inicializar la app.

### Logging
- Se utiliza un logger simple basado en `logging.StreamHandler` hacia stdout.
- No hay un estándar avanzado de logging estructurado ni niveles por entorno.

## 5. Patrones y estilos de diseño usados

El proyecto no aplica un patrón formal complejo como CQRS, repositorios o DDD completo. Sin embargo, se observan algunos patrones prácticos:

- Servicio de dominio: `TeaChatbot` actúa como orchestrator del flujo conversacional.
- Carga de dependencias por módulo: prompt, conocimiento y configuración se cargan desde módulos separados.
- Gestión de sesión en memoria: cada sesión conserva historial conversacional para el contexto del modelo.
- Inversión de dependencias simple: el chatbot depende de interfaces abstractas implícitas (cliente OpenAI, loaders, configuración), no de implementaciones hardcodeadas directamente en cada punto.

## 6. Flujos principales del producto

### Flujo 1: interacción por consola
1. Se instancia `TeaChatbot`.
2. Se carga el prompt de sistema y la base de conocimiento.
3. El usuario envía un mensaje desde la terminal.
4. El sistema construye el historial de la sesión.
5. Se envía la conversación al modelo OpenAI.
6. Se devuelve la respuesta al usuario y se registra en la sesión.

### Flujo 2: interacción por API HTTP
1. El cliente envía una solicitud `POST /chat` con `session_id` y `message`.
2. FastAPI valida el cuerpo con Pydantic.
3. El chatbot responde con la respuesta generada por el modelo.
4. El endpoint `/reset/{session_id}` reinicia la sesión.

### Flujo 3: interacción por Gradio
1. La interfaz Gradio llama a `chat_fn`.
2. Se reutiliza el mismo `TeaChatbot` para contestar al usuario.
3. La respuesta se muestra directamente en la UI web.

### Flujo 4: carga de conocimiento
1. Se leen los archivos `system_prompt.md` y `cronograma.md` desde `src/prompts/` y `src/knowledge/`.
2. El contenido se incorpora al contexto del modelo antes de cada interacción.

## 7. Integraciones críticas

### Proveedor de IA
- OpenAI GPT mediante `openai.OpenAI`.
- Requiere `OPENAI_API_KEY` configurado en variables de entorno.
- El modelo configurable mediante `MODEL_NAME`.

### Configuración y entorno
- La configuración se lee desde `.env` usando `python-dotenv`.
- Se valida la existencia de la API key al importar el módulo de configuración.

### Persistencia y almacenamiento
- Actualmente no hay base de datos ni almacenamiento persistente.
- La memoria de sesiones es en memoria RAM durante la ejecución del proceso.

### Integraciones de interfaz
- FastAPI expone endpoints para chat y reset.
- Gradio ofrece una UI web simple.
- La interacción por consola sirve como modo de prueba y desarrollo.

## 8. Riesgos y observaciones importantes

- El sistema depende fuertemente de una API externa (OpenAI).
- No hay autenticación ni autorización implementadas.
- No hay aún persistencia de conversaciones, ni histórico duradero, ni trazabilidad de las conversaciones.
- La arquitectura es funcional pero todavía bastante simple para escalar.
- La configuración es mínima y podría mejorarse con un enfoque más robusto de settings y ambientes.
- No hay notificaciones por el interés del que consume el chat.

## 9. Resumen para OpenSpec / SDD

Este proyecto es un chatbot modular en Python con una arquitectura simple en capas, orientado a respuestas basadas en contenido local y un modelo LLM. El punto de entrada principal es la clase `TeaChatbot`, y la integración crítica actual es la conexión con OpenAI.

Para futuras fases, el proyecto podría evolucionar hacia una arquitectura más explícita de dominio, con separación de casos de uso, servicios de aplicación, repositorios y configuración más robusta.
