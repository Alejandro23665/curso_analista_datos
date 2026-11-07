import { useEffect, useState } from "react";
import { ArrowDown, ArrowUp, Check, CircleCheck, CircleX, Eye, GripVertical, Lightbulb, Play } from "lucide-react";
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
      {exercise.kind === "parsons" && <ParsonsExercise exercise={exercise} onSubmit={onSubmit} />}
      {exercise.kind === "predict" && <PredictExercise exercise={exercise} onSubmit={onSubmit} />}
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

// Ordenar líneas de código: se mueven con los botones, con el teclado o arrastrando.
function ParsonsExercise({ exercise, onSubmit }) {
  const [blocks, setBlocks] = useState(exercise.blocks);
  const [result, setResult] = useState(null);
  const [busy, setBusy] = useState(false);
  const [dragging, setDragging] = useState(null);
  const [explain, setExplain] = useState(false);

  function move(from, to) {
    if (to < 0 || to >= blocks.length || from === to) return;
    setBlocks((list) => {
      const next = [...list];
      const [item] = next.splice(from, 1);
      next.splice(to, 0, item);
      return next;
    });
    setResult(null);
  }

  async function check() {
    setBusy(true);
    setExplain(false);
    try {
      setResult(await onSubmit({ order: blocks.map((b) => b.id) }));
    } finally {
      setBusy(false);
    }
  }

  const locked = Boolean(result && result.correct);
  return (
    <div className="stack">
      <ol className="parsons" aria-label="Líneas de código para ordenar">
        {blocks.map((block, index) => {
          const wrong = result && !result.correct && result.first_wrong === index;
          return (
            <li
              key={block.id}
              className={"parsons-line" + (dragging === index ? " dragging" : "") + (wrong ? " wrong" : "") + (locked ? " right" : "")}
              draggable={!locked}
              onDragStart={() => setDragging(index)}
              onDragEnd={() => setDragging(null)}
              onDragOver={(event) => event.preventDefault()}
              onDrop={() => {
                if (dragging !== null) move(dragging, index);
                setDragging(null);
              }}
            >
              <GripVertical size={16} aria-hidden="true" className="grip" />
              <code>{block.text || " "}</code>
              <span className="parsons-moves">
                <button className="btn ghost icon" disabled={locked || index === 0} onClick={() => move(index, index - 1)} aria-label={"Subir la línea " + (index + 1)}>
                  <ArrowUp size={15} aria-hidden="true" />
                </button>
                <button className="btn ghost icon" disabled={locked || index === blocks.length - 1} onClick={() => move(index, index + 1)} aria-label={"Bajar la línea " + (index + 1)}>
                  <ArrowDown size={15} aria-hidden="true" />
                </button>
              </span>
            </li>
          );
        })}
      </ol>
      <div className="actions">
        <button className="btn primary" disabled={busy || locked} onClick={check}>
          <Check size={16} aria-hidden="true" /> Comprobar orden
        </button>
        <span className="muted small push">La sangría ya viene puesta: solo cambia el orden.</span>
      </div>
      {result && (
        <div className="console" aria-live="polite">
          {result.correct ? (
            <Verdict ok>Correcto: el programa está en orden.</Verdict>
          ) : (
            <Verdict>Aún no. La primera línea fuera de sitio está marcada en rojo.</Verdict>
          )}
          {(result.correct || explain) && result.explanation && <p>{result.explanation}</p>}
          {!result.correct && !explain && result.explanation && (
            <div>
              <button className="btn ghost small" onClick={() => setExplain(true)}>
                Ver explicación
              </button>
            </div>
          )}
        </div>
      )}
      {exercise.hint && <HintOnly hint={exercise.hint} />}
    </div>
  );
}

// Seguir el código a mano y escribir lo que imprime (sin ejecutarlo).
function PredictExercise({ exercise, onSubmit }) {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [busy, setBusy] = useState(false);
  const [reveal, setReveal] = useState(false);

  async function check() {
    setBusy(true);
    try {
      setResult(await onSubmit({ text }));
    } finally {
      setBusy(false);
    }
  }

  const locked = Boolean(result && result.correct);
  return (
    <div className="stack">
      <CodeBlock code={exercise.code} lang="python" />
      <label className="predict-label">
        <span className="small muted">Salida exacta (una línea por cada print):</span>
        <textarea
          className="predict-input"
          value={text}
          onChange={(event) => {
            setText(event.target.value);
            setResult(null);
          }}
          disabled={locked}
          rows={4}
          spellCheck="false"
          autoComplete="off"
        />
      </label>
      <div className="actions">
        <button className="btn primary" disabled={busy || locked || !text.trim()} onClick={check}>
          <Check size={16} aria-hidden="true" /> Comprobar
        </button>
        <span className="muted small push">Hazlo a mano, con una tabla de variables: no lo ejecutes.</span>
      </div>
      {result && (
        <div className="console" aria-live="polite">
          {result.correct ? <Verdict ok>Correcto: seguiste bien el código.</Verdict> : <Verdict>No coincide. Repasa el código línea a línea.</Verdict>}
          {(result.correct || reveal) && (
            <>
              {!result.correct && <pre>{result.expected}</pre>}
              <p>{result.explanation}</p>
            </>
          )}
          {!result.correct && !reveal && (
            <div>
              <button className="btn ghost small" onClick={() => setReveal(true)}>
                Ver la salida correcta y la explicación
              </button>
            </div>
          )}
        </div>
      )}
      {exercise.hint && <HintOnly hint={exercise.hint} />}
    </div>
  );
}

function HintOnly({ hint }) {
  const [open, setOpen] = useState(false);
  return (
    <div className="helpers">
      <div className="actions">
        <button className="btn ghost small" onClick={() => setOpen((value) => !value)}>
          <Lightbulb size={14} aria-hidden="true" /> {open ? "Ocultar pista" : "Pista"}
        </button>
      </div>
      {open && (
        <p className="hint">
          <Lightbulb size={16} aria-hidden="true" /> <span>{hint}</span>
        </p>
      )}
    </div>
  );
}
