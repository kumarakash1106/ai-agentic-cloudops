
from langgraph.graph import StateGraph, START, END

from backend.agents.state import IncidentState
from backend.agents.logs import investigate_logs
from backend.agents.signals import inspect_signals
from backend.agents.retrieval import search_runbooks
from backend.agents.report import generate_report


def logs_node(state: IncidentState) -> dict:
    """Collect logs for the affected service."""
    result = investigate_logs(state)

    return {
        "evidence": result["evidence"],
        "log_count": result["log_count"]
    }


def metrics_node(state: IncidentState) -> dict:
    """Collect metrics and preserve existing log evidence."""
    result = inspect_signals(state)

    return {
        "evidence": (
            state.get("evidence", [])
            + result["evidence"]
        ),
        "metric_count": result["metric_count"]
    }


def runbook_node(state: IncidentState) -> dict:
    """Retrieve relevant troubleshooting documents."""
    query = (
        f"{state['title']} "
        f"{state['description']} "
        f"{state['service']}"
    )

    return {
        "runbooks": search_runbooks(query),
        "status": "investigation_complete"
    }


def report_node(state: IncidentState) -> dict:
    """Generate the final incident investigation report."""
    return generate_report(state)


builder = StateGraph(IncidentState)

builder.add_node("logs", logs_node)
builder.add_node("metrics", metrics_node)
builder.add_node("runbooks", runbook_node)
builder.add_node("report", report_node)

builder.add_edge(START, "logs")
builder.add_edge("logs", "metrics")
builder.add_edge("metrics", "runbooks")
builder.add_edge("runbooks", "report")
builder.add_edge("report", END)

investigation_graph = builder.compile()


def investigate(state: IncidentState) -> dict:
    """Execute the compiled investigation graph."""
    return investigation_graph.invoke(state)
