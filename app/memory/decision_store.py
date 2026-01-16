from datetime import datetime

# In-memory store (we'll upgrade to DB later)
DECISION_LOG = []


def store_decision(decision: dict):
    decision["timestamp"] = datetime.utcnow().isoformat()
    DECISION_LOG.append(decision)


def get_all_decisions():
    return DECISION_LOG
