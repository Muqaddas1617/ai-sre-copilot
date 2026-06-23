import json
import os
import re
import time
from typing import Any, Dict, List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from agent.approval_engine import ApprovalAgent
from agent.incident_analyzer import IncidentAnalyzerAgent
from agent.memory_agent import MemoryAgent
from agent.risk_analyzer import RiskAnalyzerAgent
from agent.summary_agent import ExplanationAgent

app = FastAPI(
    title="AI SRE Copilot",
    description="A deployment safety assistant for risk scoring, incident analysis, and approval routing.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
LOG_FILE = os.path.join(BASE_DIR, "logs.json")
LOGS: List[Dict[str, Any]] = []

SENSITIVE_PATTERN = re.compile(
    r"(?i)\b(password|passwd|pwd|token|api[_-]?key|secret|authorization)\s*[:=]\s*([^\s,;]+)"
)


def load_logs() -> List[Dict[str, Any]]:
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as handle:
                return json.load(handle)
        except (json.JSONDecodeError, OSError):
            return []
    return []


def save_logs() -> None:
    with open(LOG_FILE, "w", encoding="utf-8") as handle:
        json.dump(LOGS, handle, indent=2)


LOGS = load_logs()

risk_agent = RiskAnalyzerAgent()
incident_agent = IncidentAnalyzerAgent()
approval_agent = ApprovalAgent()
memory_agent = MemoryAgent([entry.get("input", "") for entry in LOGS])
explanation_agent = ExplanationAgent()


def sanitize_text(text: str) -> str:
    if not isinstance(text, str):
        return ""
    return SENSITIVE_PATTERN.sub(r"\1=[REDACTED]", text)


def create_log(entry: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": len(LOGS) + 1,
        "input": entry["input"],
        "risk_score": entry["risk_score"],
        "risk_reason": entry["risk_reason"],
        "incident": entry["incident"],
        "incident_reason": entry["incident_reason"],
        "incident_score": entry["incident_score"],
        "decision": entry["decision"],
        "history_matches": entry.get("history_matches", []),
        "explanation": entry.get("explanation", ""),
        "trace": {
            "risk_reason": entry["risk_reason"],
            "incident_reason": entry["incident_reason"],
        },
        "timestamp": time.time(),
    }


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok", "service": "ai-sre-copilot"}


@app.get("/")
def root() -> Dict[str, str]:
    return {"message": "AI SRE Copilot API is running"}


@app.post("/analyze")
def analyze(data: Dict[str, Any]) -> Dict[str, Any]:
    text = sanitize_text(str(data.get("text", "")))

    risk, reason = risk_agent.analyze(text)
    incident = incident_agent.analyze(text)
    decision = approval_agent.approve(risk, incident["severity_score"])

    memory_agent.add_entry(text)
    keywords = ["database", "payment", "production", "checkout"]
    history_matches = []
    for keyword in keywords:
        history_matches.extend(memory_agent.lookup(keyword))
    history_matches = list(set(history_matches))
    explanation = explanation_agent.summarize(
        text,
        risk,
        decision,
        incident_status=incident["status"],
        incident_reason=incident["reason"],
        history_matches=history_matches,
    )

    raw = {
        "input": text,
        "risk_score": risk,
        "risk_reason": reason,
        "incident": incident["status"],
        "incident_reason": incident["reason"],
        "incident_score": incident["severity_score"],
        "decision": decision,
        "history_matches": history_matches,
        "explanation": explanation,
    }

    log_entry = create_log(raw)
    LOGS.append(log_entry)
    save_logs()

    return log_entry


@app.get("/logs")
def get_logs(limit: int = 20) -> List[Dict[str, Any]]:
    return LOGS[-limit:] if LOGS else []