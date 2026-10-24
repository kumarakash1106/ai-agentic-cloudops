
import json
from pathlib import Path


# Locate the project's data folder
PROJECT_ROOT = Path(__file__).resolve().parents[2]
METRICS_FILE = PROJECT_ROOT / "data" / "metrics.json"


def inspect_signals(state: dict) -> dict:
    """
    Read service metrics and return metrics
    matching the incident's service.
    """
    service = state["service"].strip().lower()

    with METRICS_FILE.open("r", encoding="utf-8") as file:
        metrics = json.load(file)

    matching_metrics = [
        item for item in metrics
        if item.get("service", "").strip().lower() == service
    ]

    evidence = []

    for item in matching_metrics:
        evidence.append({
            "source": "synthetic_metrics",
            "service": item["service"],
            "content": (
                f"Latency: {item['latency_ms']} ms; "
                f"Error rate: {item['error_rate']}%; "
                f"Database connection pool: "
                f"{item['db_pool_percent']}%"
            ),
            "values": {
                "latency_ms": item["latency_ms"],
                "error_rate": item["error_rate"],
                "db_pool_percent": item["db_pool_percent"]
            }
        })

    return {
        "evidence": evidence,
        "metric_count": len(evidence)
    }
