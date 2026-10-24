
from backend.agents.state import IncidentState
from backend.agents.logs import investigate_logs
from backend.agents.signals import inspect_signals
from backend.agents.retrieval import search_runbooks


def run_investigation(state: IncidentState) -> dict:
    """
    Run the investigation tools in sequence and
    combine their findings into one result.
    """

    # Step 1: Collect logs for the affected service
    log_result = investigate_logs(state)

    # Step 2: Collect metrics for the affected service
    metric_result = inspect_signals(state)

    # Step 3: Search for relevant troubleshooting guidance
    query = (
        f"{state['title']} "
        f"{state['description']} "
        f"{state['service']}"
    )

    runbook_results = search_runbooks(query)

    # Step 4: Combine the findings
    combined_evidence = (
        log_result["evidence"]
        + metric_result["evidence"]
    )

    return {
        "title": state["title"],
        "description": state["description"],
        "service": state["service"],
        "evidence": combined_evidence,
        "runbooks": runbook_results,
        "log_count": log_result["log_count"],
        "metric_count": metric_result["metric_count"],
        "status": "investigation_complete"
    }
