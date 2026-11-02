import { Link } from "react-router-dom";
import { Link2 } from "lucide-react";
import { api } from "../api.js";
import Squares, { exerciseSquares, SquaresLegend } from "../components/Squares.jsx";
import { useAsync } from "../hooks.js";
import { useTrack } from "../track.jsx";
import { STATUS } from "../util.js";

export default function Roadmap() {
  const { track, setTrack } = useTrack();
  const { data, loading, error, reload } = useAsync(() => api.progress(track), [track]);

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

  const perWeek = data.hours_per_day * 7;
  const titles = Object.fromEntries(data.tracks.map((t) => [t.slug, t]));
  const nextSlug = data.next_topic && data.next_topic.slug;
  let cumulative = 0;

  return (
    <div className="page">
      {data.tracks.length > 1 && (
        <nav className="track-tabs" aria-label="Rutas">
          {data.tracks.map((t) => (
            <button key={t.slug} type="button" className={t.slug === data.track.slug ? "active" : ""} onClick={() => setTrack(t.slug)}>
              {t.title} <small>{t.percent}%</small>
            </button>
          ))}
        </nav>
      )}

      <header className="page-head">
        <h1>{data.track.title}</h1>
        <p className="muted">{data.track.description}</p>
        <div className="row between">
          <p className="muted small num">
            {data.topics_total} temas · {data.total_hours} horas · unas {Math.ceil(data.total_hours / perWeek)} semanas a {data.hours_per_day} h al
            día
          </p>
          <SquaresLegend />
        </div>
      </header>

      {data.phases.map((phase) => (
        <section key={phase.slug} className="section-block">
          <div className="section-head">
            <div>
              <h2>{phase.title}</h2>
              {phase.description && <p className="muted">{phase.description}</p>}
            </div>
            <span className="figure">
              {phase.percent}
              <small>%</small>
            </span>
          </div>
          <ul className="topic-rows">
            {phase.topics.map((topic) => {
              cumulative += topic.hours;
              const isNext = topic.slug === nextSlug;
              const square = isNext ? "next" : STATUS[topic.status].square;
              const shared = topic.shared_with.map((slug) => (titles[slug] ? titles[slug].title : slug)).join(", ");
              return (
                <li key={topic.slug}>
                  <Link to={"/tema/" + topic.slug} className={"topic-row" + (isNext ? " next" : "")}>
                    <span className={"sq " + square} aria-label={isNext ? "Siguiente" : STATUS[topic.status].label} />
                    <span className="title">
                      {topic.title}
                      {shared && <Link2 size={13} className="muted" style={{ marginLeft: 6, verticalAlign: -1 }} aria-label={"También en: " + shared} />}
                      <small className="num">
                        {topic.hours} h · semana {Math.ceil(cumulative / perWeek)}
                        {isNext && " · siguiente"}
                      </small>
                    </span>
                    <Squares size="small" label={topic.solved + " de " + topic.total + " ejercicios"} items={exerciseSquares(topic.solved, topic.total)} />
                    <span className={"pct" + (topic.percent ? "" : " zero")}>{topic.percent}%</span>
                  </Link>
                </li>
              );
            })}
          </ul>
        </section>
      ))}
    </div>
  );
}
