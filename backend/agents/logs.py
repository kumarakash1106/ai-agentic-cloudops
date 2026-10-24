
import json
from pathlib import Path


# Find the project's data folder reliably
PROJECT_ROOT = Path(__file__).resolve().parents[2]
LOGS_FILE = PROJECT_ROOT / "data" / "logs.json"


def investigate_logs(state: dict) -> dict:
    """
    Read application logs and return entries
    matching the incident's service.
    """
    service = state["service"].strip().lower()

    with LOGS_FILE.open("r", encoding="utf-8") as file:
        logs = json.load(file)

    matching_logs = [
        log for log in logs
        if log.get("service", "").strip().lower() == service
    ]

    evidence = [
        {
            "source": "synthetic_logs",
            "service": log["service"],
            "timestamp": log.get("timestamp"),
            "level": log.get("level", "UNKNOWN"),
            "content": log["message"]
        }
        for log in matching_logs
    ]

    return {
        "evidence": evidence,
        "log_count": len(evidence)
    }
