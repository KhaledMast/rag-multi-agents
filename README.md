# 🤖 rag-multi-agents

> A modular RAG pipeline designed for upcoming multi-agent orchestration and advanced retrieval.

---

## 📋 Requirements

* **Python:** 3.12+
* **Package Manager:** `uv` (recommended)
* **Containers:** Docker & Docker Compose

---

## ⚙️ Installation & Setup

### 1. Environment Setup (via MiniConda)

Follow these steps to isolate your environment and prepare the optimized package installer:

```bash
# Create a fresh Python 3.12 environment
conda create -n rag-multi-agents-app python=3.12 -y

# Activate the environment
conda activate rag-multi-agents-app

# Install 'uv' for ultra-fast dependency management
conda install -c conda-forge uv -y
```

*(Optional) Improve your terminal readability by updating your prompt style:*
```bash
export PS1="\[\033[01;32m\]\u@\h:\w\n\[\033[00m\]\$ "
```

### 2. Dependency Installation

Use `uv` to install the project dependencies instantly:
```bash
uv pip install -r requirements.txt
```

### 3. Application Configuration

Duplicate the template and fill in your application secrets:
```bash
cp .env.example .env
```

---

## 🐋 Infrastructure (Docker Services)

Launch the core infrastructure (MongoDB, Qdrant, etc.) using Docker Compose:

```bash
# Navigate to the docker infrastructure folder
cd docker

# Setup the infrastructure secrets
cp .env.example .env

# Open .env and fill in your credentials, then start the services
sudo docker compose up -d
```

---

## 🚀 Running the Application

Start the FastAPI application in development mode with live-reload enabled:

```bash
# Ensure you are back in the project root directory containing main.py
uvicorn main:app --reload --host 0.0.0.0 --port 5000
```

The server will be available at: `http://localhost:5000`

---

## 🧪 Testing & API Exploration

An official Postman collection is provided to help you test the endpoints (`/upload`, `/process`, `/ask`) right away.

📥 **Download Link:** [Postman Collection](assets/rag-multi-agents.postman_collection.json)
