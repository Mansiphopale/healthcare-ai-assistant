import logging
from datetime import datetime, timedelta
import random
from app.rag import answer_question

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Keywords that trigger tool-based responses instead of RAG
APPOINTMENT_KEYWORDS = [
    "appointment", "book", "schedule", "slot", "available",
    "booking", "visit", "consultation", "reserve"
]

EMERGENCY_KEYWORDS = [
    "emergency", "urgent", "911", "ambulance", "critical",
    "chest pain", "heart attack", "stroke", "overdose"
]

# Mock departments
DEPARTMENTS = [
    "Cardiology", "Dermatology", "Neurology",
    "Orthopedics", "Pediatrics", "General Medicine"
]

def detect_intent(question: str) -> str:
    """Detect the intent of the question."""
    question_lower = question.lower()

    if any(kw in question_lower for kw in EMERGENCY_KEYWORDS):
        return "emergency"

    if any(kw in question_lower for kw in APPOINTMENT_KEYWORDS):
        return "appointment"

    return "rag"

def check_available_slots(department: str, date: str) -> dict:
    """Mock tool: Check available appointment slots."""
    # Generate mock time slots
    base_time = datetime.now().replace(hour=9, minute=0, second=0)
    slots = []
    for i in range(4):
        slot_time = base_time + timedelta(hours=i * 2)
        slots.append(slot_time.strftime("%I:%M %p"))

    # Randomly mark some as available
    available = [s for s in slots if random.random() > 0.3]

    return {
        "department": department,
        "date": date,
        "available_slots": available if available else ["No slots available"],
        "note": "Please call the clinic to confirm your booking."
    }

def extract_department(question: str) -> str:
    """Try to extract department from question."""
    question_lower = question.lower()
    for dept in DEPARTMENTS:
        if dept.lower() in question_lower:
            return dept
    return "General Medicine"

def handle_appointment(question: str) -> dict:
    """Handle appointment booking intent."""
    department = extract_department(question)
    date = datetime.now().strftime("%A, %B %d %Y")
    slots_info = check_available_slots(department, date)

    answer = (
        f"I can check mock appointment availability for you.\n\n"
        f"Department: {slots_info['department']}\n"
        f"Date: {slots_info['date']}\n"
        f"Available slots: {', '.join(slots_info['available_slots'])}\n\n"
        f"Note: {slots_info['note']}"
    )

    return {
        "answer": answer,
        "sources": [{"document": "mock_appointment_tool", "chunk": "Appointment scheduling system"}],
        "confidence": "high",
        "intent": "appointment"
    }

def handle_emergency(question: str) -> dict:
    """Handle emergency intent."""
    return {
        "answer": (
            "[URGENT] This sounds like a medical emergency.\n\n"
            "Please call 911 or your local emergency number immediately.\n"
            "Do not rely on this assistant for emergency medical guidance.\n"
            "Go to the nearest emergency room if needed."
        ),
        "sources": [],
        "confidence": "high",
        "intent": "emergency"
    }

def run_agent(question: str) -> dict:
    """Main agent router."""
    logger.info(f"Agent received question: {question}")

    intent = detect_intent(question)
    logger.info(f"Detected intent: {intent}")

    if intent == "emergency":
        return handle_emergency(question)

    elif intent == "appointment":
        return handle_appointment(question)

    else:
        # Default: use RAG pipeline
        result = answer_question(question)
        result["intent"] = "rag"
        return result