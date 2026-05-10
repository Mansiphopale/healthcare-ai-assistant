import os
import logging
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from app.config import DATA_FOLDER, VECTOR_STORE_PATH, EMBEDDING_MODEL

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_documents():
    """Load all .txt files from the data folder."""
    docs = []
    for filename in os.listdir(DATA_FOLDER):
        if filename.endswith(".txt"):
            filepath = os.path.join(DATA_FOLDER, filename)
            try:
                loader = TextLoader(filepath, encoding="utf-8")
                loaded = loader.load()
                # Tag each doc with its source filename
                for doc in loaded:
                    doc.metadata["source"] = filename
                docs.extend(loaded)
                logger.info(f"Loaded: {filename}")
            except Exception as e:
                logger.error(f"Failed to load {filename}: {e}")
    logger.info(f"Total documents loaded: {len(docs)}")
    return docs

def split_documents(docs):
    """Split documents into chunks."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n---\n\n", "\n\n", "\n", " "]
    )
    chunks = splitter.split_documents(docs)
    # Use only first 500 chunks for faster demo deployment
    chunks = chunks[:500]
    logger.info(f"Total chunks created: {len(chunks)}")
    return chunks

def get_embedding_function():
    """Return the embedding model."""
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

def build_vector_store(chunks):
    """Build and persist ChromaDB vector store."""
    embedding_fn = get_embedding_function()
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_fn,
        persist_directory=VECTOR_STORE_PATH
    )
    logger.info(f"Vector store saved to: {VECTOR_STORE_PATH}")
    return vector_store

def load_vector_store():
    """Load existing ChromaDB vector store."""
    embedding_fn = get_embedding_function()
    vector_store = Chroma(
        persist_directory=VECTOR_STORE_PATH,
        embedding_function=embedding_fn
    )
    logger.info("Vector store loaded successfully.")
    return vector_store

def ingest():
    """Full ingestion pipeline."""
    logger.info("Starting ingestion pipeline...")
    docs = load_documents()
    if not docs:
        raise ValueError("No documents found in data folder.")
    chunks = split_documents(docs)
    vector_store = build_vector_store(chunks)
    logger.info("Ingestion complete!")
    return len(chunks)