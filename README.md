# Healthcare AI Assistant

A RAG-based healthcare AI assistant built with FastAPI, ChromaDB, LangChain, and Llama 3.3 (via Groq API). It answers healthcare questions grounded strictly in provided documents, with an agentic workflow for intent routing.

## Live Demo

URL: https://healthcare-ai-assistant-production.up.railway.app

---

## Architecture

```
User Question
│
▼
┌─────────────┐
│    Agent     │  <- Intent Router
└─────────────┘
│
├── Emergency intent    --> Emergency response
├── Appointment intent  --> Mock appointment tool
└── Healthcare question --> RAG Pipeline
                              │
               ┌──────────────▼──────────────┐
               │       Vector Store           │
               │       (ChromaDB)             │
               │       Retrieve top-k         │
               └──────────────┬──────────────┘
                              │
               ┌──────────────▼──────────────┐
               │     LLM (Llama 3.3)         │
               │     via Groq API             │
               │     Generate answer          │
               └──────────────┬──────────────┘
                              │
                           Response
               (answer + sources + confidence)
```

---

## Tech Stack

| Component | Technology |
|---|---|
| Backend API | FastAPI |
| LLM | Llama 3.3 70B via Groq API (free, cloud) |
| Embeddings | all-MiniLM-L6-v2 (HuggingFace) |
| Vector Database | ChromaDB |
| RAG Framework | LangChain |
| Dataset | MedQuAD (Medical Q&A Dataset) |
| Containerization | Docker + Docker Compose |

---

## Project Structure

```
healthcare-ai-assistant/
├── app/
│   ├── main.py        # FastAPI app and endpoints
│   ├── rag.py         # RAG pipeline
│   ├── embeddings.py  # Document ingestion and vector store
│   ├── llm.py         # Groq API integration
│   ├── agent.py       # Agentic intent router
│   └── config.py      # Configuration
├── data/              # Healthcare documents (MedQuAD)
├── vector_store/      # ChromaDB persisted store
├── tests/             # Unit tests
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── .env
```

---

## Setup and Run

### Prerequisites

- Python 3.11+
- Groq API Key (free at https://console.groq.com)

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd healthcare-ai-assistant
```

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\Activate  # Windows
source venv/bin/activate  # Mac/Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set your Groq API Key

```bash
# Windows PowerShell
$env:GROQ_API_KEY="your_groq_api_key_here"

# Mac/Linux
export GROQ_API_KEY="your_groq_api_key_here"
```

### 5. Start the server

```bash
uvicorn app.main:app --host 0.0.0.0 --port 9000
```

### 6. Open in browser

```
http://localhost:9000
```

---

## API Endpoints

### GET /health

```bash
curl http://localhost:9000/health
```

Response:
```json
{
  "status": "healthy",
  "service": "Healthcare AI Assistant",
  "version": "1.0.0"
}
```

### POST /ingest

```bash
curl -X POST http://localhost:9000/ingest
```

Response:
```json
{
  "message": "Documents ingested successfully.",
  "chunks_ingested": 56538
}
```

### POST /ask

```bash
curl -X POST http://localhost:9000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What are the symptoms of diabetes?"}'
```

Response:
```json
{
  "answer": "Symptoms of diabetes include increased thirst, frequent urination...",
  "sources": [
    {
      "document": "4_MedlineplusGov_QA.txt",
      "chunk": "Q: What are the symptoms of diabetes?..."
    }
  ],
  "confidence": "high",
  "intent": "rag"
}
```

---

## Prompt Engineering Strategy

The system prompt enforces:

1. Answer only from provided context
2. Refuse to guess if answer is not in documents
3. Never provide direct medical diagnoses
4. Keep responses professional and concise
5. Always recommend consulting a healthcare professional

---

## Agentic Workflow

The agent routes questions based on detected intent:

| Intent | Trigger Keywords | Handler |
|---|---|---|
| Emergency | emergency, chest pain, heart attack | Emergency response with 911 guidance |
| Appointment | book, schedule, appointment, slot | Mock appointment tool |
| Healthcare Q&A | Everything else | RAG pipeline |

---

## Dataset

**MedQuAD** (Medical Question Answer Dataset)

- Source: https://github.com/abachaa/MedQuAD
- Categories used: CancerGov, GARD, GHR, MedlinePlus, NIDDK
- Total chunks ingested: ~56,000
- Format: XML converted to Q&A text files

---

## Docker

```bash
docker-compose up --build
```

---

## Assignment Checklist

| Requirement | Status |
|---|---|
| Document ingestion | Done |
| Vector store (ChromaDB) | Done |
| RAG pipeline | Done |
| LLM integration (Groq / Llama 3.3) | Done |
| Prompt engineering | Done |
| Agentic workflow | Done |
| REST API (FastAPI) | Done |
| Source citations | Done |
| Error handling and logging | Done |
| Docker + Docker Compose | Done |
| Frontend UI (bonus) | Done |
| Local then cloud LLM (bonus) | Done |
| Live deployment on Railway (bonus) | Done |

---

## Limitations and Future Improvements

- Currently uses CPU for embeddings (GPU would be faster)
- Mock appointment tool does not connect to a real system
- No authentication on API endpoints
- Could add re-ranking for better retrieval quality
- Could add streaming responses for better UX
- PHI/HIPAA compliance would require encrypted storage and access controls
