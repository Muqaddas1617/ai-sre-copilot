import { useEffect, useState } from "react";

function App() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(false);

  const API = process.env.REACT_APP_API_URL || "http://127.0.0.1:8000";
  const demoCases = [
    {
      label: "Safe deploy",
      text: "Deploy minor frontend copy change to staging for a marketing banner update.",
    },
    {
      label: "Medium risk",
      text: "Roll out a small database schema change to production with a standard rollback plan.",
    },
    {
      label: "High risk",
      text: "Deploy payment service change to production; rollback is complex and latency increased for checkout requests.",
    },
    {
      label: "Critical incident",
      text: "Production checkout payment failed after a database migration; users cannot complete purchases.",
    },
  ];

  const getRiskColor = (score) => {
    if (score >= 80) return "#ef4444";
    if (score >= 60) return "#f59e0b";
    if (score >= 35) return "#facc15";
    return "#22c55e";
  };

  const getDecisionColor = (decision) => {
    if (decision?.includes("BLOCKED")) return "#ef4444";
    if (decision?.includes("HUMAN")) return "#f59e0b";
    if (decision?.includes("REVIEW")) return "#facc15";
    return "#22c55e";
  };

  const getIncidentBadgeColor = (incident) => {
    if (incident?.includes("CRITICAL")) return "#dc2626";
    if (incident?.includes("HIGH")) return "#f97316";
    if (incident?.includes("MEDIUM")) return "#eab308";
    return "#22c55e";
  };

  const analyzeWithText = async (inputText) => {
    if (!inputText || loading) return;

    setText(inputText);
    setLoading(true);

    try {
      const res = await fetch(`${API}/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: inputText }),
      });

      const data = await res.json();
      setResult(data);
      loadLogs();
    } catch (err) {
      console.error("API Error:", err);
    } finally {
      setLoading(false);
    }
  };

  const analyze = async () => {
    analyzeWithText(text);
  };

  const loadLogs = async () => {
    try {
      const res = await fetch(`${API}/logs`);
      const data = await res.json();
      setLogs(Array.isArray(data) ? [...data].reverse() : []);
    } catch (err) {
      console.error("Logs Error:", err);
    }
  };

  useEffect(() => {
    loadLogs();
  }, []);

  return (
    <div
      style={{
        padding: 20,
        fontFamily: "Arial",
        background: "#0f172a",
        color: "white",
        minHeight: "100vh",
      }}
    >
      <h1>AI SRE Copilot Dashboard</h1>
      <p style={{ color: "#cbd5e1" }}>
        Submit a deployment change and receive an operational risk review with approval guidance.
      </p>

      <div style={{ marginBottom: 20 }}>
        <div style={{ marginBottom: 10, color: "#cbd5e1", fontSize: 14 }}>
          Try a sample scenario:
        </div>
        <div style={{ marginBottom: 12 }}>
          {demoCases.map((demo) => (
            <button
              key={demo.label}
              onClick={() => setText(demo.text)}
              style={{
                marginRight: 8,
                marginBottom: 8,
                padding: "6px 10px",
                borderRadius: 999,
                border: "1px solid #475569",
                background: "#1e293b",
                color: "white",
                cursor: "pointer",
              }}
            >
              {demo.label}
            </button>
          ))}
        </div>

        <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
          <input
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Enter deployment change..."
            style={{ flex: "1 1 320px", minWidth: 280, padding: 10, borderRadius: 8, border: "1px solid #475569" }}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                analyze();
              }
            }}
          />

          <button
            onClick={analyze}
            disabled={loading}
            style={{
              padding: "10px 16px",
              background: loading ? "#64748b" : "#22c55e",
              border: "none",
              borderRadius: 8,
              cursor: "pointer",
              color: "white",
              fontWeight: "bold",
            }}
          >
            {loading ? "Analyzing..." : "Analyze"}
          </button>
        </div>
      </div>

      {result && (
        <div
          style={{
            background: "#1e293b",
            padding: 15,
            borderRadius: 10,
            marginBottom: 20,
          }}
        >
          <h3>📊 Latest Analysis</h3>

          <div style={{ display: "flex", gap: 12, flexWrap: "wrap", marginBottom: 12 }}>
            <div style={{ background: getRiskColor(result.risk_score), padding: "8px 12px", borderRadius: 999 }}>
              <b>Risk Meter:</b> {result.risk_score}/100
            </div>
            <div style={{ background: getIncidentBadgeColor(result.incident), padding: "8px 12px", borderRadius: 999 }}>
              <b>Incident:</b> {result.incident}
            </div>
            <div style={{ background: getDecisionColor(result.decision), padding: "8px 12px", borderRadius: 999 }}>
              <b>Decision:</b> {result.decision}
            </div>
          </div>

          <div style={{ marginBottom: 10 }}>
            <b>Explanation:</b> {result.explanation}
          </div>
          <div style={{ marginBottom: 10 }}>
            <b>History Matches:</b> {result.history_matches?.length ? result.history_matches.join(", ") : "No similar prior entries"}
          </div>
          <pre style={{ whiteSpace: "pre-wrap" }}>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}

      <h2>📜 Deployment History</h2>

      {logs.map((l) => (
        <div
          key={l.id}
          style={{
            background: "#111827",
            padding: 10,
            marginBottom: 10,
            borderRadius: 8,
            border: "1px solid #334155",
          }}
        >
          <b>Input:</b> {l.input} <br />
          <b>Risk:</b> {l.risk_score} <br />
          <b>Incident:</b> {l.incident} <br />
          <b>Decision:</b> {l.decision}
        </div>
      ))}
    </div>
  );
}

export default App;