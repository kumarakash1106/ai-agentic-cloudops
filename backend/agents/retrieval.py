
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
RUNBOOK_DIR = PROJECT_ROOT / "data" / "runbooks"


def search_runbooks(query: str, limit: int = 3) -> list[dict]:
    """
    Search Markdown runbooks using simple keyword overlap.
    Higher scores indicate more matching words.
    """
    query_tokens = set(
        re.findall(r"\b[a-z0-9]+\b", query.lower())
    )

    results = []

    for path in RUNBOOK_DIR.glob("*.md"):
        content = path.read_text(encoding="utf-8")

        document_tokens = set(
            re.findall(r"\b[a-z0-9]+\b", content.lower())
        )

        score = len(query_tokens & document_tokens)

        if score > 0:
            results.append({
                "document": path.name,
                "content": content,
                "score": score
            })

    results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return results[:limit]
