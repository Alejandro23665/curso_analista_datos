import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { ArrowRight, Layers, Mic, TriangleAlert, Volume2 } from "lucide-react";
import { api } from "../api.js";
import Squares, { exerciseSquares, SquaresLegend } from "../components/Squares.jsx";
import { canListen, canSpeak, englishVoices, getSettings, saveSettings, speak } from "../english/speech.js";
import { useAsync } from "../hooks.js";
import { formatDate, percent, STATUS } from "../util.js";
import Loading from "../components/Loading.jsx";

const LEVEL_TEXT = {
  A1: "Empieza por el bloque A1 · Bases. Usa siempre el audio lento, repite cada frase en voz alta y haz el vocabulario a diario.",
  A2: "Tienes bases. Empieza por las unidades A2 para ganar soltura y pasa pronto a B1.",
  B1: "Te defiendes. Las unidades B1 te preparan para explicar proyectos y trabajar con clientes.",
  B2: "Buen nivel. Pule las unidades B2 (negociar, revisar código, incidentes) y practica entrevistas en voz alta.",
};

export default function English() {
  const { data, loading, error, reload } = useAsync(() => api.english.overview(), []);

  if (loading && !data) return <Loading text="Cargando…" />;
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

  const { placement, next_unit: next, vocab } = data;
  const nextSlug = next && next.slug;
  const pending = vocab.due + vocab.new_available;

  return (
    <div className="page">
      <section className="next-block">
        <div>
          {next ? (
            <h1>
              Inglés: sigue con <span className="hl" lang="en">{next.title}</span>
            </h1>
          ) : (
            <h1>
              Inglés: <span className="hl green">todas las unidades completadas</span>
            </h1>
          )}
          <p className="lede">
            Entrevistas, clientes, trabajo en equipo e inglés técnico. Escucha, completa, traduce y habla; la corrección es automática.
          </p>
          <p className="meta">
            {placement ? (
              <>
                <span>
                  Tu nivel <span className="tag level">{placement.level}</span>
                </span>
                <span>
                  Prueba del {formatDate(placement.date)} · <Link to="/ingles/prueba">repetir</Link>
                </span>
              </>
            ) : (
              <span>Aún no sabes tu nivel: la prueba son 18 preguntas, unos 6 minutos.</span>
            )}
          </p>
        </div>
        <div className="actions">
          {!placement && (
            <Link className="btn primary" to="/ingles/prueba">
              Hacer la prueba de nivel
            </Link>
          )}
          {next && (
            <Link className={"btn" + (placement ? " primary" : "")} to={"/ingles/unidad/" + next.slug}>
              {next.status === "pendiente" ? "Empezar" : "Continuar"} <ArrowRight size={16} aria-hidden="true" />
            </Link>
          )}
          <Link className="btn" to="/ingles/vocabulario">
            <Layers size={16} aria-hidden="true" /> Vocabulario {pending > 0 && <span className="tag next num">{pending}</span>}
          </Link>
        </div>
      </section>

      {placement && <p className="notice">{LEVEL_TEXT[placement.level]}</p>}

      <dl className="ledger">
        <div>
          <dt>Unidades completadas</dt>
          <dd>
            {data.units_completed} / {data.units_total}
            <small>{data.percent}% del inglés</small>
          </dd>
        </div>
        {data.focus.map((f) => (
          <div key={f.slug}>
            <dt>{f.title}</dt>
            <dd>
              {f.percent}%<small>{f.attempts ? "Acierto " + percent(f.accuracy) + " en " + f.attempts + " intentos" : "Sin practicar"}</small>
            </dd>
          </div>
        ))}
        <div>
          <dt>Palabras aprendidas</dt>
          <dd>
            {vocab.learned} / {vocab.total}
            <small>
              {vocab.due} para repasar hoy · {vocab.new_available} nuevas
            </small>
          </dd>
        </div>
      </dl>

      <SquaresLegend />

      {data.levels.map((level) => {
        const done = level.units.filter((u) => u.status === "completado").length;
        return (
          <section key={level.slug} className="section-block">
            <div className="section-head">
              <div>
                <h2 className="row">
                  {level.title}
                  {level.slug === data.start_level && placement && <span className="tag next">Empieza aquí</span>}
                </h2>
                <p className="muted">{level.description}</p>
              </div>
              <span className="figure">
                {done}
                <small>/{level.units.length}</small>
              </span>
            </div>
            <ul className="topic-rows">
              {level.units.map((unit) => {
                const isNext = unit.slug === nextSlug;
                return (
                  <li key={unit.slug}>
                    <Link to={"/ingles/unidad/" + unit.slug} className={"topic-row" + (isNext ? " next" : "")}>
                      <span className={"sq " + (isNext ? "next" : STATUS[unit.status].square)} aria-label={isNext ? "Siguiente" : STATUS[unit.status].label} />
                      <span className="title">
                        <span lang="en">{unit.title}</span>
                        <small>
                          {unit.focus_title} · {unit.minutes} min{isNext && " · siguiente"}
                        </small>
                      </span>
                      <Squares size="small" label={unit.solved + " de " + unit.total + " ejercicios"} items={exerciseSquares(unit.solved, unit.total)} />
                      <span className={"pct" + (unit.percent ? "" : " zero")}>{unit.percent}%</span>
                    </Link>
                  </li>
                );
              })}
            </ul>
          </section>
        );
      })}

      <div className="cols">
        <section className="module">
          <h2>Tu rutina diaria, 45-60 min</h2>
          <ol className="review-list">
            <li>
              <strong>10 min de vocabulario:</strong> repasa las tarjetas del día; las difíciles vuelven antes.
            </li>
            <li>
              <strong>20-30 min, una unidad:</strong> lee la lección, escucha las frases clave y haz los ejercicios.
            </li>
            <li>
              <strong>5 min en voz alta:</strong> repite tu presentación y explica un proyecto sin leer.
            </li>
          </ol>
          <p className="muted small">Fuera de la plataforma: lee documentación en inglés y escribe en inglés tus README y commits.</p>
        </section>
        <VoiceSettings />
      </div>
    </div>
  );
}

function VoiceSettings() {
  const [voices, setVoices] = useState(englishVoices());
  const [settings, setSettings] = useState(getSettings());

  useEffect(() => {
    if (!canSpeak()) return undefined;
    const update = () => setVoices(englishVoices());
    window.speechSynthesis.addEventListener("voiceschanged", update);
    update();
    return () => window.speechSynthesis.removeEventListener("voiceschanged", update);
  }, []);

  function change(patch) {
    saveSettings(patch);
    setSettings(getSettings());
  }

  return (
    <section className="module voice-settings">
      <h2>Audio y micrófono</h2>
      {canSpeak() ? (
        <>
          <label className="field">
            <span>Voz</span>
            <select value={settings.voice} onChange={(event) => change({ voice: event.target.value })}>
              <option value="">Automática (inglés de EE. UU.)</option>
              {voices.map((v) => (
                <option key={v.name} value={v.name}>
                  {v.name} ({v.lang})
                </option>
              ))}
            </select>
          </label>
          <label className="field">
            <span className="num">Velocidad: {settings.rate.toFixed(2)}×</span>
            <input type="range" min="0.6" max="1.2" step="0.05" value={settings.rate} onChange={(event) => change({ rate: event.target.value })} />
          </label>
          <div>
            <button className="btn small" onClick={() => speak("Hi! I'm a Python developer focused on AI applications.")}>
              <Volume2 size={15} aria-hidden="true" /> Probar la voz
            </button>
          </div>
        </>
      ) : (
        <p className="notice">
          <TriangleAlert size={16} aria-hidden="true" />
          <span>Tu navegador no puede leer en voz alta: los ejercicios de escucha no funcionarán aquí.</span>
        </p>
      )}
      <p className="muted small row">
        <Mic size={15} aria-hidden="true" />
        {canListen()
          ? "Reconocimiento de voz disponible. La primera vez el navegador te pedirá permiso para usar el micrófono."
          : "Este navegador no tiene reconocimiento de voz; usa Chrome o Edge para los ejercicios de hablar. Mientras, podrás escribir la frase."}
      </p>
    </section>
  );
}
