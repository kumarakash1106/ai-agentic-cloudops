
from backend.agents.workflow import run_investigation
from backend.agents.state import IncidentState

incident: IncidentState = {
    "title": "Checkout API latency increased",
    "description": (
        "Checkout requests became slow after "
        "deployment checkout-v42."
    ),
    "service": "checkout",
    "status": "received"
}

result = run_investigation(incident)

print("=== INCIDENT INVESTIGATION ===")
print("Title:", result["title"])
print("Service:", result["service"])
print("Status:", result["status"])

print("\n=== EVIDENCE SUMMARY ===")
print("Matching logs:", result["log_count"])
print("Matching metric records:", result["metric_count"])

for item in result["evidence"]:
    print(f"\n[{item['source']}] {item['content']}")

print("\n=== RELEVANT RUNBOOKS ===")

for item in result["runbooks"]:
    print(
        f"Document: {item['document']} "
        f"(keyword score: {item['score']})"
    )

print("\nWorkflow test completed!")
