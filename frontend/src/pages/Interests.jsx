import { Link } from "react-router-dom";
import { ArrowRight } from "lucide-react";
import { api } from "../api.js";
import { useAsync } from "../hooks.js";

// Temas de interés: áreas para estudiar en el tiempo libre. No forman parte de la ruta ni del panel principal.
export default function Interests() {
  const { data, loading, error, reload } = useAsync(() => api.interests(), []);

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

  return (
    <div className="page">
      <header className="page-head">
        <h1>
          Temas de <span className="hl">interés</span>
        </h1>
        <p className="muted">
          Para tus ratos libres, a tu ritmo. No cuentan en tu ruta ni en el avance del panel, pero sí suman XP, racha y repasos. Los ejercicios
          funcionan igual que en la ruta.
        </p>
      </header>

      {data.areas.length === 0 ? (
        <div className="empty">
          <p className="muted">Todavía no hay temas de interés.</p>
        </div>
      ) : (
        <div className="interest-grid">
          {data.areas.map((area) => (
            <Link key={area.slug} to={"/intereses/" + area.slug} className="interest-card">
              <div className="row between">
                <h2>{area.title}</h2>
                <strong className="num">{area.percent}%</strong>
              </div>
              <p className="muted">{area.description}</p>
              <div className="meter">
                <span style={{ width: area.percent + "%" }} />
              </div>
              <div className="row between">
                <span className="muted small num">
                  {area.topics_completed}/{area.topics_total} temas · {area.blocks} bloques · {area.total_hours} h
                </span>
                <span className="link-arrow">
                  {area.percent > 0 ? "Continuar" : "Empezar"} <ArrowRight size={14} aria-hidden="true" />
                </span>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  );
}
