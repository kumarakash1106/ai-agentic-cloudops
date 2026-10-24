
from backend.agents.graph import investigate
from backend.agents.state import IncidentState

incident: IncidentState = {
    "title": "Checkout API latency increased",
    "description": (
        "Checkout requests became slow after "
        "deployment checkout-v42."
    ),
    "service": "checkout",
    "evidence": [],
    "runbooks": [],
    "status": "received"
}

result = investigate(incident)

print("=== LANGGRAPH INVESTIGATION ===")
print("Status:", result["status"])
print("Matching logs:", result["log_count"])
print("Matching metric records:", result["metric_count"])
print("Total evidence items:", len(result["evidence"]))

print("\n=== EVIDENCE ===")
for item in result["evidence"]:
    print(f"[{item['source']}] {item['content']}")

print("\n=== RUNBOOKS ===")
for item in result["runbooks"]:
    print(item["document"])

print("\nLangGraph test completed!")
