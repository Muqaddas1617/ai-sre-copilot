from agent.risk_analyzer import analyze_risk
from agent.incident_analyzer import analyze_incident
from agent.approval_engine import approve

def run_agent(text):
    risk, reason = analyze_risk(text)
    incident = analyze_incident(text)
    decision = approve(risk)

    return {
        "risk_score": risk,
        "reason": reason,
        "incident": incident,
        "decision": decision
    }

if __name__ == "__main__":
    while True:
        text = input("Enter deployment info: ")
        result = run_agent(text)
        print(result)