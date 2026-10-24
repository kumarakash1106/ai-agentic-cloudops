
def generate_report(state: dict) -> dict:
    """
    Generate a readable incident report from collected evidence.
    This is a deterministic mock report, not an LLM-generated response.
    """

    title = state.get("title", "Untitled incident")
    description = state.get("description", "No description provided")
    service = state.get("service", "unknown")
    evidence = state.get("evidence", [])
    runbooks = state.get("runbooks", [])

    # Separate log evidence from metric evidence.
    log_items = [
        item for item in evidence
        if item.get("source") == "synthetic_logs"
    ]

    metric_items = [
        item for item in evidence
        if item.get("source") == "synthetic_metrics"
    ]

    # Build the evidence section.
    evidence_lines = []

    for item in evidence:
        timestamp = item.get("timestamp")

        if timestamp:
            evidence_lines.append(
                f"- [{item.get('level', 'INFO')}] "
                f"{timestamp}: {item.get('content', '')}"
            )
        else:
            evidence_lines.append(
                f"- {item.get('content', 'No details available')}"
            )

    if not evidence_lines:
        evidence_lines.append("- No matching evidence was found.")

    # Identify retrieved runbooks.
    runbook_names = [
        item.get("document", "Unnamed runbook")
        for item in runbooks
    ]

    if runbook_names:
        runbook_section = "\n".join(
            f"- {name}" for name in runbook_names
        )
    else:
        runbook_section = "- No matching runbooks were found."

    # Build a cautious assessment.
    assessment = (
        f"The investigation found {len(log_items)} matching log entries "
        f"and {len(metric_items)} matching metric records for {service}. "
        "These observations may help explain the incident, but they do not "
        "prove its root cause. Compare the incident timeline with recent "
        "deployments and inspect database operations before drawing a conclusion."
    )

    recommendations = [
        "Compare deployment timing with the start of the incident.",
        "Inspect slow database operations and database timeouts.",
        "Compare the current release with the previous version.",
        "Review the collected logs and metrics before confirming a root cause.",
        "Do not execute a rollback without human review and approval."
    ]

    report = f"""# Incident Investigation Report

## Incident
- **Title:** {title}
- **Service:** {service}
- **Description:** {description}
- **Status:** Investigation completed

## Collected Evidence
{chr(10).join(evidence_lines)}

## Initial Assessment
{assessment}

## Relevant Runbooks
{runbook_section}

## Recommended Next Steps
{chr(10).join(f"- {item}" for item in recommendations)}

## Safety Note
This report provides investigative guidance, not a confirmed root cause.
No remediation or rollback has been executed.
"""

    return {"final_report": report}
