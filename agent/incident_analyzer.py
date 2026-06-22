def analyze_incident(text: str):
    text = text.lower()

    score = 0
    issues = []

    if "failed" in text:
        score += 40
        issues.append("Failure detected")

    if "payment failed" in text:
        score += 50
        issues.append("Critical payment failure")

    if "production" in text:
        score += 20
        issues.append("Production impact")

    if "database" in text and "prod" in text:
        score += 30
        issues.append("Critical DB production risk")

    if score >= 80:
        status = "CRITICAL INCIDENT"
    elif score >= 50:
        status = "HIGH INCIDENT"
    else:
        status = "NO INCIDENT DETECTED"

    return {
        "status": status,
        "severity_score": min(score, 100),
        "reason": " | ".join(issues) if issues else "System healthy"
    }