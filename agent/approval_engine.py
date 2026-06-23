class ApprovalAgent:
    name = "Approval Agent"

    def approve(self, risk: int, incident_score: int = 0):
        combined_score = max(risk, incident_score)

        if combined_score >= 80:
            return "BLOCKED - CRITICAL RISK"
        if combined_score >= 60:
            return "HUMAN APPROVAL REQUIRED"
        if combined_score >= 35:
            return "REVIEW RECOMMENDED"
        return "AUTO APPROVED"


def approve(risk: int, incident_score: int = 0):
    agent = ApprovalAgent()
    return agent.approve(risk, incident_score)