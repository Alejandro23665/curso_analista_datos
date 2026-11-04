import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { TriangleAlert } from "lucide-react";
import { api } from "../api.js";
import AudioButtons from "../english/AudioButtons.jsx";
import { canSpeak, speak } from "../english/speech.js";
import { useAsync } from "../hooks.js";

const GRADES = [
  { id: "otra", label: "Otra vez", help: "No me acordaba" },
  { id: "dificil", label: "Difícil", help: "Me costó" },
  { id: "bien", label: "Bien", help: "La sabía" },
  { id: "facil", label: "Fácil", help: "Sin dudar" },
];

const FOCUS_TITLE = { entrevistas: "Entrevistas", freelance: "Clientes", equipo: "Equipo", tecnico: "Técnico" };

// Caja siguiente según la calificación (igual que en el servidor) para mostrar cuándo vuelve la tarjeta.
function nextBox(box, grade, top) {
  if (grade === "otra") return 0;
  if (grade === "dificil") return Math.max(1, box);
  if (grade === "bien") return Math.min(box + 1, top);
  return Math.min(box + 2, top);
}

function when(days) {
  if (days === 0) return "hoy";
  if (days === 1) return "mañana";
  if (days < 30) return days + " días";
  return Math.round(days / 30) + (days < 60 ? " mes" : " meses");
}

export default function EnglishVocab() {
  const { data, loading, error, reload } = useAsync(() => api.english.vocab(), []);
  const [queue, setQueue] = useState(null);
  const [revealed, setRevealed] = useState(false);
  const [done, setDone] = useState(0);
  const [busy, setBusy] = useState(false);
  const [saveError, setSaveError] = useState("");

  useEffect(() => {
    if (data) setQueue(data.cards);
  }, [data]);

  const card = queue && queue[0];
  useEffect(() => {
    setRevealed(false);
    if (card && canSpeak()) speak(card.en);
  }, [card]);

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
  if ((loading && !data) || !queue) return <div className="loading">Cargando tarjetas…</div>;

  async function grade(id) {
    setBusy(true);
    setSaveError("");
    try {
      await api.english.grade(card.id, id);
      setDone((n) => n + 1);
      // "Otra vez": la tarjeta vuelve al final de la sesión de hoy.
      setQueue((previous) => {
        const rest = previous.slice(1);
        return id === "otra" ? [...rest, { ...previous[0], box: 0, is_new: false }] : rest;
      });
    } catch (e) {
      setSaveError(e.message);
    } finally {
      setBusy(false);
    }
  }

  if (!card)
    return (
      <div className="page narrow">
        <div className="empty">
          <h1>{done ? "Repaso terminado" : "Nada que repasar por ahora"}</h1>
          <p className="muted">
            {done
              ? "Repasaste " + done + " tarjetas. Las que te costaron volverán antes; las fáciles, dentro de más días."
              : "Ya repasaste todo lo pendiente y las tarjetas nuevas de hoy. Vuelve mañana."}
          </p>
          <div className="actions">
            <Link className="btn primary" to="/ingles">
              Volver a Inglés
            </Link>
            {done > 0 && (
              <button className="btn" onClick={() => reload()}>
                Comprobar si hay más
              </button>
            )}
          </div>
        </div>
      </div>
    );

  const top = data.intervals.length - 1;
  return (
    <div className="page narrow">
      <header className="page-head">
        <h1>Vocabulario</h1>
        <p className="muted">Di la palabra en español antes de darle la vuelta. Califícate con honestidad: eso decide cuándo vuelve cada tarjeta.</p>
        <p className="muted small num">
          Quedan {queue.length} · repasadas en esta sesión: {done} · aprendidas: {data.counts.learned}/{data.counts.total}
        </p>
      </header>

      <section className="graph card-sheet en-vocab" aria-live="polite">
        <div className="row">
          <span className="tag">
            {card.level} · {FOCUS_TITLE[card.focus] || card.focus}
          </span>
          {card.is_new && <span className="tag next">Nueva</span>}
        </div>
        <p className="en-card-front" lang="en">
          {card.en}
        </p>
        {card.pron && <p className="en-pron en-card-pron">Suena: {card.pron}</p>}
        <AudioButtons text={card.en} />
        {revealed ? (
          <>
            <p className="en-card-back">
              <span className="hl">{card.es}</span>
            </p>
            <p className="en-card-example" lang="en">
              «{card.example}» <AudioButtons text={card.example} compact />
            </p>
            <div className="en-grades">
              {GRADES.map((g) => (
                <button key={g.id} className={"btn" + (g.id === "bien" ? " primary" : "")} disabled={busy} onClick={() => grade(g.id)}>
                  {g.label}
                  <small>
                    {g.help} · {when(data.intervals[nextBox(card.box, g.id, top)])}
                  </small>
                </button>
              ))}
            </div>
          </>
        ) : (
          <button className="btn primary" onClick={() => setRevealed(true)}>
            Mostrar respuesta
          </button>
        )}
        {saveError && (
          <p className="notice" role="alert">
            <TriangleAlert size={16} aria-hidden="true" /> <span>{saveError}</span>
          </p>
        )}
      </section>
    </div>
  );
}
