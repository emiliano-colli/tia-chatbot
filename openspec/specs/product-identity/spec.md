# product-identity

## Purpose

Define la identidad de marca y naming del asistente TIA (Trama IA) en producto, UI, prompt y símbolos de código.

## Requirements

### Requirement: Product display name uses TIA Chatbot
Los títulos y nombres de producto visibles al usuario (README, documentación de proyecto, título de la API FastAPI y equivalentes) MUST usar la forma **TIA Chatbot** (espacio, sin guión). MUST NOT usar TEA, Tea, Téa ni TEA-Chatbot como nombre de producto.

#### Scenario: README product title
- **WHEN** un lector abre el `README.md` del repositorio
- **THEN** el título principal identifica el producto como TIA Chatbot

#### Scenario: FastAPI application title
- **WHEN** se inspecciona el título de la aplicación FastAPI
- **THEN** el título contiene TIA Chatbot (o equivalente que use TIA Chatbot como nombre de producto)

### Requirement: Assistant identity is TIA
La identidad conversacional del asistente (prompt de sistema y mensajes de UI/CLI dirigidos al usuario) MUST presentar el nombre **TIA**. MUST NOT presentar el asistente como Téa ni Tea.

#### Scenario: System prompt identity
- **WHEN** se carga el prompt de sistema
- **THEN** el campo de nombre del asistente es TIA

#### Scenario: CLI greeting uses TIA
- **WHEN** el usuario inicia la CLI
- **THEN** los mensajes de presentación y prefijos de respuesta usan TIA

### Requirement: Domain class follows Python naming for TIA
La clase principal del chatbot MUST llamarse `TiaChatbot`. Los entrypoints, imports y tests MUST referenciar `TiaChatbot`. MUST NOT exportar ni usar `TeaChatbot` como nombre de clase activo.

#### Scenario: Import from entrypoints
- **WHEN** `main.py`, `gradio_app.py`, `app/api.py` o `tests/test_chatbot.py` importan el chatbot
- **THEN** importan e instancian `TiaChatbot`

#### Scenario: No legacy class symbol
- **WHEN** se busca el símbolo `TeaChatbot` en el código fuente del producto
- **THEN** no hay definiciones ni referencias activas a esa clase
