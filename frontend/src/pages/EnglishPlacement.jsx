import { useState } from "react";
import { Link } from "react-router-dom";
import { ArrowLeft, ArrowRight, Headphones, TriangleAlert } from "lucide-react";
import { api } from "../api.js";
import AudioButtons from "../english/AudioButtons.jsx";
import { useAsync } from "../hooks.js";

const DONT_KNOW = -1;

const LEVEL_TEXT = {
  A1: "Estás empezando. Empieza por el bloque A1 · Bases: ve despacio, usa el audio lento y repite mucho en voz alta.",
  A2: "Tienes bases. Empieza por las unidades A2 y avanza a B1 en cuanto te sientas cómodo.",
  B1: "Te defiendes. Empieza por las unidades B1: explicar proyectos, hacer buenas preguntas y escribir mensajes de trabajo.",
  B2: "Buen nivel. Ve a las unidades B2 y dedica mucho tiempo a hablar: es lo que más se nota en una entrevista.",
};

export default function EnglishPlacement() {
  const { data, loading, error, reload } = useAsync(() => api.english.placement(), []);
  const [started, setStarted] = useState(false);
  const [index, setIndex] = useState(0);
  const [answers, setAnswers] = useState({});
  const [result, setResult] = useState(null);
  const [busy, setBusy] = useState(false);
  const [sendError, setSendError] = useState("");

  if (loading && !data) return <div className="loading">Cargando…</div>;
  if (error)
    return (
      <div className="page narrow">
        <div className="empty">
          <p className="muted">{error.message}</p>
          <button className="btn primary" onClick={reload}>
            Reintentar
          </button>
        </div>
      </div>
    );

  const questions = data.questions;

  async function finish(final) {
    setBusy(true);
    setSendError("");
    try {
      setResult(await api.english.sendPlacement(final));
    } catch (e) {
      setSendError(e.message);
    } finally {
      setBusy(false);
    }
  }

  function choose(value) {
    const next = { ...answers, [questions[index].id]: value };
    setAnswers(next);
    if (index + 1 < questions.length) setIndex(index + 1);
    else finish(next);
  }

  if (result) return <PlacementResult result={result} />;

  if (!started)
    return (
      <div className="page narrow">
        <header className="page-head">
          <h1>¿Cuál es tu nivel de inglés?</h1>
          <p className="muted">
            {questions.length} preguntas de gramática, vocabulario y comprensión auditiva, de nivel A2 a B2. Tardarás unos 6 minutos.
          </p>
        </header>
        <ul className="ruled">
          <li>Las preguntas de escucha se oyen: sube el volumen. Puedes repetir el audio las veces que quieras.</li>
          <li>Si no sabes una respuesta, elige «No lo sé»: adivinar solo hace que el resultado sea menos útil.</li>
          <li>Puedes repetir la prueba cuando quieras para medir tu avance.</li>
        </ul>
        <div>
          <button className="btn primary" onClick={() => setStarted(true)}>
            Empezar <ArrowRight size={16} aria-hidden="true" />
          </button>
        </div>
      </div>
    );

  const q = questions[index];
  return (
    <div className="page narrow">
      <div className="row between">
        <span className="muted small num">
          Pregunta {index + 1} de {questions.length}
        </span>
        {index > 0 && (
          <button className="btn ghost small" onClick={() => setIndex(index - 1)} disabled={busy}>
            <ArrowLeft size={14} aria-hidden="true" /> Anterior
          </button>
        )}
      </div>
      <div className="meter" role="progressbar" aria-valuemin={0} aria-valuemax={questions.length} aria-valuenow={index}>
        <span style={{ width: (100 * index) / questions.length + "%" }} />
      </div>
      {q.kind === "listen" && (
        <div className="en-audio">
          <Headphones size={20} aria-hidden="true" />
          <AudioButtons key={q.id} text={q.audio} />
        </div>
      )}
      <h1 className="en-question" lang={q.kind === "listen" ? undefined : "en"}>
        {q.prompt}
      </h1>
      <ul className="options">
        {q.options.map((text, i) => (
          <li key={i}>
            <button className={"option" + (answers[q.id] === i ? " selected" : "")} disabled={busy} onClick={() => choose(i)}>
              {text}
            </button>
          </li>
        ))}
        <li>
          <button className="option dim" disabled={busy} onClick={() => choose(DONT_KNOW)}>
            No lo sé
          </button>
        </li>
      </ul>
      {busy && <p className="muted small">Calculando tu nivel…</p>}
      {sendError && (
        <p className="notice" role="alert">
          <TriangleAlert size={16} aria-hidden="true" />
          <span>
            {sendError}{" "}
            <button className="btn small" onClick={() => finish(answers)}>
              Reintentar
            </button>
          </span>
        </p>
      )}
    </div>
  );
}

function PlacementResult({ result }) {
  const wrong = result.review.filter((r) => !r.correct);
  return (
    <div className="page narrow">
      <header className="page-head">
        <h1>
          Tu nivel: <span className="hl">{result.level}</span>
        </h1>
        <p>{LEVEL_TEXT[result.level]}</p>
      </header>
      <dl className="ledger">
        {Object.entries(result.scores).map(([band, score]) => (
          <div key={band}>
            <dt>Preguntas {band}</dt>
            <dd>
              {Math.round(score * 100)}%
              <span className="meter" style={{ marginTop: 6 }}>
                <span style={{ width: score * 100 + "%" }} />
              </span>
            </dd>
          </div>
        ))}
      </dl>
      <div>
        <Link className="btn primary" to="/ingles">
          Ver mi plan de inglés <ArrowRight size={16} aria-hidden="true" />
        </Link>
      </div>
      {wrong.length > 0 && (
        <section className="module">
          <h2>Repasa estas preguntas</h2>
          <ol className="en-review">
            {wrong.map((r) => (
              <li key={r.id}>
                <span className="tag">{r.level}</span> {r.prompt}
                <br />
                <span className="small">
                  Correcta: <strong>{r.answer}</strong>
                  {r.chosen && <span className="muted"> · elegiste: {r.chosen}</span>}
                </span>
              </li>
            ))}
          </ol>
        </section>
      )}
    </div>
  );
}
