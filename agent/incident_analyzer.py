class IncidentAnalyzerAgent:
    name = "Incident Analyzer Agent"

    def analyze(self, text: str):
        text = text.lower()

        score = 0
        issues = []

        if "failed" in text or "error" in text:
            score += 20
            issues.append("Observed failure or error signal")

        if "payment failed" in text or "checkout failed" in text:
            score += 25
            issues.append("Critical payment or checkout disruption")

        if "production" in text or "prod" in text:
            score += 15
            issues.append("Production impact detected")

        if "database" in text and ("prod" in text or "production" in text):
            score += 20
            issues.append("Critical database-to-production risk")

        if "latency" in text or "slow" in text:
            score += 10
            issues.append("Performance degradation signal")

        if "rollback" in text or "backfill" in text:
            score += 10
            issues.append("Rollback or data recovery complexity")

        if ("payment" in text or "checkout" in text) and ("production" in text or "prod" in text):
            score += 15
            issues.append("Customer-facing service impacted in production")

        if score >= 80:
            status = "CRITICAL INCIDENT"
        elif score >= 50:
            status = "HIGH INCIDENT"
        elif score >= 25:
            status = "MEDIUM INCIDENT"
        else:
            status = "NO INCIDENT DETECTED"

        return {
            "status": status,
            "severity_score": min(score, 100),
            "reason": " | ".join(issues) if issues else "System healthy"
        }


def analyze_incident(text: str):
    agent = IncidentAnalyzerAgent()
    return agent.analyze(text)