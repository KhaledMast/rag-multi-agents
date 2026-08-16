# 🤖 RAG Multi-Agents

A FastAPI-based RAG application that indexes and searches document chunks with a vector database, and integrates LLM providers for generation and embeddings.

---

## Requirements

- Python 3.12+
- Docker and Docker Compose
- Optional: `uv` for package installation

---

## Environment setup

From the project root:

```bash
cd src
cp .env.exemple .env
```

Then update the values in `.env` according to your environment (MongoDB, LLM provider, vector DB, etc.).

For Docker services, copy the example file in the docker folder:

```bash
cd docker
cp .env.exemple .env
```

---

## Install dependencies

With `pip`:

```bash
cd src
pip install -r requirements.txt
```

With `uv`:

```bash
cd src
uv pip install -r requirements.txt
```

---

## Start infrastructure

```bash
cd docker
docker compose up -d
```

This starts the required infrastructure services such as MongoDB and other project dependencies.

---

## Run the API

From the project root, launch the application from the `src` folder:

```bash
cd src
uvicorn main:app --reload --host 0.0.0.0 --port 5000
```

The API will be available at:

```text
http://localhost:5000
```

---

## API routes


### Data

```http
POST /api/v1/data/upload/{project_id}
POST /api/v1/data/process/{project_id}
```

### NLP / RAG

```http
POST /api/v1/nlp/index/push/{project_id}
GET /api/v1/nlp/index/info/{project_id}
POST /api/v1/nlp/index/search/{project_id}
POST /api/v1/nlp/index/answer/{project_id}
```

---

## API testing

A Postman collection is included for manual testing:

- [src/assets/rag-multi-agents.postman_collection.json](src/assets/rag-multi-agents.postman_collection.json)

---

## Notes

This project is structured around a modular backend with:
- FastAPI for the API layer
- MongoDB for document metadata storage
- Qdrant for vector search
- LLM providers for generation and embeddings
- services and repositories organized by responsibility

This is a practical RAG backend foundation that can be extended into a more advanced multi-agent architecture.
