import { useEffect, useState } from "react";
import { Check, CircleCheck, CircleX, Eye, Lightbulb, Play } from "lucide-react";
import { api } from "../api.js";
import { runPython } from "../pyRunner.js";
import { KINDS } from "../util.js";
import CodeBlock from "./CodeBlock.jsx";
import CodeEditor from "./CodeEditor.jsx";
import Markdown from "./Markdown.jsx";
import ResultTable from "./ResultTable.jsx";

// `onSubmit(body)` envía el intento al servidor y devuelve su respuesta.
export default function ExercisePanel({ exercise, solved, onSubmit }) {
  const { Icon, label } = KINDS[exercise.kind];
  return (
    <section className="exercise">
      <header className="exercise-head">
        <h2>{exercise.title}</h2>
        <span className="tag">
          <Icon size={14} aria-hidden="true" /> {label}
        </span>
        {solved && (
          <span className="tag ok">
            <Check size={14} aria-hidden="true" /> Resuelto
          </span>
        )}
      </header>
      <div className="exercise-prompt">
        <Markdown>{exercise.prompt}</Markdown>
      </div>
      {exercise.kind === "python" && <PythonExercise exercise={exercise} onSubmit={onSubmit} />}
      {exercise.kind === "sql" && <SqlExercise exercise={exercise} onSubmit={onSubmit} />}
      {exercise.kind === "quiz" && <QuizExercise exercise={exercise} onSubmit={onSubmit} />}
      {exercise.kind === "checklist" && <ChecklistExercise exercise={exercise} onSubmit={onSubmit} solved={solved} />}
    </section>
  );
}

export function Verdict({ ok, children, detail }) {
  const Icon = ok ? CircleCheck : CircleX;
  return (
    <p className={"verdict " + (ok ? "ok" : "bad")}>
      <Icon size={18} aria-hidden="true" /> {children}
      {detail && <span className="detail">{detail}</span>}
    </p>
  );
}

function Helpers({ exercise, solution }) {
  const [hint, setHint] = useState(false);
  const [showSolution, setShowSolution] = useState(false);

  function revealSolution() {
    if (window.confirm("¿Seguro? Intentarlo tú primero es lo que más te hace aprender.")) setShowSolution(true);
  }

  return (
    <div className="helpers">
      <div className="actions">
        {exercise.hint && (
          <button className="btn ghost small" onClick={() => setHint((value) => !value)}>
            <Lightbulb size={14} aria-hidden="true" /> {hint ? "Ocultar pista" : "Pista"}
          </button>
        )}
        {!showSolution && (
          <button className="btn ghost small" onClick={revealSolution}>
            <Eye size={14} aria-hidden="true" /> Ver solución
          </button>
        )}
      </div>
      {hint && (
        <p className="hint">
          <Lightbulb size={16} aria-hidden="true" /> <span>{exercise.hint}</span>
        </p>
      )}
      {showSolution && (
        <div>
          <p className="muted small">Solución de referencia (hay más de una forma correcta):</p>
          <CodeBlock code={solution.replace(/\n$/, "")} lang={exercise.kind === "sql" ? "sql" : "python"} />
        </div>
      )}
    </div>
  );
}

function PythonExercise({ exercise, onSubmit }) {
  const [code, setCode] = useState(exercise.starter);
  const [busy, setBusy] = useState(false);
  const [status, setStatus] = useState("");
  const [outcome, setOutcome] = useState(null);

  async function execute(check) {
    setBusy(true);
    setOutcome(null);
    try {
      const result = await runPython({
        code,
        tests: check ? exercise.tests : "",
        packages: exercise.packages,
        onStatus: setStatus,
      });
      const passed = Boolean(check && result.passed && !result.error);
      setOutcome({ check, ...result, passed });
      if (check) await onSubmit({ passed });
    } catch (error) {
      setOutcome({ check, passed: false, error: error.message, output: "" });
    } finally {
      setBusy(false);
      setStatus("");
    }
  }

  return (
    <div className="stack">
      <CodeEditor value={code} onChange={setCode} language="python" onRun={() => !busy && execute(false)} />
      <div className="actions">
        <button className="btn" disabled={busy} onClick={() => execute(false)}>
          <Play size={15} aria-hidden="true" /> Ejecutar
        </button>
        <button className="btn primary" disabled={busy} onClick={() => execute(true)}>
          <Check size={16} aria-hidden="true" /> Comprobar
        </button>
        {busy && <span className="muted small">{status || "Ejecutando… (la primera vez descarga Python, puede tardar)"}</span>}
        <span className="muted small push">
          <kbd>Ctrl</kbd> + <kbd>Enter</kbd> para ejecutar
        </span>
      </div>
      {outcome && <Console outcome={outcome} />}
      <Helpers exercise={exercise} solution={exercise.solution} />
    </div>
  );
}

function Console({ outcome }) {
  return (
    <div className="console" aria-live="polite">
      {outcome.output ? <pre>{outcome.output}</pre> : null}
      {outcome.error && <pre className="err">{outcome.error}</pre>}
      {outcome.check && !outcome.error && outcome.passed && <Verdict ok>Correcto: pasó todas las pruebas.</Verdict>}
      {outcome.check && !outcome.error && !outcome.passed && <Verdict>Aún no: {outcome.feedback || "alguna prueba falló."}</Verdict>}
      {!outcome.check && !outcome.error && !outcome.output && <p className="muted small">Sin salida. Usa print() para ver valores.</p>}
    </div>
  );
}

function SqlExercise({ exercise, onSubmit }) {
  const [query, setQuery] = useState(exercise.starter);
  const [busy, setBusy] = useState(false);
  const [view, setView] = useState(null);

  async function run() {
    setBusy(true);
    try {
      const result = await api.runSql(query);
      setView({ ...result, verdict: null });
    } catch (error) {
      setView({ error: error.message });
    } finally {
      setBusy(false);
    }
  }

  async function submit() {
    setBusy(true);
    try {
      const result = await onSubmit({ query });
      setView({
        columns: result.columns,
        rows: result.rows,
        truncated: result.truncated,
        error: result.error,
        verdict: { correct: result.correct, text: result.feedback },
      });
    } catch (error) {
      setView({ error: error.message });
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="stack">
      <CodeEditor value={query} onChange={setQuery} language="sql" height="220px" onRun={() => !busy && run()} />
      <div className="actions">
        <button className="btn" disabled={busy} onClick={run}>
          <Play size={15} aria-hidden="true" /> Ejecutar
        </button>
        <button className="btn primary" disabled={busy} onClick={submit}>
          <Check size={16} aria-hidden="true" /> Enviar respuesta
        </button>
        <span className="muted small push">
          <kbd>Ctrl</kbd> + <kbd>Enter</kbd> para ejecutar
        </span>
      </div>
      {view && (
        <div className="console" aria-live="polite">
          {view.error && <pre className="err">{view.error}</pre>}
          {view.verdict && view.verdict.correct && <Verdict ok>Correcto.</Verdict>}
          {view.verdict && !view.verdict.correct && <Verdict>{view.verdict.text}</Verdict>}
          {view.columns && <ResultTable columns={view.columns} rows={view.rows} truncated={view.truncated} />}
        </div>
      )}
      <Helpers exercise={exercise} solution={exercise.solution} />
    </div>
  );
}

function QuizExercise({ exercise, onSubmit }) {
  const [choice, setChoice] = useState(null);
  const [result, setResult] = useState(null);
  const [busy, setBusy] = useState(false);
  const [explain, setExplain] = useState(false);

  async function answer() {
    setBusy(true);
    setExplain(false);
    try {
      setResult(await onSubmit({ answer: choice }));
    } finally {
      setBusy(false);
    }
  }

  const locked = Boolean(result && result.correct);
  return (
    <div className="stack">
      <ul className="options">
        {exercise.options.map((text, index) => {
          let state = "";
          if (result && choice === index) state = result.correct ? " right" : " wrong";
          return (
            <li key={index}>
              <label className={"option" + (choice === index ? " selected" : "") + state}>
                <input
                  type="radio"
                  name={exercise.id}
                  checked={choice === index}
                  disabled={busy || locked}
                  onChange={() => {
                    setChoice(index);
                    setResult(null);
                  }}
                />
                <span>{text}</span>
              </label>
            </li>
          );
        })}
      </ul>
      <div className="actions">
        <button className="btn primary" disabled={busy || locked || choice === null} onClick={answer}>
          Responder
        </button>
      </div>
      {result && result.correct && (
        <div className="console" aria-live="polite">
          <Verdict ok>Correcto.</Verdict>
          <p>{result.explanation}</p>
        </div>
      )}
      {result && !result.correct && (
        <div className="console" aria-live="polite">
          <Verdict>No es esa. Repasa la teoría e inténtalo de nuevo.</Verdict>
          {!explain && (
            <div>
              <button className="btn ghost small" onClick={() => setExplain(true)}>
                Ver explicación
              </button>
            </div>
          )}
          {explain && <p>{result.explanation}</p>}
        </div>
      )}
    </div>
  );
}

function ChecklistExercise({ exercise, onSubmit, solved }) {
  const storageKey = "datapath:checklist:" + exercise.id;
  const size = exercise.items.length;
  const [checked, setChecked] = useState(() => {
    try {
      const saved = JSON.parse(localStorage.getItem(storageKey));
      if (Array.isArray(saved) && saved.length === size) return saved;
    } catch (_) {
      /* sin almacenamiento */
    }
    return Array(size).fill(false);
  });
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    try {
      localStorage.setItem(storageKey, JSON.stringify(checked));
    } catch (_) {
      /* sin almacenamiento */
    }
  }, [checked, storageKey]);

  const done = checked.every(Boolean);

  async function complete() {
    setBusy(true);
    try {
      await onSubmit({ passed: true });
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="checklist stack">
      <ul>
        {exercise.items.map((item, index) => (
          <li key={index}>
            <label>
              <input
                type="checkbox"
                checked={checked[index]}
                onChange={() => setChecked((previous) => previous.map((value, i) => (i === index ? !value : value)))}
              />
              <span>{item}</span>
            </label>
          </li>
        ))}
      </ul>
      <div className="actions">
        <button className="btn primary" disabled={!done || busy || solved} onClick={complete}>
          {solved ? (
            <>
              <Check size={16} aria-hidden="true" /> Completado
            </>
          ) : (
            "Marcar como completado"
          )}
        </button>
        {!done && <span className="muted small">Marca todos los puntos para completarlo.</span>}
      </div>
    </div>
  );
}
