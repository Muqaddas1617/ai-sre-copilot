import { useState, useEffect } from "react";

function App() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(false);

  const API = "http://127.0.0.1:8000";

  // -------------------------
  // ANALYZE FUNCTION (SAFE)
  // -------------------------
  const analyze = async () => {
    if (!text || loading) return; // prevent spam + empty input

    setLoading(true);

    try {
      const res = await fetch(`${API}/analyze`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text })
      });

      const data = await res.json();
      setResult(data);
      loadLogs();

    } catch (err) {
      console.error("API Error:", err);
    }

    setLoading(false);
  };

  // -------------------------
  // LOAD LOGS
  // -------------------------
  const loadLogs = async () => {
    try {
      const res = await fetch(`${API}/logs`);
      const data = await res.json();

      setLogs(Array.isArray(data) ? [...data].reverse() : []);
    } catch (err) {
      console.error("Logs Error:", err);
    }
  };

  // -------------------------
  // INIT LOAD
  // -------------------------
  useEffect(() => {
    loadLogs();
  }, []);

  // -------------------------
  // UI
  // -------------------------
  return (
    <div style={{
      padding: 20,
      fontFamily: "Arial",
      background: "#0f172a",
      color: "white",
      minHeight: "100vh"
    }}>
      
      <h1> AI SRE Copilot Dashboard</h1>

      {/* INPUT AREA */}
      <div style={{ marginBottom: 20 }}>
        <input
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Enter deployment change..."
          style={{
            width: "60%",
            padding: 10,
            borderRadius: 6
          }}
        />

        <button
          onClick={analyze}
          disabled={loading}
          style={{
            marginLeft: 10,
            padding: 10,
            background: loading ? "#64748b" : "#22c55e",
            border: "none",
            borderRadius: 6,
            cursor: "pointer"
          }}
        >
          {loading ? "Analyzing..." : "Analyze"}
        </button>
      </div>

      {/* RESULT */}
      {result && (
        <div style={{
          background: "#1e293b",
          padding: 15,
          borderRadius: 10,
          marginBottom: 20
        }}>
          <h3>📊 Latest Analysis</h3>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}

      {/* LOGS */}
      <h2>📜 Deployment History</h2>

      {logs.map((l) => (
        <div key={l.id} style={{
          background: "#111827",
          padding: 10,
          marginBottom: 10,
          borderRadius: 8,
          border: "1px solid #334155"
        }}>
          <b>Input:</b> {l.input} <br />
          <b>Risk:</b> {l.risk_score} <br />
          <b>Decision:</b> {l.decision}
        </div>
      ))}

    </div>
  );
}

export default App;