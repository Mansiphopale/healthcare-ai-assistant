import logging
from app.embeddings import load_vector_store
from app.llm import ask_llm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def retrieve_context(question: str, k: int = 4):
    """Retrieve top-k relevant chunks from vector store."""
    vector_store = load_vector_store()
    retriever = vector_store.as_retriever(search_kwargs={"k": k})
    docs = retriever.invoke(question)
    logger.info(f"Retrieved {len(docs)} chunks for question: {question}")
    return docs

def format_context(docs) -> str:
    """Combine retrieved docs into a single context string."""
    return "\n\n".join([doc.page_content for doc in docs])

def format_sources(docs) -> list:
    """Extract source info from retrieved docs."""
    sources = []
    seen = set()
    for doc in docs:
        source = doc.metadata.get("source", "unknown")
        chunk = doc.page_content[:200].strip()
        key = (source, chunk[:50])
        if key not in seen:
            seen.add(key)
            sources.append({
                "document": source,
                "chunk": chunk
            })
    return sources

def answer_question(question: str) -> dict:
    """Full RAG pipeline: retrieve → format → generate → respond."""
    logger.info(f"Processing question: {question}")

    try:
        # Step 1: Retrieve relevant docs
        docs = retrieve_context(question)

        if not docs:
            return {
                "answer": "I could not find this information in the provided documents.",
                "sources": [],
                "confidence": "low"
            }

        # Step 2: Format context
        context = format_context(docs)

        # Step 3: Generate answer via LLM
        answer = ask_llm(f"Context:\n{context}\n\nQuestion: {question}")

        # Step 4: Format sources
        sources = format_sources(docs)

        # Step 5: Assess confidence
        confidence = min(1.0, len(docs) / 4.0)

        return {
            "answer": answer,
            "sources": sources,
            "confidence": confidence
        }

    except Exception as e:
        logger.error(f"RAG pipeline error: {e}")
        return {
            "answer": "An error occurred while processing your question.",
            "sources": [],
            "confidence": "low"
        }