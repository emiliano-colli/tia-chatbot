# Project Context - TIA Chatbot

## 1. Contexto general del producto

Este proyecto implementa un asistente virtual de consulta para TRAMA y Comunidad Maternar. Su objetivo es responder preguntas sobre talleres, servicios, cronograma y otros contenidos institucionales a partir de una base de conocimiento local y un prompt de sistema.

El producto se presenta en tres formas de interacciÃ³n:
- CLI: ejecuciÃ³n por terminal mediante Python.
- Web UI: interfaz Gradio para chat en navegador.
- API: backend HTTP con FastAPI para integrar el chatbot en otros canales.

El proyecto estÃ¡ pensado como un MVP simple, orientado a demostrar el flujo de conversaciÃ³n con un modelo LLM y contenido de dominio cargado desde archivos Markdown.

## 2. Stack tÃ©cnico

- Lenguaje: Python 3.x
- Frameworks principales:
  - OpenAI Python SDK para acceso al modelo GPT
  - FastAPI para la API HTTP
  - Gradio para la interfaz web conversational
  - Pydantic para validaciÃ³n de modelos de entrada/salida
- Servidor ASGI: Uvicorn
- GestiÃ³n de configuraciÃ³n: python-dotenv
- Herramientas de ejecuciÃ³n:
  - Python scripts (`main.py`, `gradio_app.py`)
  - Entorno virtual (`.venv`)
  - InstalaciÃ³n con `pip` y `requirements.txt`
- Pruebas: pytest (actualmente con un test bÃ¡sico de integraciÃ³n del chatbot)

### Herramientas de build / ejecuciÃ³n
- No hay un pipeline formal de build ni CI configurado en este momento.
- La ejecuciÃ³n se basa en scripts Python y dependencias instaladas por pip.

## 3. Arquitectura

La arquitectura actual es modular y sencilla, con separaciÃ³n bÃ¡sica entre:
- PresentaciÃ³n: CLI, Gradio y FastAPI
- LÃ³gica de dominio: clase `TiaChatbot`
- Infraestructura: carga de configuraciÃ³n, prompts, knowledge base, logging y cliente OpenAI

### Estructura general
- `src/`: lÃ³gica principal del chatbot
  - `chatbot.py`: nÃºcleo del flujo conversacional
  - `config.py`: configuraciÃ³n cargada desde variables de entorno
  - `knowledge/`: contenido base del dominio
  - `prompts/`: prompt de sistema
  - `utils/`: utilidades compartidas
- `app/`: adaptadores de interfaz HTTP
- `tests/`: pruebas
- `main.py`: entrada por consola
- `gradio_app.py`: entrada por interfaz Gradio

### Estilo arquitectÃ³nico
No se implementa una arquitectura formal tipo hexagonal ni clean architecture completa. El diseÃ±o es mÃ¡s cercano a una arquitectura modular en capas simple:
- Capa de presentaciÃ³n: entradas por consola, Gradio y API
- Capa de aplicaciÃ³n: `TiaChatbot`
- Capa de infraestructura: OpenAI, ficheros Markdown, logging, .env

## 4. Convenciones del proyecto

### Nombres
- MÃ³dulos y archivos en snake_case
- Clases en PascalCase
- Funciones y mÃ©todos en snake_case
- Constantes en MAYÃšSCULAS cuando son globales

### Estructura de carpetas
- `src/` para el nÃºcleo del sistema
- `app/` para adaptadores de interfaz
- `tests/` para pruebas
- `Datos/` parece ser un Ã¡rea de datos o recursos de apoyo, pero actualmente no estÃ¡ integrada de forma explÃ­cita en la lÃ³gica principal

### Manejo de errores
- Los errores de acceso al modelo se capturan en `TiaChatbot.ask()` y se traducen a un mensaje amigable para el usuario.
- La carga de archivos de prompt y conocimiento falla con `FileNotFoundError` si no existen.
- La configuraciÃ³n exige la presencia de `OPENAI_API_KEY` al inicializar la app.

### Logging
- Se utiliza un logger simple basado en `logging.StreamHandler` hacia stdout.
- No hay un estÃ¡ndar avanzado de logging estructurado ni niveles por entorno.

## 5. Patrones y estilos de diseÃ±o usados

El proyecto no aplica un patrÃ³n formal complejo como CQRS, repositorios o DDD completo. Sin embargo, se observan algunos patrones prÃ¡cticos:

- Servicio de dominio: `TiaChatbot` actÃºa como orchestrator del flujo conversacional.
- Carga de dependencias por mÃ³dulo: prompt, conocimiento y configuraciÃ³n se cargan desde mÃ³dulos separados.
- GestiÃ³n de sesiÃ³n en memoria: cada sesiÃ³n conserva historial conversacional para el contexto del modelo.
- InversiÃ³n de dependencias simple: el chatbot depende de interfaces abstractas implÃ­citas (cliente OpenAI, loaders, configuraciÃ³n), no de implementaciones hardcodeadas directamente en cada punto.

## 6. Flujos principales del producto

### Flujo 1: interacciÃ³n por consola
1. Se instancia `TiaChatbot`.
2. Se carga el prompt de sistema y la base de conocimiento.
3. El usuario envÃ­a un mensaje desde la terminal.
4. El sistema construye el historial de la sesiÃ³n.
5. Se envÃ­a la conversaciÃ³n al modelo OpenAI.
6. Se devuelve la respuesta al usuario y se registra en la sesiÃ³n.

### Flujo 2: interacciÃ³n por API HTTP
1. El cliente envÃ­a una solicitud `POST /chat` con `session_id` y `message`.
2. FastAPI valida el cuerpo con Pydantic.
3. El chatbot responde con la respuesta generada por el modelo.
4. El endpoint `/reset/{session_id}` reinicia la sesiÃ³n.

### Flujo 3: interacciÃ³n por Gradio
1. La interfaz Gradio llama a `chat_fn`.
2. Se reutiliza el mismo `TiaChatbot` para contestar al usuario.
3. La respuesta se muestra directamente en la UI web.

### Flujo 4: carga de conocimiento
1. Se leen los archivos `system_prompt.md` y `cronograma.md` desde `src/prompts/` y `src/knowledge/`.
2. El contenido se incorpora al contexto del modelo antes de cada interacciÃ³n.

## 7. Integraciones crÃ­ticas

### Proveedor de IA
- OpenAI GPT mediante `openai.OpenAI`.
- Requiere `OPENAI_API_KEY` configurado en variables de entorno.
- El modelo configurable mediante `MODEL_NAME`.

### ConfiguraciÃ³n y entorno
- La configuraciÃ³n se lee desde `.env` usando `python-dotenv`.
- Se valida la existencia de la API key al importar el mÃ³dulo de configuraciÃ³n.

### Persistencia y almacenamiento
- Actualmente no hay base de datos ni almacenamiento persistente.
- La memoria de sesiones es en memoria RAM durante la ejecuciÃ³n del proceso.

### Integraciones de interfaz
- FastAPI expone endpoints para chat y reset.
- Gradio ofrece una UI web simple.
- La interacciÃ³n por consola sirve como modo de prueba y desarrollo.

## 8. Riesgos y observaciones importantes

- El sistema depende fuertemente de una API externa (OpenAI).
- No hay autenticaciÃ³n ni autorizaciÃ³n implementadas.
- No hay aÃºn persistencia de conversaciones, ni histÃ³rico duradero, ni trazabilidad de las conversaciones.
- La arquitectura es funcional pero todavÃ­a bastante simple para escalar.
- La configuraciÃ³n es mÃ­nima y podrÃ­a mejorarse con un enfoque mÃ¡s robusto de settings y ambientes.
- No hay notificaciones por el interÃ©s del que consume el chat.

## 9. Resumen para OpenSpec / SDD

Este proyecto es un chatbot modular en Python con una arquitectura simple en capas, orientado a respuestas basadas en contenido local y un modelo LLM. El punto de entrada principal es la clase `TiaChatbot`, y la integraciÃ³n crÃ­tica actual es la conexiÃ³n con OpenAI.

Para futuras fases, el proyecto podrÃ­a evolucionar hacia una arquitectura mÃ¡s explÃ­cita de dominio, con separaciÃ³n de casos de uso, servicios de aplicaciÃ³n, repositorios y configuraciÃ³n mÃ¡s robusta.
