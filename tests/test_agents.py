import unittest

from agent.approval_engine import ApprovalAgent, approve
from agent.incident_analyzer import IncidentAnalyzerAgent, analyze_incident
from agent.memory_agent import MemoryAgent
from agent.risk_analyzer import RiskAnalyzerAgent, analyze_risk
from agent.summary_agent import ExplanationAgent


class AgentArchitectureTests(unittest.TestCase):
    def test_risk_agent_class(self):
        agent = RiskAnalyzerAgent()
        risk, reason = agent.analyze("Deploy database migration to production payment service")
        self.assertGreater(risk, 0)
        self.assertIn("database", reason.lower())

    def test_incident_agent_class(self):
        agent = IncidentAnalyzerAgent()
        result = agent.analyze("Payment failed in production after checkout latency spike")
        self.assertIn(result["status"], ["HIGH INCIDENT", "CRITICAL INCIDENT"])
        self.assertGreaterEqual(result["severity_score"], 50)

    def test_approval_agent_class(self):
        agent = ApprovalAgent()
        self.assertEqual(agent.approve(85, 70), "BLOCKED - CRITICAL RISK")

    def test_function_compatibility(self):
        self.assertEqual(approve(90, 85), "BLOCKED - CRITICAL RISK")
        self.assertEqual(analyze_incident("system healthy")["status"], "NO INCIDENT DETECTED")
        self.assertGreater(analyze_risk("database prod")[0], 0)

    def test_memory_and_explanation_agents(self):
        memory_agent = MemoryAgent()
        explanation_agent = ExplanationAgent()
        memory_agent.add_entry("database prod payment failure")
        history = memory_agent.lookup("database")
        summary = explanation_agent.summarize("database migration", 85, "BLOCKED - CRITICAL RISK")
        self.assertGreaterEqual(len(history), 1)
        self.assertIn("risk", summary.lower())

    def test_small_change_risk_is_not_overinflated(self):
        risk, _ = RiskAnalyzerAgent().analyze("small database schema change with rollback")
        self.assertLess(risk, 40)

    def test_explanation_is_structured(self):
        explanation_agent = ExplanationAgent()
        summary = explanation_agent.summarize(
            "small database change in production",
            35,
            "REVIEW RECOMMENDED",
            incident_status="MEDIUM INCIDENT",
            incident_reason="Production impact detected",
            history_matches=["database prod payment failure"],
        )
        self.assertIn("Risk Factors:", summary)
        self.assertIn("Incident Signals:", summary)
        self.assertIn("Decision:", summary)


if __name__ == "__main__":
    unittest.main()
