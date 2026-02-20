# Techculture Service Assistant — Agentic RAG Pipeline

An intelligent, AI-powered chatbot that answers questions about **Techculture's** technology services, pricing, case studies, and FAQs. Built with an **Agentic RAG (Retrieval-Augmented Generation)** architecture, where the LLM autonomously decides when to invoke domain-specific tools (e.g., a pricing estimator) and when to rely solely on retrieved knowledge-base context.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Setup & Installation](#setup--installation)
3. [Running the Application](#running-the-application)
4. [Architecture](#architecture)
5. [Component Descriptions](#component-descriptions)
6. [Tech Stack](#tech-stack)
7. [Project Structure](#project-structure)
8. [API Documentation](#api-documentation)

---

## Project Overview

This project implements an **Agentic Retrieval-Augmented Generation (RAG)** pipeline for a technology services company (Techculture). The system:

- **Ingests** company knowledge base documents (services, pricing, case studies, FAQs)
- **Chunks & embeds** documents into a FAISS vector store using HuggingFace sentence-transformers
- **Retrieves** the most relevant document chunks given a user query
- **Autonomously decides** (via LLM tool-calling) whether to invoke domain tools (e.g., pricing estimator)
- **Generates** a grounded, cited answer using the Groq-hosted Llama 3.3 70B model
- **Exposes** the pipeline as a FastAPI REST endpoint
- **Provides** a Streamlit chat UI for interactive use

---

## Setup & Installation

### Prerequisites

- **Python 3.10+** installed
- **Groq API Key** — Get one at [console.groq.com](https://console.groq.com)

### Step 1: Clone the Repository

```bash
git clone https://github.com/rahul9416/Chatbot-Assignment.git
cd Chatbot-Assignment
```

### Step 2: Create a Virtual Environment

```bash
python -m venv venv

venv\Scripts\activate

```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Create a `.env` file in the project root (or edit the existing one):

```env
GROQ_API_KEY=your_groq_api_key_here
LLM_MODEL=llama-3.3-70b-versatile
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

### Step 5: Initialize the Vector Store

```bash
python initialize.py
```

This loads all documents from `data/`, chunks them, generates embeddings, and saves the FAISS index to `vector_store/`.

---

## Running the Application

**Terminal 1 — Start the API server:**

```bash
uvicorn api:app --reload --port 8000
```

**Terminal 2 — Start the Streamlit UI:**

```bash
streamlit run app.py
```

The chat UI will open at `http://localhost:8501`.

---

## Architecture

```
┌───────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                      │
│  ┌─────────────┐         ┌──────────────────────────┐     │
│  │ Streamlit   │ HTTP    │  FastAPI REST API         │     │
│  │ Chat UI     │────────▶│  POST /ask                │     │
│  │ (app.py)    │         │  (api.py)                 │     │
│  └─────────────┘         └────────────┬─────────────┘     │
└───────────────────────────────────────┼───────────────────┘
                                        │
┌───────────────────────────────────────▼───────────────────┐
│                    ORCHESTRATION LAYER                     │
│                                                           │
│  ┌─────────────────────────────────────────────────┐      │
│  │            Agent Orchestrator (agent.py)         │      │
│  │                                                 │      │
│  │  1. Bind tools to LLM                           │      │
│  │  2. LLM decides: tool needed?                   │      │
│  │     ├── YES → Execute tool → Get output         │      │
│  │     └── NO  → Skip                              │      │
│  │  3. Pass query + tool_output to RAG pipeline    │      │
│  └────────┬────────────────────────┬───────────────┘      │
│           │                        │                      │
│     ┌─────▼──────┐    ┌───────────▼──────────────┐        │
│     │ Tool Layer │    │  RAG Pipeline             │        │
│     │            │    │  (rag_pipeline.py)        │        │
│     │ pricing_   │    │                           │        │
│     │ estimator  │    │  retrieve() → format()    │        │
│     │            │    │  → generate_answer()      │        │
│     └────────────┘    └──────────────────────────┘        │
└───────────────────────────────────────────────────────────┘
                                        │
┌───────────────────────────────────────▼───────────────────┐
│                    DATA / STORAGE LAYER                    │
│                                                           │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────────┐  │
│  │ Knowledge   │  │ FAISS       │  │ Groq API         │  │
│  │ Base        │  │ Vector      │  │ (Llama 3.3 70B)  │  │
│  │ (.md files) │  │ Store       │  │                  │  │
│  └─────────────┘  └─────────────┘  └──────────────────┘  │
└───────────────────────────────────────────────────────────┘
```

## Component Descriptions

### 1. `config.py` — Centralized Configuration

Loads all environment variables and defines system-wide constants:

- **`GROQ_API_KEY`**: API key for Groq LLM inference
- **`LLM_MODEL`**: Model identifier (`llama-3.3-70b-versatile`)
- **`EMBEDDING_MODEL`**: HuggingFace model for embeddings (`sentence-transformers/all-MiniLM-L6-v2`)
- **`VECTOR_STORE_PATH`**: Path to the persisted FAISS index
- **`DATA_DIR`**: Path to the knowledge base documents
- **`CHUNK_SIZE` / `CHUNK_OVERLAP`**: Chunking parameters (500 / 50)
- **`TOP_K`**: Number of documents to retrieve (4)

### 2. `ingestion.py` — Document Loading & Chunking

- **`load_documents()`**: Uses LangChain's `DirectoryLoader` to read all `.md` files from `data/`
- **`chunk_documents()`**: Splits documents using `RecursiveCharacterTextSplitter` with configurable chunk size and overlap
- **`run_ingestion()`**: Orchestrates the full ingestion: load → chunk → return chunks

### 3. `embeddings.py` — Embedding & Vector Store Management

- **`get_embedding_model()`**: Initializes the HuggingFace sentence-transformer model
- **`create_vector_store(chunks)`**: Creates a FAISS vector store from document chunks
- **`save_vector_store(vectorstore)`**: Persists the vector store to disk
- **`load_vector_store(path)`**: Loads a previously saved vector store

### 4. `initialize.py` — One-Time Setup Script

Runs the full initialization pipeline:

```
Load documents → Chunk documents → Create embeddings → Save FAISS vector store
```

Must be run once before querying the system.

### 5. `rag_pipeline.py` — RAG Pipeline

- **`retrieve(query)`**: Searches the FAISS vector store for the top-K most similar chunks
- **`format_context(chunks)`**: Formats retrieved chunks into a context string with source citations
- **`generate_answer(query, context, tool_output)`**: Calls the Groq LLM with system prompt + context + optional tool output
- **`ask(query, tool_output)`**: Main entry point — orchestrates retrieve → format → generate

### 6. `agent.py` — Agentic Orchestrator

- **`pricing_tool()`**: LangChain `@tool`-decorated function that wraps the pricing estimator
- **`run_agent(query)`**: The core agentic loop:
  1. Binds the pricing tool to the LLM
  2. LLM autonomously decides if a tool call is needed
  3. If yes → executes the tool → passes output to RAG pipeline
  4. If no → calls RAG pipeline directly
  5. RAG pipeline always handles final answer generation

### 7. `tools/pricing_estimator.py` — Pricing Estimation Tool

- Rule-based pricing calculator for Techculture's services
- Supports: `ai_consulting`, `digital_marketing`, `web_development`, `cloud_devops`
- Parameters: `project_type`, `duration` (months), `complexity` (low/medium/high)
- Returns structured pricing estimate with notes

### 8. `api.py` — FastAPI REST Server

- **`POST /ask`**: Accepts a JSON body `{ "question": "..." }` and returns `{ "answer": "...", "question": "..." }`
- Includes CORS middleware for cross-origin requests
- Input validation and error handling

### 9. `app.py` — Streamlit Chat UI

- Interactive chat interface with message history
- Gradient-styled header with Techculture branding
- Sends requests to the FastAPI backend
- Displays loading spinners and error messages gracefully

### 10. `data/` — Knowledge Base Documents

| File                      | Content                          |
| ------------------------- | -------------------------------- |
| `services_overview.md`    | Company overview & service lines |
| `ai_consulting.md`        | AI & ML consulting services      |
| `digital_marketing.md`    | Digital marketing services       |
| `web_app_development.md`  | Web & app development services   |
| `pricing_guide.md`        | Detailed pricing tables & models |
| `case_study_ecommerce.md` | E-commerce case study            |
| `case_study_fintech.md`   | Fintech case study               |
| `faq.md`                  | Frequently asked questions       |

---

## Tech Stack

| Layer            | Technology                     | Purpose                                     |
| ---------------- | ------------------------------ | ------------------------------------------- |
| **LLM**          | Groq (Llama 3.3 70B)           | Answer generation & tool-calling            |
| **Embeddings**   | HuggingFace `all-MiniLM-L6-v2` | Document embedding (384-dim vectors)        |
| **Vector Store** | FAISS (CPU)                    | Similarity search over embeddings           |
| **Framework**    | LangChain                      | RAG pipeline, tool binding, LLM abstraction |
| **API**          | FastAPI + Uvicorn              | REST API server                             |
| **UI**           | Streamlit                      | Interactive chat frontend                   |
| **Config**       | python-dotenv                  | Environment variable management             |
| **Validation**   | Pydantic                       | Request/response schema validation          |

---

## Project Structure

```
Chatbot-Assignment/
├── .env                        # Environment variables (API keys, model names)
├── .gitignore                  # Git ignore rules
├── requirements.txt            # Python dependencies
├── config.py                   # Centralized configuration
├── ingestion.py                # Document loading & chunking
├── embeddings.py               # Embedding model & vector store operations
├── initialize.py               # One-time initialization script
├── rag_pipeline.py             # Retrieve → Format → Generate pipeline
├── agent.py                    # Agentic orchestrator with tool-calling
├── api.py                      # FastAPI REST server
├── app.py                      # Streamlit chat UI
├── tools/
│   └── pricing_estimator.py    # Rule-based pricing calculator tool
├── data/                       # Knowledge base documents
│   ├── services_overview.md
│   ├── ai_consulting.md
│   ├── digital_marketing.md
│   ├── web_app_development.md
│   ├── pricing_guide.md
│   ├── case_study_ecommerce.md
│   ├── case_study_fintech.md
│   └── faq.md
└── vector_store/               # Persisted FAISS index (generated)
```

---

## API Documentation

### `POST /ask`

**Request Body:**

```json
{
  "question": "What AI services do you offer?"
}
```

**Success Response (200):**

```json
{
  "answer": "Techculture offers a comprehensive range of AI & ML services including...",
  "question": "What AI services do you offer?"
}
```

**Error Responses:**

- `400` — Empty question
- `500` — Internal server error

### Interactive Docs

Once the API server is running, visit:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

---

## Future Improvements

- **Document-Driven Pricing Tool** — The current pricing estimator uses a hardcoded rate table. A key improvement would be to enhance the pricing tool so it retrieves pricing information directly from the knowledge base documents (e.g., `pricing_guide.md`) via the RAG pipeline instead of relying on static values. This would ensure pricing stays in sync with the documents and allow non-technical users to update pricing by simply editing the markdown files.
- **Conversation Memory** — Add multi-turn conversation context so the assistant can handle follow-up questions like _"What about for 6 months instead?"_ without the user repeating the full query.
