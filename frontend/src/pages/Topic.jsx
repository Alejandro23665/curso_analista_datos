import { useEffect, useRef, useState } from "react";
import { Link, useParams, useSearchParams } from "react-router-dom";
import { api } from "../api.js";
import ExercisePanel from "../components/ExercisePanel.jsx";
import Markdown from "../components/Markdown.jsx";
import SchemaPanel from "../components/SchemaPanel.jsx";
import { useAsync } from "../hooks.js";
import { prewarm } from "../pyRunner.js";
import { KINDS } from "../util.js";

const TABS = [
  { id: "teoria", label: "📖 Teoría" },
  { id: "practica", label: "🧪 Práctica" },
  { id: "apuntes", label: "📝 Apuntes" },
];

export default function Topic() {
  const { slug } = useParams();
  const [params, setParams] = useSearchParams();
  const tab = TABS.some((t) => t.id === params.get("tab")) ? params.get("tab") : "teoria";
  const { data: topic, loading, error, reload, setData } = useAsync(() => api.topic(slug), [slug]);

  useEffect(() => {
    window.scrollTo(0, 0);
  }, [slug, tab]);

  // Descarga Python por adelantado cuando entras a la práctica de un tema con ejercicios de código.
  useEffect(() => {
    if (!topic || tab !== "practica") return;
    const python = topic.exercises.filter((e) => e.kind === "python");
    if (python.length) prewarm([...new Set(python.flatMap((e) => e.packages))]);
  }, [topic, tab]);

  if (loading && !topic) return <div className="page muted">Cargando tema…</div>;
  if (error)
    return (
      <div className="page">
        <div className="card center">
          <h2>No se pudo cargar el tema</h2>
          <p className="muted">{error.message}</p>
          <button className="btn primary" onClick={reload}>
            Reintentar
          </button>
        </div>
      </div>
    );

  const progress = topic.progress;
  const goTab = (id) => setParams(id === "teoria" ? {} : { tab: id });

  async function toggleTheory() {
    const next = !progress.theory_done;
    const updated = await api.setTheory(topic.slug, next);
    setData((previous) => ({ ...previous, progress: updated }));
  }

  async function submitExercise(exercise, body) {
    const result = await api.submit(exercise.id, body);
    setData((previous) => ({
      ...previous,
      progress: result.progress,
      solved_ids:
        result.correct && !previous.solved_ids.includes(exercise.id)
          ? [...previous.solved_ids, exercise.id]
          : previous.solved_ids,
    }));
    return result;
  }

  return (
    <div className="page topic">
      <header className="topic-head card">
        <p className="eyebrow">
          <Link to="/ruta" className="link">
            Ruta
          </Link>{" "}
          · {topic.hours} h estimadas · {topic.exercise_count} ejercicios
        </p>
        <h1>{topic.title}</h1>
        <p className="muted">{topic.summary}</p>
        <div className="row between">
          <div className="bar wide">
            <span style={{ width: progress.percent + "%" }} />
          </div>
          <strong>{progress.percent}%</strong>
        </div>
        <nav className="tabs" role="tablist">
          {TABS.map((t) => (
            <button key={t.id} role="tab" aria-selected={tab === t.id} className={tab === t.id ? "active" : ""} onClick={() => goTab(t.id)}>
              {t.label}
            </button>
          ))}
        </nav>
      </header>

      {tab === "teoria" && (
        <section className="card theory">
          <Markdown>{topic.theory}</Markdown>
          <div className="row actions end">
            <button className={"btn " + (progress.theory_done ? "ghost" : "primary")} onClick={toggleTheory}>
              {progress.theory_done ? "✓ Teoría leída (deshacer)" : "Marcar teoría como leída"}
            </button>
            <button className="btn" onClick={() => goTab("practica")}>
              Ir a la práctica →
            </button>
          </div>
        </section>
      )}

      {tab === "practica" && <Practice key={topic.slug} topic={topic} onSubmit={submitExercise} />}

      {tab === "apuntes" && <Notes key={topic.slug} slug={topic.slug} initial={topic.note} />}

      <footer className="topic-nav">
        {topic.prev ? (
          <Link className="btn ghost" to={"/tema/" + topic.prev}>
            ← Tema anterior
          </Link>
        ) : (
          <span />
        )}
        {topic.next ? (
          <Link className="btn ghost" to={"/tema/" + topic.next}>
            Siguiente tema →
          </Link>
        ) : (
          <span />
        )}
      </footer>
    </div>
  );
}

function Practice({ topic, onSubmit }) {
  const [current, setCurrent] = useState(() => {
    const index = topic.exercises.findIndex((e) => !topic.solved_ids.includes(e.id));
    return index === -1 ? 0 : index;
  });
  const exercise = topic.exercises[Math.min(current, topic.exercises.length - 1)];
  const hasSql = topic.exercises.some((e) => e.kind === "sql");

  return (
    <div className="practice">
      <aside className="practice-side">
        <div className="card">
          <h4>
            Ejercicios ({topic.solved_ids.length}/{topic.exercises.length})
          </h4>
          <ol className="exercise-list">
            {topic.exercises.map((e, index) => {
              const done = topic.solved_ids.includes(e.id);
              return (
                <li key={e.id}>
                  <button className={(index === current ? "active " : "") + (done ? "done" : "")} onClick={() => setCurrent(index)}>
                    <span className="mark">{done ? "✓" : KINDS[e.kind].icon}</span>
                    <span>{e.title}</span>
                  </button>
                </li>
              );
            })}
          </ol>
        </div>
        {hasSql && <SchemaPanel />}
      </aside>

      <div className="practice-main card">
        <ExercisePanel
          key={exercise.id}
          exercise={exercise}
          solved={topic.solved_ids.includes(exercise.id)}
          onSubmit={(body) => onSubmit(exercise, body)}
        />
        <div className="row between exercise-nav">
          <button className="btn ghost" disabled={current === 0} onClick={() => setCurrent(current - 1)}>
            ← Anterior
          </button>
          <button className="btn ghost" disabled={current >= topic.exercises.length - 1} onClick={() => setCurrent(current + 1)}>
            Siguiente →
          </button>
        </div>
      </div>
    </div>
  );
}

function Notes({ slug, initial }) {
  const [text, setText] = useState(initial || "");
  const [state, setState] = useState("idle");
  const [preview, setPreview] = useState(false);
  const first = useRef(true);

  useEffect(() => {
    if (first.current) {
      first.current = false;
      return undefined;
    }
    setState("saving");
    const timer = setTimeout(() => {
      api
        .saveNote(slug, text)
        .then(() => setState("saved"))
        .catch(() => setState("error"));
    }, 800);
    return () => clearTimeout(timer);
  }, [text, slug]);

  const labels = { idle: "", saving: "Guardando…", saved: "✓ Guardado", error: "⚠ No se pudo guardar" };

  return (
    <section className="card notes">
      <div className="row between">
        <h3>Mis apuntes</h3>
        <div className="row">
          <span className={"muted small save-" + state}>{labels[state]}</span>
          <button className="btn ghost small" onClick={() => setPreview((value) => !value)}>
            {preview ? "✏️ Editar" : "👁 Vista previa"}
          </button>
        </div>
      </div>
      {preview ? (
        <div className="notes-preview">{text.trim() ? <Markdown>{text}</Markdown> : <p className="muted">Aún no hay apuntes.</p>}</div>
      ) : (
        <textarea
          value={text}
          onChange={(event) => setText(event.target.value)}
          placeholder={"Escribe aquí con Markdown: ideas clave, errores que cometiste, fórmulas, dudas para preguntar...\n\n## Lo que aprendí\n- ...\n\n## Errores que no quiero repetir\n- ..."}
          spellCheck="true"
        />
      )}
      <p className="muted small">Se guardan solos en tu base de datos. Admite Markdown (títulos, listas, tablas y bloques de código).</p>
    </section>
  );
}
