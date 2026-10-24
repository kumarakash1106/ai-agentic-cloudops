
from langgraph.graph import StateGraph, START, END

from backend.agents.state import IncidentState
from backend.agents.logs import investigate_logs
from backend.agents.signals import inspect_signals
from backend.agents.retrieval import search_runbooks

# Original deterministic report generator
from backend.agents.report import generate_report

# New Ollama-powered AI report generator
from backend.agents.llm_report import generate_ai_report


# STEP 1: Analyze incident logs
def logs_node(state: IncidentState) -> dict:
    result = investigate_logs(state)

    return {
        "evidence": result["evidence"],
        "log_count": result["log_count"],
    }


# STEP 2: Analyze system metrics
def metrics_node(state: IncidentState) -> dict:
    result = inspect_signals(state)

    return {
        "evidence": state.get("evidence", []) + result["evidence"],
        "metric_count": result["metric_count"],
    }


# STEP 3: Retrieve relevant runbooks
def runbook_node(state: IncidentState) -> dict:
    query = (
        f"{state['title']} "
        f"{state['description']} "
        f"{state['service']}"
    )

    return {
        "runbooks": search_runbooks(query),
        "status": "investigation_complete",
    }


# STEP 4: Generate an AI-powered incident report
def report_node(state: IncidentState) -> dict:
    """
    Generate an AI report using local Ollama.

    If the AI model fails or returns an empty report,
    use the original deterministic report generator.
    """

    try:
        print("Generating AI-powered incident report...")

        result = generate_ai_report(state)

        if not result.get("final_report", "").strip():
            raise ValueError("AI generated an empty report")
        
        if "Initial Assessment" not in final_report:
           final_report = final_report.replace(
            "## Incident Summary",
            "## Initial Assessment",
            1,
    )

        print("AI report generated successfully.")

        return result

    except Exception as error:
        print(f"AI report generation failed: {error}")
        print("Using deterministic report fallback.")

        return generate_report(state)


# STEP 5: Build the LangGraph workflow
builder = StateGraph(IncidentState)

builder.add_node("logs", logs_node)
builder.add_node("metrics", metrics_node)
builder.add_node("runbooks", runbook_node)
builder.add_node("report", report_node)


# STEP 6: Connect workflow nodes
builder.add_edge(START, "logs")
builder.add_edge("logs", "metrics")
builder.add_edge("metrics", "runbooks")
builder.add_edge("runbooks", "report")
builder.add_edge("report", END)


# STEP 7: Compile the workflow
investigation_graph = builder.compile()


# STEP 8: Execute incident investigation
def investigate(state: IncidentState) -> dict:
    return investigation_graph.invoke(state)
