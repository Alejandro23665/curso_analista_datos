import { useEffect, useRef, useState } from "react";
import { Link, useParams, useSearchParams } from "react-router-dom";
import { ArrowLeft, ArrowRight, BookOpen, Check, Clock, Eye, FlaskConical, ListChecks, NotebookPen, PenLine, Undo2 } from "lucide-react";
import { api } from "../api.js";
import ExercisePanel from "../components/ExercisePanel.jsx";
import Markdown from "../components/Markdown.jsx";
import SchemaPanel from "../components/SchemaPanel.jsx";
import Squares from "../components/Squares.jsx";
import { useAsync } from "../hooks.js";
import { useTrack } from "../track.jsx";
import { prewarm } from "../pyRunner.js";
import { KINDS } from "../util.js";

const TABS = [
  { id: "teoria", label: "Teoría", Icon: BookOpen },
  { id: "practica", label: "Práctica", Icon: FlaskConical },
  { id: "apuntes", label: "Apuntes", Icon: NotebookPen },
];

export default function Topic() {
  const { slug } = useParams();
  const [params, setParams] = useSearchParams();
  const tab = TABS.some((t) => t.id === params.get("tab")) ? params.get("tab") : "teoria";
  const { track, setTrack } = useTrack();
  const { data: topic, loading, error, reload, setData } = useAsync(() => api.topic(slug, track), [slug, track]);

  useEffect(() => {
    window.scrollTo(0, 0);
  }, [slug, tab]);

  // Descarga Python por adelantado cuando entras a la práctica de un tema con ejercicios de código.
  useEffect(() => {
    if (!topic || tab !== "practica") return;
    const python = topic.exercises.filter((e) => e.kind === "python");
    if (python.length) prewarm([...new Set(python.flatMap((e) => e.packages))]);
  }, [topic, tab]);

  if (loading && !topic) return <div className="loading">Cargando tema…</div>;
  if (error)
    return (
      <div className="page narrow">
        <div className="empty">
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
        result.correct && !previous.solved_ids.includes(exercise.id) ? [...previous.solved_ids, exercise.id] : previous.solved_ids,
    }));
    return result;
  }

  const exerciseItems = topic.exercises.map((e, i) => ({
    key: e.id,
    state: topic.solved_ids.includes(e.id) ? "done" : "todo",
    title: (i + 1) + ". " + e.title,
  }));

  return (
    <div className="page">
      <header className="topic-head">
        <h1>{topic.title}</h1>
        <p className="summary">{topic.summary}</p>
        <div className="crumbs">
          <Link to="/ruta">{topic.track.title}</Link>
          <span>
            <Clock size={14} aria-hidden="true" /> {topic.hours} h estimadas
          </span>
          <span>
            <ListChecks size={14} aria-hidden="true" /> {topic.exercise_count} ejercicios
          </span>
          {progress.theory_done && (
            <span>
              <Check size={14} aria-hidden="true" /> Teoría leída
            </span>
          )}
        </div>
        {topic.tracks.length > 1 && (
          <div className="row">
            <span className="muted small">Cuenta en las rutas:</span>
            {topic.tracks.map((t) => (
              <button
                key={t.slug}
                type="button"
                className={"tag" + (t.slug === topic.track.slug ? " current" : "")}
                onClick={() => setTrack(t.slug)}
                title={t.slug === topic.track.slug ? "Ruta actual" : "Cambiar a esta ruta"}
              >
                {t.title}
              </button>
            ))}
          </div>
        )}
        <div className="progress-line">
          <Squares label="Ejercicios del tema" items={exerciseItems} />
          <strong>{progress.percent}%</strong>
        </div>
      </header>

      <nav className="tabs" role="tablist" aria-label="Partes del tema">
        {TABS.map(({ id, label, Icon }) => (
          <button key={id} role="tab" aria-selected={tab === id} className={tab === id ? "active" : ""} onClick={() => goTab(id)}>
            <Icon size={16} aria-hidden="true" /> {label}
          </button>
        ))}
      </nav>

      {tab === "teoria" && (
        <section className="sheet">
          <Markdown>{topic.theory}</Markdown>
          <div className="sheet-actions">
            <button className={"btn " + (progress.theory_done ? "" : "primary")} onClick={toggleTheory}>
              {progress.theory_done ? (
                <>
                  <Undo2 size={16} aria-hidden="true" /> Desmarcar teoría leída
                </>
              ) : (
                <>
                  <Check size={16} aria-hidden="true" /> Marcar teoría como leída
                </>
              )}
            </button>
            <button className="btn" onClick={() => goTab("practica")}>
              Ir a la práctica <ArrowRight size={16} aria-hidden="true" />
            </button>
          </div>
        </section>
      )}

      {tab === "practica" && <Practice key={topic.slug} topic={topic} onSubmit={submitExercise} />}

      {tab === "apuntes" && <Notes key={topic.slug} slug={topic.slug} initial={topic.note} />}

      <footer className="topic-nav">
        {topic.prev ? (
          <Link className="btn ghost" to={"/tema/" + topic.prev}>
            <ArrowLeft size={16} aria-hidden="true" /> Tema anterior
          </Link>
        ) : (
          <span />
        )}
        {topic.next ? (
          <Link className="btn ghost" to={"/tema/" + topic.next}>
            Siguiente tema <ArrowRight size={16} aria-hidden="true" />
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
        <div>
          <h2>
            Ejercicios{" "}
            <span className="muted small num">
              {topic.solved_ids.length}/{topic.exercises.length}
            </span>
          </h2>
          <ol className="exercise-list">
            {topic.exercises.map((e, index) => {
              const done = topic.solved_ids.includes(e.id);
              const { Icon, label } = KINDS[e.kind];
              return (
                <li key={e.id}>
                  <button className={index === current ? "active" : ""} onClick={() => setCurrent(index)} aria-current={index === current ? "step" : undefined}>
                    <span className={"sq " + (done ? "done" : "")} aria-label={done ? "Resuelto" : "Pendiente"} />
                    <span>{e.title}</span>
                    <span className="kind" title={label}>
                      <Icon size={14} aria-label={label} />
                    </span>
                  </button>
                </li>
              );
            })}
          </ol>
        </div>
        {hasSql && <SchemaPanel />}
      </aside>

      <div className="practice-main">
        <ExercisePanel
          key={exercise.id}
          exercise={exercise}
          solved={topic.solved_ids.includes(exercise.id)}
          onSubmit={(body) => onSubmit(exercise, body)}
        />
        <div className="exercise-nav">
          <button className="btn ghost" disabled={current === 0} onClick={() => setCurrent(current - 1)}>
            <ArrowLeft size={16} aria-hidden="true" /> Anterior
          </button>
          <button className="btn" disabled={current >= topic.exercises.length - 1} onClick={() => setCurrent(current + 1)}>
            Siguiente <ArrowRight size={16} aria-hidden="true" />
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

  const labels = { idle: "", saving: "Guardando…", saved: "Guardado", error: "No se pudo guardar" };

  return (
    <section className="notes">
      <div className="row between">
        <h2>Mis apuntes</h2>
        <div className="row">
          <span className={"small save-" + state} aria-live="polite">
            {labels[state]}
          </span>
          <button className="btn small" onClick={() => setPreview((value) => !value)}>
            {preview ? (
              <>
                <PenLine size={14} aria-hidden="true" /> Editar
              </>
            ) : (
              <>
                <Eye size={14} aria-hidden="true" /> Vista previa
              </>
            )}
          </button>
        </div>
      </div>
      {preview ? (
        <div className="notes-preview sheet">{text.trim() ? <Markdown>{text}</Markdown> : <p className="muted">Aún no hay apuntes.</p>}</div>
      ) : (
        <textarea
          value={text}
          onChange={(event) => setText(event.target.value)}
          aria-label="Apuntes del tema"
          placeholder={"Escribe aquí con Markdown: ideas clave, errores que cometiste, dudas para preguntar...\n\n## Lo que aprendí\n- ...\n\n## Errores que no quiero repetir\n- ..."}
          spellCheck="true"
        />
      )}
      <p className="muted small">Se guardan solos en tu base de datos. Admite Markdown: títulos, listas, tablas y bloques de código.</p>
    </section>
  );
}
