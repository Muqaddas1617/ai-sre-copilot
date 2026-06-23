class ExplanationAgent:
    name = "Explanation Agent"

    def summarize(self, context: str, risk_score: int, decision: str, incident_status: str = "", incident_reason: str = "", history_matches=None):
        context_text = context.strip() if context else "deployment change"
        lowered = context_text.lower()

        factors = []
        if "database" in lowered or "schema" in lowered or "migration" in lowered:
            factors.append("Database or schema change")
        if "prod" in lowered or "production" in lowered:
            factors.append("Production deployment")
        if "payment" in lowered or "checkout" in lowered:
            factors.append("Customer-facing payment flow")
        if "rollback" in lowered or "backfill" in lowered:
            factors.append("Rollback complexity")
        if "small" in lowered or "minor" in lowered:
            factors.append("Low-scope change")

        risk_factors = ", ".join(factors[:4]) if factors else "General deployment change"

        incident_lines = []
        if incident_status:
            incident_lines.append(f"Incident Status: {incident_status}")
        if incident_reason:
            incident_lines.append(f"Incident Signals: {incident_reason}")

        history_line = ""
        if history_matches:
            history_line = f"History Notes: Similar prior entries found in {', '.join(history_matches[:2])}."

        return (
            f"Risk Factors: {risk_factors}\n"
            f"Incident Signals: {incident_reason if incident_reason else 'No major incident signals detected'}\n"
            f"Decision: {decision} based on a risk score of {risk_score}.\n"
            f"{history_line}".strip()
        )
