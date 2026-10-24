
from backend.agents.signals import inspect_signals


incident = {
    "title": "Checkout API latency increased",
    "description": (
        "Checkout requests became slow "
        "after deployment checkout-v42."
    ),
    "service": "checkout"
}

result = inspect_signals(incident)

print("Matching metric count:", result["metric_count"])
print("\nMetric evidence:")

for item in result["evidence"]:
    print(item["content"])
