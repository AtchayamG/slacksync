import { useEffect, useMemo, useState } from "react";
import { Activity, BarChart3, Bot, Braces, CheckCircle2, Clock3, GitPullRequest, PieChart, Radio, Shield, Sparkles } from "lucide-react";
import type { AgentResult, SyncCommand } from "@slacksync/contracts";
import { apiAvailable, runCommand } from "./api";
import { commandSummary, resultHeadline, statusTone } from "./viewModel";
import { commands, results, timeline } from "./demoData";

const agents = [
  ["Reviewer", "reviewer", "Security-aware PR analysis", "online", "violet"],
  ["Tester", "tester", "Syntax-valid test generation", "online", "blue"],
  ["Scribe", "scribe", "Docs and changelog drafts", "standby", "amber"],
  ["Watchdog", "watchdog", "CI failure triage", "watching", "rose"]
];

const readiness = [
  { label: "Maestro", value: 97, color: "var(--green)" },
  { label: "Reviewer", value: 92, color: "var(--violet)" },
  { label: "Tester", value: 89, color: "var(--blue)" },
  { label: "Scribe", value: 91, color: "var(--yellow)" },
  { label: "Watchdog", value: 94, color: "var(--red)" }
];

const commandMix = [
  { label: "Review", value: 38, color: "#7c5cff" },
  { label: "Tests", value: 27, color: "#36c5f0" },
  { label: "Docs", value: 18, color: "#ecb22e" },
  { label: "Status", value: 17, color: "#e01e5a" }
];

export function App() {
  const [selected, setSelected] = useState<SyncCommand>("review");
  const [liveResult, setLiveResult] = useState<AgentResult | null>(null);
  const [mode, setMode] = useState<"api" | "demo" | "loading">("demo");
  const command = commands.find((item) => item.id === selected)!;
  const active = liveResult?.kind === selected || (selected === "status" && liveResult?.kind === "status") ? liveResult : results[selected];
  const parsed = useMemo(() => commandSummary(command.prompt), [command.prompt]);

  useEffect(() => {
    let cancelled = false;
    if (!apiAvailable()) {
      setLiveResult(null);
      setMode("demo");
      return;
    }
    setMode("loading");
    runCommand(command.prompt)
      .then((response) => {
        if (!cancelled) {
          setLiveResult(response.result);
          setMode("api");
        }
      })
      .catch(() => {
        if (!cancelled) {
          setLiveResult(null);
          setMode("demo");
        }
      });
    return () => {
      cancelled = true;
    };
  }, [command.prompt]);

  return (
    <main className="shell">
      <section className="hero">
        <div className="heroCopy">
          <p className="eyebrow">Demo mode - no secrets loaded</p>
          <h1>SlackSync</h1>
          <p className="lede">A Slack-native agent operations center that routes engineering requests, attaches context, and returns judge-visible proof.</p>
          <div className="heroBadges" aria-label="Core proof points">
            <span>Slash command live</span>
            <span>Typed contracts</span>
            <span>Demo-safe adapters</span>
          </div>
        </div>
        <div className="heroStatus">
          <div className="pulse">
            <Radio size={18} />
            <span>{mode === "api" ? "Live FastAPI route" : mode === "loading" ? "Routing command" : "Deterministic demo fallback"}</span>
          </div>
          <div className="signalCard">
            <Sparkles size={18} />
            <strong>Judge path is ready</strong>
            <p>/sync command, Slack proof, API tests, and architecture evidence are all tied together.</p>
          </div>
        </div>
      </section>

      <section className="metrics" aria-label="Operational dashboard">
        <Metric icon={<GitPullRequest />} label="PRs reviewed" value="18" />
        <Metric icon={<CheckCircle2 />} label="Tests drafted" value="64" />
        <Metric icon={<Clock3 />} label="Median ack" value="180 ms" />
        <Metric icon={<Shield />} label="Demo safety" value="0 secrets" />
      </section>

      <section className="grid">
        <div className="panel command">
          <div className="panelHead">
            <div>
              <p className="eyebrow">Command simulator</p>
              <h2>/sync router</h2>
            </div>
            <Bot />
          </div>
          <div className="tabs">
            {commands.map((item) => (
              <button className={item.id === selected ? "active" : ""} key={item.id} onClick={() => setSelected(item.id)}>
                {item.label}
              </button>
            ))}
          </div>
          <code className="terminal">{command.prompt}</code>
          <p className="route">{parsed}</p>
          <div className={`result ${statusTone(active.status)}`}>
            <strong>{resultHeadline(active)}</strong>
            <span>{active.summary}</span>
          </div>
        </div>

        <div className="panel thread">
          <div className="panelHead">
            <div>
              <p className="eyebrow">Slack thread preview</p>
              <h2>#dev-agent-ops</h2>
            </div>
            <Activity />
          </div>
          <Message author="Asha" text={command.prompt} />
          <Message author="SlackSync" text={active.summary} accent />
          {active.kind === "review" &&
            active.comments.map((comment) => (
              <Message
                key={`${comment.filePath}-${comment.lineNumber}`}
                author={comment.severity}
                text={`${comment.filePath}:${comment.lineNumber} - ${comment.message}`}
              />
            ))}
          {active.kind === "status" && <Message author="root cause" text={active.rootCause ?? active.summary} />}
        </div>
      </section>

      <section className="analytics" aria-label="Workspace analytics">
        <div className="panel chartPanel">
          <div className="panelHead">
            <div>
              <p className="eyebrow">Agent readiness</p>
              <h2>Fleet health score</h2>
            </div>
            <BarChart3 />
          </div>
          <BarChart data={readiness} />
        </div>
        <div className="panel chartPanel">
          <div className="panelHead">
            <div>
              <p className="eyebrow">Command mix</p>
              <h2>/sync usage (7 days)</h2>
            </div>
            <PieChart />
          </div>
          <Donut data={commandMix} centerTop="312" centerSub="runs" />
        </div>
      </section>

      <section className="lower">
        <div className="panel">
          <p className="eyebrow">Agent fleet</p>
          <div className="agents">
            {agents.map(([name, key, detail, state, tone]) => (
              <article className={`agent ${tone}`} key={key}>
                <span className="orb" aria-hidden="true" />
                <div>
                  <h3>{name}</h3>
                  <p>{detail}</p>
                </div>
                <b>{state}</b>
              </article>
            ))}
          </div>
        </div>
        <div className="panel">
          <p className="eyebrow">Workflow timeline</p>
          <ol className="timeline">
            {timeline.map((step) => (
              <li key={step}>{step}</li>
            ))}
          </ol>
        </div>
        <div className="panel proof">
          <p className="eyebrow">Architecture proof</p>
          <h2>Slack surfaces to FastAPI to Maestro to agents to Block Kit</h2>
          <p>
            This console mirrors the planned Slack App Home and threaded responses while keeping real Slack,
            GitHub, Jira, and LLM credentials outside demo mode.
          </p>
          <div className="chips">
            <span>Typed contracts</span>
            <span>Deterministic routing</span>
            <span>MCP-ready boundary</span>
            <span>RTS context slot</span>
          </div>
          {active.context && (
            <div className="evidence">
              <Braces size={18} />
              <div>
                <b>{active.context.mcp[0]?.source} MCP</b>
                <p>{active.context.mcp[0]?.title}</p>
              </div>
              <div>
                <b>{active.context.rts[0]?.channel} RTS</b>
                <p>{active.context.rts[0]?.snippet}</p>
              </div>
            </div>
          )}
        </div>
      </section>
    </main>
  );
}

function Metric({ icon, label, value }: { icon: React.ReactNode; label: string; value: string }) {
  return (
    <article className="metric">
      {icon}
      <span>{label}</span>
      <strong>{value}</strong>
    </article>
  );
}

function Message({ author, text, accent = false }: { author: string; text: string; accent?: boolean }) {
  return (
    <article className={accent ? "message accent" : "message"}>
      <b>{author}</b>
      <p>{text}</p>
    </article>
  );
}

function BarChart({ data }: { data: Array<{ label: string; value: number; color: string }> }) {
  const max = Math.max(...data.map((d) => d.value), 100);
  return (
    <div className="barChart" role="img" aria-label="Agent readiness scores">
      {data.map((d) => (
        <div className="barRow" key={d.label}>
          <span className="barLabel">{d.label}</span>
          <div className="barTrack">
            <div className="barFill" style={{ width: `${(d.value / max) * 100}%`, background: d.color }} />
          </div>
          <span className="barValue">{d.value}</span>
        </div>
      ))}
    </div>
  );
}

function Donut({ data, centerTop, centerSub }: { data: Array<{ label: string; value: number; color: string }>; centerTop: string; centerSub: string }) {
  const total = data.reduce((sum, d) => sum + d.value, 0);
  const r = 60;
  const c = 2 * Math.PI * r;
  let offset = 0;
  const segments = data.map((d) => {
    const frac = d.value / total;
    const seg = { ...d, dash: frac * c, gap: c - frac * c, off: -offset * c, pct: Math.round(frac * 100) };
    offset += frac;
    return seg;
  });
  return (
    <div className="donutWrap">
      <svg className="donutSvg" viewBox="0 0 160 160" role="img" aria-label="Command mix">
        <circle cx="80" cy="80" r={r} fill="none" stroke="rgba(255,255,255,0.06)" strokeWidth="18" />
        {segments.map((s) => (
          <circle
            key={s.label}
            cx="80"
            cy="80"
            r={r}
            fill="none"
            stroke={s.color}
            strokeWidth="18"
            strokeDasharray={`${s.dash} ${s.gap}`}
            strokeDashoffset={s.off}
            transform="rotate(-90 80 80)"
            strokeLinecap="butt"
          />
        ))}
        <text x="80" y="74" textAnchor="middle" className="donutTop">{centerTop}</text>
        <text x="80" y="94" textAnchor="middle" className="donutSub">{centerSub}</text>
      </svg>
      <ul className="donutLegend">
        {segments.map((s) => (
          <li key={s.label}>
            <span className="legendDot" style={{ background: s.color }} />
            <span className="legendLabel">{s.label}</span>
            <span className="legendPct">{s.pct}%</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
