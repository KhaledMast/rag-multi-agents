# rag-multi-agents
RAG pipeline with a multi-agent orchestration layer for retrieval and generation.


## Requirements

Python 3.12

### Install Python using MiniConda

1) Download and install MiniConda.
2) Create a new environment "rag-multi-agents"
4) Install uv inside the Conda Environment
```bash
conda install -c conda-forge uv
```
3) Activate the environment:
```bash
$ conda activate rag-multi-agents-app
```

### (Optional) Setup you command line interface for better readability

```bash
export PS1="\[\033[01;32m\]\u@\h:\w\n\[\033[00m\]\$ "
```

## Installation

### Install the required packages

```bash
$ uv pip install -r requirements.txt
```

### Setup the environment variables

```bash
$ cp .env.example .env
```

## Run Docker Compose Services

```bash
$ cd docker
$ cp .env.example .env
```

- update `.env` with your credentials


```bash
$ cd docker
$ sudo docker compose up -d

## Run the FastAPI server (Development Mode)

```bash
$ uvicorn main:app --reload --host 0.0.0.0 --port 5000
```



## POSTMAN Collection

Download the POSTMAN collection from [/assets/rag-multi-agents.postman_collection.json](/assets/rag-multi-agents.postman_collection.json)