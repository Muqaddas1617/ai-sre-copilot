def analyze_risk(text: str):
    text = text.lower()

    risk = 0
    reasons = []

    if "database" in text:
        risk += 40
        reasons.append("Database change detected")

    if "prod" in text or "production" in text:
        risk += 30
        reasons.append("Production environment impact")

    if "payment" in text:
        risk += 35
        reasons.append("Payment system affected")

    # 🔥 COMBO RULE (VERY IMPORTANT)
    if "database" in text and "prod" in text:
        risk += 25
        reasons.append("High blast radius: production database")

    if risk > 100:
        risk = 100

    return risk, " | ".join(reasons)