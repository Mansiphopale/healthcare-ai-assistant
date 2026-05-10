from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from contextlib import asynccontextmanager
from app.agent import run_agent
from app.embeddings import ingest
from fastapi import BackgroundTasks
from app.config import APP_HOST, APP_PORT, LOG_LEVEL

# Logging setup
logging.basicConfig(level=getattr(logging, LOG_LEVEL, logging.INFO))
logger = logging.getLogger(__name__)

# Request/Response models
class QuestionRequest(BaseModel):
    question: str

class IngestResponse(BaseModel):
    message: str
    chunks_ingested: int

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Healthcare AI Assistant starting up...")
    yield
    logger.info("Healthcare AI Assistant shutting down...")

# App initialization
app = FastAPI(
    title="Healthcare AI Assistant",
    description="A RAG-based healthcare assistant powered by Mistral via Ollama",
    version="1.0.0",
    lifespan=lifespan
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
def serve_ui():
    return FileResponse("app/static/index.html")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Endpoints ──────────────────────────────────────────

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Healthcare AI Assistant",
        "version": "1.0.0"
    }

@app.post("/ingest")
def ingest_documents(background_tasks: BackgroundTasks):
    """Ingest documents in background."""
    background_tasks.add_task(ingest)
    return {"message": "Ingestion started in background. Wait 5-10 minutes then ask questions.", "chunks_ingested": 0}

@app.post("/ask")
def ask_question(request: QuestionRequest):
    """Answer a healthcare question using RAG + agent workflow."""
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    try:
        logger.info(f"Received question: {request.question}")
        result = run_agent(request.question)
        return result
    except Exception as e:
        logger.error(f"Error processing question: {e}")
        raise HTTPException(status_code=500, detail="Failed to process question.")