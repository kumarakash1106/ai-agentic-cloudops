
from backend.agents.logs import investigate_logs


incident = {
    "title": "Checkout API latency increased",
    "description": "Checkout requests became slow after deployment checkout-v42.",
    "service": "checkout"
}

result = investigate_logs(incident)

print("Matching log count:", result["log_count"])
print("\nEvidence:")

for item in result["evidence"]:
    print(f"[{item['level']}] {item['service']}: {item['content']}")
