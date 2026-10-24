
from typing import TypedDict


class IncidentState(TypedDict, total=False):
    title: str
    description: str
    service: str
    evidence: list[dict]
    runbooks: list[dict]
    log_count: int
    metric_count: int
    status: str
    final_report: str
