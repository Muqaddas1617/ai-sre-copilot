from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from agent.risk_analyzer import analyze_risk
from agent.incident_analyzer import analyze_incident
from agent.approval_engine import approve
import time
import json
import os

app = FastAPI(title="AI SRE Copilot")

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- MEMORY ----------------
LOG_FILE = "logs.json"
LOGS = []

def load_logs():
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r") as f:
                return json.load(f)
        except:
            return []
    return []

def save_logs():
    with open(LOG_FILE, "w") as f:
        json.dump(LOGS, f, indent=2)

LOGS = load_logs()

# ---------------- LOG FORMAT ----------------
def create_log(entry):
    return {
        "id": len(LOGS) + 1,
        "input": entry["input"],
        "risk_score": entry["risk_score"],
        "risk_reason": entry["risk_reason"],
        "incident": entry["incident"],
        "incident_reason": entry["incident_reason"],
        "incident_score": entry["incident_score"],
        "decision": entry["decision"],
        "trace": {
            "risk_reason": entry["risk_reason"],
            "incident_reason": entry["incident_reason"]
        },
        "timestamp": time.time()
    }

# ---------------- ANALYZE ----------------
@app.post("/analyze")
def analyze(data: dict):
    text = data.get("text", "")

    risk, reason = analyze_risk(text)
    incident = analyze_incident(text)
    decision = approve(risk)

    raw = {
        "input": text,
        "risk_score": risk,
        "risk_reason": reason,
        "incident": incident["status"],
        "incident_reason": incident["reason"],
        "incident_score": incident["severity_score"],
        "decision": decision
    }

    log_entry = create_log(raw)
    LOGS.append(log_entry)
    save_logs()

    return log_entry

# ---------------- LOGS ----------------
@app.get("/logs")
def get_logs(limit: int = 20):
    return LOGS[-limit:]