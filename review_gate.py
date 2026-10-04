import json
from datetime import datetime, timezone

def review_gate_v1(report: str, decision: str, region: str, reviewer_note: str = "") -> dict:
    allowed_decisions = {"approve", "edit", "reject"}
    if decision not in allowed_decisions:
        raise ValueError(f"Invalid decision '{decision}'. Must be one of {allowed_decisions}")

    external_use_allowed = (decision == "approve")
    
    # Generating the run_id using timestamp 
    now = datetime.now(timezone.utc)
    run_id = f"run_{now.strftime('%Y%m%d_%H%M%S_%f')}"
    timestamp = now.isoformat()

    audit_entry = {
        "timestamp": timestamp,
        "run_id": run_id,
        "region": region,
        "decision": decision,
        "reviewer_note": reviewer_note
    }

    with open("audit_log.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(audit_entry) + "\n")

    return {
        "run_id": run_id,
        "region": region,
        "decision": decision,
        "external_use_allowed": external_use_allowed,
        "reviewer_note": reviewer_note,
        "report_content": report
    }
