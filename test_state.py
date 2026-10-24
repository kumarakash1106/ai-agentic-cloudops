
from backend.agents.state import IncidentState

incident: IncidentState = {
    "title": "Checkout API latency increased",
    "description": (
        "Checkout requests became slow after deployment."
    ),
    "service": "checkout",
    "evidence": [],
    "runbooks": [],
    "status": "received"
}

print("Incident title:", incident["title"])
print("Affected service:", incident["service"])
print("Initial status:", incident["status"])
print("Incident state created successfully!")
