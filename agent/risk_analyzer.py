class RiskAnalyzerAgent:
    name = "Risk Analyzer Agent"

    def analyze(self, text: str):
        text = text.lower()

        risk = 0
        reasons = []
        context = {
            "database_change": "database" in text or "schema" in text or "migration" in text,
            "production_target": "prod" in text or "production" in text,
            "payment_system": "payment" in text or "checkout" in text or "billing" in text,
            "rollback_complexity": "rollback" in text or "backfill" in text or "data migration" in text,
            "peak_hours": "peak" in text or "weekend" in text or "night" in text,
            "small_change": any(word in text for word in ["small", "minor", "patch", "lightweight"]),
        }

        if context["database_change"]:
            risk += 25
            reasons.append("Database or schema change detected")

        if context["production_target"]:
            risk += 20
            reasons.append("Production environment impact")

        if context["payment_system"]:
            risk += 20
            reasons.append("Payment or checkout workflow affected")

        if context["rollback_complexity"]:
            risk += 12
            reasons.append("Rollback or data migration complexity")

        if context["peak_hours"]:
            risk += 8
            reasons.append("Deployment during high-risk operating window")

        if context["database_change"] and context["production_target"]:
            risk += 10
            reasons.append("High blast radius: production database change")

        if context["database_change"] and context["payment_system"]:
            risk += 8
            reasons.append("Cross-service dependency with billing or payments")

        if context["small_change"]:
            risk -= 20
            reasons.append("Minor or low-scope change")

        if risk > 100:
            risk = 100
        if risk < 0:
            risk = 0

        return risk, " | ".join(reasons) if reasons else "No specific deployment risk indicators found"


def analyze_risk(text: str):
    agent = RiskAnalyzerAgent()
    return agent.analyze(text)