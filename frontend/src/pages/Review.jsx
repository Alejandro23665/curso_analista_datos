import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { ArrowRight, BookOpen, CalendarClock, Check, Swords } from "lucide-react";
import { api } from "../api.js";
import ExercisePanel from "../components/ExercisePanel.jsx";
import Squares from "../components/Squares.jsx";
import { useAsync } from "../hooks.js";
import { prewarm } from "../pyRunner.js";
import { useGame } from "../study/game.jsx";

const BOX_LABEL = ["Recién fallado o nuevo", "Repaso a los 3 días", "Repaso a la semana", "Repaso a las 3 semanas", "Dominado"];

// Repaso del día: ejercicios de temas anteriores que tocan hoy según la repetición espaciada, mezclados entre temas,
// más el desafío del día y los temas con la teoría leída pero la práctica pendiente.
export default function Review() {
  const { data, loading, error, reload } = useAsync(() => api.review(), []);
  const { afterSubmit } = useGame();
  const [index, setIndex] = useState(0);
  const [answered, setAnswered] = useState({}); // id -> correcto
  const [challengeOpen, setChallengeOpen] = useState(false);
  const [challengeDone, setChallengeDone] = useState(false);

  useEffect(() => {
    if (!data) return;
    const packages = data.items.filter((i) => i.exercise.kind === "python").flatMap((i) => i.exercise.packages);
    if (data.items.some((i) => i.exercise.kind === "python")) prewarm([...new Set(packages)]);
  }, [data]);

  if (loading && !data) return <div className="loading">Preparando tu repaso…</div>;
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

  const items = data.items;
  const current = items[Math.min(index, items.length - 1)];
  const doneCount = Object.keys(answered).length;
  const finished = items.length > 0 && doneCount >= items.length;

  async function submit(exercise, body, mode) {
    const result = await api.submit(exercise.id, { ...body, mode });
    afterSubmit(result);
    if (mode === "review") setAnswered((prev) => (exercise.id in prev ? prev : { ...prev, [exercise.id]: result.correct }));
    if (mode === "challenge" && result.correct) setChallengeDone(true);
    return result;
  }

  const squares = items.map((item, i) => ({
    key: item.exercise.id,
    state: item.exercise.id in answered ? (answered[item.exercise.id] ? "done" : "doing") : i === index ? "next" : "todo",
    title: item.topic.title,
  }));

  return (
    <div className="page">
      <header className="page-head">
        <h1>
          Repaso <span className="hl">del día</span>
        </h1>
        <p className="muted">
          Ejercicios de temas que ya estudiaste, justo cuando empiezas a olvidarlos. Recordar con esfuerzo es lo que fija lo aprendido; mezclar temas
          ayuda todavía más. Un fallo no es malo: ese ejercicio volverá mañana.
        </p>
      </header>

      {data.challenge && (
        <section className={"challenge" + (data.challenge.done || challengeDone ? " done" : "")}>
          <div className="row between">
            <h2>
              <Swords size={20} aria-hidden="true" /> Desafío del día
            </h2>
            <span className="tag next">+{data.challenge.xp} XP</span>
          </div>
          {data.challenge.done || challengeDone ? (
            <p>
              <Check size={16} aria-hidden="true" /> Superado. Mañana habrá otro.
            </p>
          ) : challengeOpen ? (
            <ExercisePanel
              exercise={data.challenge.exercise}
              solved={false}
              onSubmit={(body) => submit(data.challenge.exercise, body, "challenge")}
            />
          ) : (
            <div className="row between">
              <p className="muted">Un ejercicio sorpresa de un tema que ya empezaste: <strong>{data.challenge.topic.title}</strong>.</p>
              <button className="btn primary" onClick={() => setChallengeOpen(true)}>
                Aceptar el desafío
              </button>
            </div>
          )}
        </section>
      )}

      <section className="module">
        <div className="module-head">
          <h2>
            <CalendarClock size={20} aria-hidden="true" /> Tus repasos de hoy
          </h2>
          <span className="muted small num">
            {data.due_total > items.length
              ? "Tienes " + data.due_total + " pendientes; hoy van " + items.length + " (máximo " + data.session_size + " al día)."
              : items.length + " para hoy"}
            {data.done_today ? " · ya hiciste " + data.done_today + " hoy" : ""}
          </span>
        </div>

        {items.length === 0 ? (
          <div className="empty">
            <h3>{data.done_today ? "Repaso de hoy terminado" : "Nada que repasar hoy"}</h3>
            <p className="muted">
              {data.done_today
                ? "Buen trabajo. Lo que acertaste volverá dentro de unos días; lo que fallaste, mañana."
                : "Los ejercicios que resuelvas o falles en los temas aparecerán aquí cuando toque repasarlos."}
            </p>
          </div>
        ) : finished ? (
          <div className="empty">
            <h3>Repaso de hoy terminado</h3>
            <p className="muted num">
              Acertaste {Object.values(answered).filter(Boolean).length} de {items.length}. Los fallados vuelven mañana; los acertados, más adelante.
            </p>
            <Squares label="Resultado del repaso" items={squares} />
          </div>
        ) : (
          <>
            <div className="row between">
              <Squares label="Progreso del repaso" items={squares} />
              <span className="muted small">
                Tema: <Link to={"/tema/" + current.topic.slug}>{current.topic.title}</Link> · {BOX_LABEL[current.box] || BOX_LABEL[4]}
              </span>
            </div>
            <ExercisePanel
              key={current.exercise.id}
              exercise={current.exercise}
              solved={false}
              onSubmit={(body) => submit(current.exercise, body, "review")}
            />
            <div className="exercise-nav">
              <span className="muted small">
                {current.exercise.id in answered ? "Respondido. Sigue con el siguiente." : "Inténtalo sin mirar la teoría: el esfuerzo de recordar es el entrenamiento."}
              </span>
              <button
                className="btn primary"
                disabled={!(current.exercise.id in answered)}
                onClick={() => setIndex(items.findIndex((item, i) => i > index && !(item.exercise.id in answered)) === -1 ? index : items.findIndex((item, i) => i > index && !(item.exercise.id in answered)))}
              >
                Siguiente <ArrowRight size={16} aria-hidden="true" />
              </button>
            </div>
          </>
        )}
      </section>

      {data.pending_practice.length > 0 && (
        <section className="module">
          <div className="module-head">
            <h2>
              <BookOpen size={20} aria-hidden="true" /> Práctica pendiente
            </h2>
            <p className="muted small">Temas con la teoría leída y ejercicios sin resolver. Hacerlos un día después de leer ayuda a recordar.</p>
          </div>
          <ul className="ruled">
            {data.pending_practice.map((t) => (
              <li key={t.slug}>
                <Link to={"/tema/" + t.slug + "?tab=practica"}>{t.title}</Link>
                <span className="muted small num">
                  {t.solved}/{t.total} ejercicios
                </span>
              </li>
            ))}
          </ul>
        </section>
      )}
    </div>
  );
}
