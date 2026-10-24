
import { useState } from "react";
import "./App.css";

type Evidence = {
  source?: string;
  service?: string;
  timestamp?: string;
  level?: string;
  content?: string;
};

type Runbook = {
  document?: string;
  score?: number;
};

type InvestigationResult = {
  title: string;
  description: string;
  service: string;
  status: string;
  log_count: number;
  metric_count: number;
  evidence: Evidence[];
  runbooks: Runbook[];
  final_report: string;
};

function App() {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [service, setService] = useState("checkout");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState<InvestigationResult | null>(null);

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    setError("");
    setResult(null);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/incidents/investigate",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ title, description, service }),
        }
      );

      if (!response.ok) {
        const details = await response.text();
        throw new Error(`Request failed (${response.status}): ${details}`);
      }

      const data: InvestigationResult = await response.json();
      setResult(data);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Something went wrong while investigating the incident."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="app-shell">
      <header className="topbar">
        <div className="brand">
          <div className="brand-icon">C</div>
          <div>
            <h1>CloudOps AI</h1>
            <p>Incident Investigation Assistant</p>
          </div>
        </div>
        <div className="system-status">
          <span className="status-dot" />
          Local environment
        </div>
      </header>

      <section className="hero">
        <p className="eyebrow">AI-ASSISTED OPERATIONS</p>
        <h2>Investigate incidents with clarity.</h2>
        <p className="hero-description">
          Submit an incident to collect service evidence, retrieve troubleshooting
          guidance, and generate an investigation report.
        </p>
      </section>

      <section className="dashboard-grid">
        <div className="panel incident-panel">
          <div className="panel-heading">
            <div>
              <p className="eyebrow">NEW INVESTIGATION</p>
              <h3>Incident details</h3>
            </div>
            <span className="step-label">Step 1</span>
          </div>

          <form onSubmit={handleSubmit}>
            <label htmlFor="title">Incident title</label>
            <input
              id="title"
              value={title}
              onChange={(event) => setTitle(event.target.value)}
              placeholder="e.g. Checkout API latency increased"
              minLength={3}
              maxLength={150}
              required
            />

            <label htmlFor="service">Affected service</label>
            <select
              id="service"
              value={service}
              onChange={(event) => setService(event.target.value)}
              required
            >
              <option value="checkout">Checkout</option>
              <option value="payments">Payments</option>
            </select>

            <label htmlFor="description">Incident description</label>
            <textarea
              id="description"
              value={description}
              onChange={(event) => setDescription(event.target.value)}
              placeholder="Describe what happened, when it started, and any recent changes..."
              minLength={10}
              maxLength={2000}
              rows={5}
              required
            />

            <button type="submit" disabled={loading}>
              {loading ? "Investigating..." : "Run investigation"}
              {!loading && <span aria-hidden="true"> →</span>}
            </button>

            <p className="form-note">
              Investigation uses the local sample logs, metrics, and runbooks.
            </p>
          </form>
        </div>

        <div className="panel overview-panel">
          <p className="eyebrow">INVESTIGATION PIPELINE</p>
          <h3>How it works</h3>

          <div className="pipeline">
            <div className="pipeline-item">
              <span className="pipeline-number">01</span>
              <div>
                <h4>Log analysis</h4>
                <p>Find entries for the affected service.</p>
              </div>
            </div>
            <div className="pipeline-item">
              <span className="pipeline-number">02</span>
              <div>
                <h4>Metric inspection</h4>
                <p>Review latency, error rate, and pool usage.</p>
              </div>
            </div>
            <div className="pipeline-item">
              <span className="pipeline-number">03</span>
              <div>
                <h4>Runbook retrieval</h4>
                <p>Find relevant troubleshooting instructions.</p>
              </div>
            </div>
            <div className="pipeline-item">
              <span className="pipeline-number">04</span>
              <div>
                <h4>Report generation</h4>
                <p>Combine findings into a readable report.</p>
              </div>
            </div>
          </div>

          <div className="safety-note">
            <strong>Safety first</strong>
            <p>
              Findings are investigative guidance, not proof of root cause.
              No automatic remediation is performed.
            </p>
          </div>
        </div>
      </section>

      {loading && (
        <section className="message-panel" aria-live="polite">
          <span className="loading-spinner" />
          <div>
            <h3>Investigating incident</h3>
            <p>Collecting evidence and generating the report...</p>
          </div>
        </section>
      )}

      {error && (
        <section className="error-panel" role="alert">
          <h3>Investigation could not be completed</h3>
          <p>{error}</p>
          <p>
            Check that your FastAPI server is running. A browser CORS
            configuration may also be needed before the frontend can call it.
          </p>
        </section>
      )}

      {result && (
        <section className="results-section">
          <div className="results-heading">
            <div>
              <p className="eyebrow">INVESTIGATION RESULTS</p>
              <h2>{result.title}</h2>
              <p>{result.description}</p>
            </div>
            <span className="result-status">
              {result.status.replaceAll("_", " ")}
            </span>
          </div>

          <div className="stats-grid">
            <div className="stat-card">
              <p>Matching log entries</p>
              <strong>{result.log_count}</strong>
            </div>
            <div className="stat-card">
              <p>Matching metric records</p>
              <strong>{result.metric_count}</strong>
            </div>
            <div className="stat-card">
              <p>Total evidence records</p>
              <strong>{result.evidence.length}</strong>
            </div>
          </div>

          <div className="panel">
            <p className="eyebrow">COLLECTED EVIDENCE</p>
            <h3>Logs and metrics</h3>
            {result.evidence.length === 0 ? (
              <p>No matching evidence was found.</p>
            ) : (
              <div className="evidence-list">
                {result.evidence.map((item, index) => (
                  <article className="evidence-item" key={`${item.source}-${index}`}>
                    <div className="evidence-meta">
                      <span>{item.source ?? "Evidence"}</span>
                      {item.level && <span>{item.level}</span>}
                      {item.timestamp && <time>{item.timestamp}</time>}
                    </div>
                    <p>{item.content}</p>
                  </article>
                ))}
              </div>
            )}
          </div>

          <div className="panel">
            <p className="eyebrow">TROUBLESHOOTING GUIDANCE</p>
            <h3>Retrieved runbooks</h3>
            {result.runbooks.length === 0 ? (
              <p>No matching runbooks were found.</p>
            ) : (
              <ul className="runbook-list">
                {result.runbooks.map((runbook, index) => (
                  <li key={`${runbook.document}-${index}`}>
                    <span>{runbook.document ?? "Unnamed runbook"}</span>
                    {typeof runbook.score === "number" && (
                      <span>Match score: {runbook.score}</span>
                    )}
                  </li>
                ))}
              </ul>
            )}
          </div>

          <div className="panel report-panel">
            <p className="eyebrow">GENERATED REPORT</p>
            <h3>Incident investigation report</h3>
            <pre>{result.final_report}</pre>
          </div>
        </section>
      )}

      <footer>
        AI Agentic CloudOps · Local development build · Human review required
      </footer>
    </main>
  );
}

export default App;
