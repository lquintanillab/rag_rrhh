# Chatbot de soporte FAQ con RAG (Recuperación aumentada por generación)

**Repositorio:** https://github.com/lquintanillab/rag_rrhh.git

## Contexto y propósito

En una empresa de **HR SaaS** con mucha documentación, el equipo de soporte recibe cientos de preguntas repetitivas al día sobre políticas, funcionalidades y procedimientos ya recogidos en FAQs internas y guías. Este proyecto implementa un **asistente de preguntas frecuentes** basado en **RAG**: el modelo no “memoriza” el manual entero en el prompt, sino que **recupera fragmentos relevantes** de la documentación y **genera una respuesta fundamentada** en ese contexto. Así se reduce la carga de búsqueda manual y se acelera la atención sin sustituir el criterio humano donde haga falta.

El sistema está pensado para ser **autocontenido**: dependencias declaradas en `requirements.txt`, configuración por variables de entorno (plantilla en `.env.example`) y rutas de datos resueltas respecto a la raíz del proyecto para que la indexación y las consultas funcionen igual desde distintos directorios de trabajo.

## Objetivos cumplidos

| Objetivo | Implementación |
|----------|----------------|
| **Base de conocimiento desde texto plano** | `data/faq_document.txt` se carga completo, se segmenta en fragmentos (chunks), se vectoriza con embeddings OpenAI y se persiste en **ChromaDB** (`data/chroma_db/`). |
| **≥ 20 chunks** | El documento actual produce **decenas de chunks** (p. ej. 50+ con la configuración por defecto); el tamaño y solapamiento se definen en `src/config.py`. |
| **Pipeline de consulta** | `src/query.py`: pregunta → embedding de la consulta → búsqueda por similitud en el vector store → ensamblado de contexto → respuesta con **LLM** (OpenAI). |
| **Salida JSON estructurada** | Diccionario con tres campos equivalentes a los de la rúbrica: `pregunta_usuario`, `respuesta_sistema`, `fragmentos_relacionados` (mismo rol que `user_question`, `system_answer`, `chunks_related`). |




## Requisitos

- **Python** 3.10 o superio.
- Cuenta **OpenAI** con API key válida (embeddings + chat).
- Conexión a Internet para llamadas a la API en indexación y consulta.

## Instalación y configuración

Sigue al menos estos pasos para un entorno reproducible:

1. **Clonar el repositorio** y entrar en la carpeta del proyecto:
   ```bash
   git clone https://github.com/lquintanillab/rag_rrhh.git
   cd rag_rrhh
   ```

2. **Crear y activar un entorno virtual** (recomendado):
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
   En Linux/macOS: `source .venv/bin/activate`

3. **Instalar dependencias** (versiones fijadas en el archivo):
   ```bash
   pip install -r requirements.txt
   ```

4. **Variables de entorno:** copia la plantilla y edita la clave:
   ```bash
   copy .env.example .env
   ```
   En Linux/macOS: `cp .env.example .env`

   Define al menos:
   - `OPENAI_API_KEY` — tu clave de OpenAI.
   - Opcional: `EMBEDDING_MODEL` (por defecto `text-embedding-3-small`), `CHAT_MODEL` (por defecto `gpt-4.1-mini` según `config.py`).

   En terminal (ejemplos):
   ```bash
   set OPENAI_API_KEY=tu-clave-aqui
   ```
   Linux/macOS:
   ```bash
   export OPENAI_API_KEY=tu-clave-aqui
   ```

   El código carga la clave con `os.getenv("OPENAI_API_KEY")` vía `python-dotenv` desde `.env` si existe.

## Uso

### 1. Pipeline de indexación (documento → chunks → embeddings → vector store)

Desde la raíz del repositorio:

```bash
cd src
python build_index.py
```

**Etapas (modular en funciones):** `load_document` → `chunk_documents` → `build_vector_store` (embeddings + persistencia en Chroma). Al finalizar verás mensajes con la ruta absoluta de `data/chroma_db` y el número de documentos indexados.

### 2. Pipeline de consultas (pregunta → recuperación → LLM → JSON)

```bash
cd src
python query.py
```

Escribe la pregunta cuando se solicite. La salida es **JSON** por consola (`ensure_ascii=False` para caracteres UTF-8).

**Ejemplo de pregunta:**  
`¿Cuál es el mínimo de días de vacaciones obligatorios al año?`

**Ejemplo de forma de salida** (estructura; el contenido depende del manual y del modelo):

```json
{
  "pregunta_usuario": "¿Cuál es el mínimo de días de vacaciones obligatorios al año?",
  "respuesta_sistema": "... respuesta redactada según el contexto recuperado ...",
  "fragmentos_relacionados": [
    "... primer fragmento del manual ...",
    "... segundo fragmento ..."
  ]
}
```

### 3. Evaluador

Tras obtener `respuesta_sistema` y la lista de textos de fragmentos, puedes invocar en Python:

```python
from evaluator import evaluate_response

ev = evaluate_response(pregunta, respuesta, fragmentos)
# ev["puntuacion"], ev["motivo"]
```

## Estructura del repositorio

| Ruta | Contenido |
|------|-----------|
| `data/faq_document.txt` | Documento fuente de políticas / procedimientos / producto (texto plano, UTF-8). |
| `data/chroma_db/` | Almacén vectorial generado (no versionar secretos; puede ignorarse en `.gitignore` si se desea). |
| `src/config.py` | Rutas del proyecto, modelos, `CHUNK_SIZE`, `CHUNK_OVERLAP`, `TOP_K`, carga de `.env`. |
| `src/build_index.py` | Pipeline de indexación ejecutable. |
| `src/query.py` | Pipeline de consulta RAG ejecutable. |
| `src/evaluator.py` | Evaluación heurística 0–10 + motivo. |
| `outputs/sample_queries.json` | Ejemplos de salida JSON (varias preguntas de muestra). |
| `requirements.txt` | Dependencias con versiones. |
| `.env.example` | Plantilla de variables de entorno. |
