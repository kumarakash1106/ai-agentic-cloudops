
from backend.agents.retrieval import search_runbooks

query = (
    "checkout API latency increased "
    "database connection pool errors"
)

results = search_runbooks(query)

print("Matching runbooks:", len(results))

for item in results:
    print("\nDocument:", item["document"])
    print("Keyword score:", item["score"])
    print("First 300 characters:")
    print(item["content"][:300])
