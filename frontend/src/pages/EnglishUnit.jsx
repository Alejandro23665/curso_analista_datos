import { useEffect, useState } from "react";
import { Link, useParams, useSearchParams } from "react-router-dom";
import { ArrowLeft, ArrowRight, BookOpen, Check, Clock, Headphones, Undo2 } from "lucide-react";
import { api } from "../api.js";
import Markdown from "../components/Markdown.jsx";
import Squares from "../components/Squares.jsx";
import AudioButtons from "../english/AudioButtons.jsx";
import EnglishExercise, { EN_KINDS } from "../english/EnglishExercise.jsx";
import { useAsync } from "../hooks.js";
import Loading from "../components/Loading.jsx";

const TABS = [
  { id: "leccion", label: "Lección", Icon: BookOpen },
  { id: "practica", label: "Práctica", Icon: Headphones },
];

export default function EnglishUnit() {
  const { slug } = useParams();
  const [params, setParams] = useSearchParams();
  const tab = TABS.some((t) => t.id === params.get("tab")) ? params.get("tab") : "leccion";
  const { data: unit, loading, error, reload, setData } = useAsync(() => api.english.unit(slug), [slug]);

  useEffect(() => {
    window.scrollTo(0, 0);
  }, [slug, tab]);

  if (loading && !unit) return <Loading text="Cargando unidad…" />;
  if (error)
    return (
      <div className="page narrow">
        <div className="empty">
          <h2>No se pudo cargar la unidad</h2>
          <p className="muted">{error.message}</p>
          <button className="btn primary" onClick={reload}>
            Reintentar
          </button>
        </div>
      </div>
    );

  const progress = unit.progress;
  const goTab = (id) => setParams(id === "leccion" ? {} : { tab: id });

  async function toggleLesson() {
    const updated = await api.english.setLesson(unit.slug, !progress.lesson_done);
    setData((previous) => ({ ...previous, progress: updated }));
  }

  async function submitExercise(exercise, body) {
    const result = await api.english.submit(exercise.id, body);
    setData((previous) => ({
      ...previous,
      progress: result.progress,
      solved_ids:
        result.correct && !previous.solved_ids.includes(exercise.id) ? [...previous.solved_ids, exercise.id] : previous.solved_ids,
    }));
    return result;
  }

  const exerciseItems = unit.exercises.map((e, i) => ({
    key: e.id,
    state: unit.solved_ids.includes(e.id) ? "done" : "todo",
    title: i + 1 + ". " + EN_KINDS[e.kind].label,
  }));

  return (
    <div className="page">
      <header className="topic-head">
        <h1 lang="en">{unit.title}</h1>
        <p className="summary">{unit.summary}</p>
        <div className="crumbs">
          <Link to="/ingles">Inglés</Link>
          <span className="tag level">{unit.level}</span>
          <span>{unit.focus_title}</span>
          <span>
            <Clock size={14} aria-hidden="true" /> {unit.minutes} min
          </span>
          {progress.lesson_done && (
            <span>
              <Check size={14} aria-hidden="true" /> Lección estudiada
            </span>
          )}
        </div>
        <div className="progress-line">
          <Squares label="Ejercicios de la unidad" items={exerciseItems} />
          <strong>{progress.percent}%</strong>
        </div>
      </header>

      <nav className="tabs" role="tablist" aria-label="Partes de la unidad">
        {TABS.map(({ id, label, Icon }) => (
          <button key={id} role="tab" aria-selected={tab === id} className={tab === id ? "active" : ""} onClick={() => goTab(id)}>
            <Icon size={16} aria-hidden="true" /> {label}
          </button>
        ))}
      </nav>

      {tab === "leccion" && (
        <section className="sheet">
          <Markdown selfCheck>{unit.lesson}</Markdown>
          <div className="markdown">
            <h2>Frases clave</h2>
            <p className="muted">
              Escúchalas y repítelas en voz alta hasta que te salgan sin leer. Debajo de cada una tienes cómo suena, escrito con
              letras del español: la tilde marca la sílaba fuerte.
            </p>
          </div>
          <ul className="en-phrases">
            {unit.phrases.map((phrase) => (
              <li key={phrase.en}>
                <div>
                  <strong lang="en">{phrase.en}</strong>
                  {phrase.pron && <span className="en-pron">{phrase.pron}</span>}
                  <span className="muted small">{phrase.es}</span>
                </div>
                <AudioButtons text={phrase.en} compact />
              </li>
            ))}
          </ul>
          <div className="sheet-actions">
            <button className={"btn " + (progress.lesson_done ? "" : "primary")} onClick={toggleLesson}>
              {progress.lesson_done ? (
                <>
                  <Undo2 size={16} aria-hidden="true" /> Desmarcar lección
                </>
              ) : (
                <>
                  <Check size={16} aria-hidden="true" /> Marcar lección como estudiada
                </>
              )}
            </button>
            <button className="btn" onClick={() => goTab("practica")}>
              Ir a la práctica <ArrowRight size={16} aria-hidden="true" />
            </button>
          </div>
        </section>
      )}

      {tab === "practica" && <Practice key={unit.slug} unit={unit} onSubmit={submitExercise} />}

      <footer className="topic-nav">
        {unit.prev ? (
          <Link className="btn ghost" to={"/ingles/unidad/" + unit.prev}>
            <ArrowLeft size={16} aria-hidden="true" /> Unidad anterior
          </Link>
        ) : (
          <span />
        )}
        {unit.next ? (
          <Link className="btn ghost" to={"/ingles/unidad/" + unit.next}>
            Siguiente unidad <ArrowRight size={16} aria-hidden="true" />
          </Link>
        ) : (
          <span />
        )}
      </footer>
    </div>
  );
}

function Practice({ unit, onSubmit }) {
  const [current, setCurrent] = useState(() => {
    const index = unit.exercises.findIndex((e) => !unit.solved_ids.includes(e.id));
    return index === -1 ? 0 : index;
  });
  const exercise = unit.exercises[Math.min(current, unit.exercises.length - 1)];
  const solved = unit.solved_ids.includes(exercise.id);

  return (
    <div className="practice">
      <aside className="practice-side">
        <div>
          <h2>
            Ejercicios{" "}
            <span className="muted small num">
              {unit.solved_ids.length}/{unit.exercises.length}
            </span>
          </h2>
          <ol className="exercise-list">
            {unit.exercises.map((e, index) => {
              const done = unit.solved_ids.includes(e.id);
              const { Icon, label } = EN_KINDS[e.kind];
              return (
                <li key={e.id}>
                  <button className={index === current ? "active" : ""} onClick={() => setCurrent(index)} aria-current={index === current ? "step" : undefined}>
                    <span className={"sq " + (done ? "done" : "")} aria-label={done ? "Resuelto" : "Pendiente"} />
                    <span>
                      {index + 1}. {label}
                    </span>
                    <span className="kind">
                      <Icon size={14} aria-hidden="true" />
                    </span>
                  </button>
                </li>
              );
            })}
          </ol>
        </div>
      </aside>

      <div className="practice-main">
        <EnglishExercise key={exercise.id} exercise={exercise} index={current + 1} solved={solved} onSubmit={(body) => onSubmit(exercise, body)} />
        <div className="exercise-nav">
          <button className="btn ghost" disabled={current === 0} onClick={() => setCurrent(current - 1)}>
            <ArrowLeft size={16} aria-hidden="true" /> Anterior
          </button>
          <button className={"btn" + (solved ? " primary" : "")} disabled={current >= unit.exercises.length - 1} onClick={() => setCurrent(current + 1)}>
            Siguiente <ArrowRight size={16} aria-hidden="true" />
          </button>
        </div>
      </div>
    </div>
  );
}
