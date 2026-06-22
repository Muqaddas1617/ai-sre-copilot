def approve(risk: int):
    if risk >= 80:
        return "BLOCKED - CRITICAL RISK"
    elif risk >= 50:
        return "HUMAN APPROVAL REQUIRED"
    elif risk >= 30:
        return "REVIEW RECOMMENDED"
    return "AUTO APPROVED"