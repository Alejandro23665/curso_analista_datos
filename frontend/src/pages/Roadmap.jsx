import { Link } from "react-router-dom";
import { api } from "../api.js";
import { useAsync } from "../hooks.js";
import { STATUS } from "../util.js";

export default function Roadmap() {
  const { data, loading, error, reload } = useAsync(() => api.progress(), []);

  if (loading && !data) return <div className="page muted">Cargando…</div>;
  if (error)
    return (
      <div className="page">
        <div className="card center">
          <p className="muted">{error.message}</p>
          <button className="btn primary" onClick={reload}>
            Reintentar
          </button>
        </div>
      </div>
    );

  const perWeek = data.hours_per_day * 7;
  let cumulative = 0;

  return (
    <div className="page">
      <header className="page-head">
        <h1>Ruta de aprendizaje</h1>
        <p className="muted">
          {data.topics_total} temas · {data.total_hours} horas en total · unas {Math.ceil(data.total_hours / perWeek)} semanas
          estudiando {data.hours_per_day} h al día.
        </p>
      </header>

      {data.phases.map((phase) => (
        <section key={phase.slug} className="card phase">
          <div className="row between">
            <div>
              <h2>{phase.title}</h2>
              <p className="muted">{phase.description}</p>
            </div>
            <strong className="phase-percent">{phase.percent}%</strong>
          </div>
          <div className="bar">
            <span style={{ width: phase.percent + "%" }} />
          </div>
          <ul className="topic-list">
            {phase.topics.map((topic) => {
              cumulative += topic.hours;
              const status = STATUS[topic.status];
              return (
                <li key={topic.slug}>
                  <Link to={"/tema/" + topic.slug} className={"topic-row " + topic.status}>
                    <span className="status-icon" title={status.label}>
                      {status.icon}
                    </span>
                    <span className="topic-title">
                      {topic.title}
                      <small className="muted">
                        {" "}
                        · {topic.hours} h · semana ≈ {Math.ceil(cumulative / perWeek)}
                      </small>
                    </span>
                    <span className="topic-meta muted small">
                      {topic.solved}/{topic.total} ejercicios
                    </span>
                    <span className="mini-bar">
                      <span style={{ width: topic.percent + "%" }} />
                    </span>
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
