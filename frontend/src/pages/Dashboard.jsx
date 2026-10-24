import { Link } from "react-router-dom";
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { api } from "../api.js";
import ProgressRing from "../components/ProgressRing.jsx";
import { useAsync } from "../hooks.js";
import { formatDate, LEVELS, percent } from "../util.js";

function Stat({ icon, value, label }) {
  return (
    <div className="card stat">
      <span className="stat-icon">{icon}</span>
      <strong>{value}</strong>
      <span className="muted">{label}</span>
    </div>
  );
}

export default function Dashboard() {
  const progress = useAsync(() => api.progress(), []);
  const stats = useAsync(() => api.stats(), []);

  if (progress.loading && !progress.data) return <div className="page muted">Cargando tu progreso…</div>;
  if (progress.error)
    return (
      <div className="page">
        <div className="card center">
          <h2>No se pudo conectar con el servidor</h2>
          <p className="muted">{progress.error.message}</p>
          <p className="muted small">Comprueba que el backend (FastAPI) y PostgreSQL estén en marcha.</p>
          <button className="btn primary" onClick={progress.reload}>
            Reintentar
          </button>
        </div>
      </div>
    );

  const p = progress.data;
  const s = stats.data;
  const next = p.next_topic;

  return (
    <div className="page">
      <section className="hero card">
        <div className="hero-text">
          <p className="eyebrow">Tu ruta a ingeniero de datos</p>
          {next ? (
            <>
              <h1>Sigue donde lo dejaste</h1>
              <p className="muted">
                {next.phase} · <strong>{next.title}</strong>
              </p>
              <p>{next.summary}</p>
              <div className="row">
                <Link className="btn primary" to={"/tema/" + next.slug}>
                  {next.percent > 0 ? "Continuar" : "Empezar"} →
                </Link>
                <Link className="btn ghost" to="/ruta">
                  Ver toda la ruta
                </Link>
              </div>
            </>
          ) : (
            <>
              <h1>¡Completaste toda la ruta! 🎉</h1>
              <p>Ahora toca lo más importante: publicar tus proyectos y empezar a postular.</p>
            </>
          )}
        </div>
        <ProgressRing value={p.overall_percent} label="de la ruta" />
      </section>

      <section className="stat-grid">
        <Stat icon="🔥" value={p.streak + (p.streak === 1 ? " día" : " días")} label="racha de estudio" />
        <Stat icon="📚" value={p.topics_completed + " / " + p.topics_total} label="temas completados" />
        <Stat
          icon="🧩"
          value={s ? s.totals.exercises_solved + " / " + s.totals.exercises_total : "—"}
          label="ejercicios resueltos"
        />
        <Stat icon="🎯" value={s ? percent(s.totals.accuracy) : "—"} label="precisión en intentos" />
        <Stat
          icon="🗓️"
          value={p.remaining_hours + " h"}
          label={p.days_left ? "restantes · fin ≈ " + formatDate(p.eta_date) : "restantes"}
        />
      </section>
      <p className="muted small note">
        Estimación basada en {p.hours_per_day} h de estudio al día, todos los días.
      </p>

      <div className="grid-2">
        <section className="card">
          <h3>Progreso por fase</h3>
          <ul className="phase-list">
            {p.phases.map((phase) => (
              <li key={phase.slug}>
                <div className="row between">
                  <span>{phase.title}</span>
                  <strong>{phase.percent}%</strong>
                </div>
                <div className="bar">
                  <span style={{ width: phase.percent + "%" }} />
                </div>
              </li>
            ))}
          </ul>
        </section>

        <section className="card">
          <h3>Actividad (últimos 28 días)</h3>
          {s ? (
            <div className="chart">
              <ResponsiveContainer width="100%" height={210}>
                <BarChart data={s.activity.map((d) => ({ dia: d.date.slice(5), acciones: d.count }))}>
                  <CartesianGrid stroke="var(--line)" vertical={false} />
                  <XAxis dataKey="dia" tick={{ fill: "var(--muted)", fontSize: 11 }} interval={3} />
                  <YAxis allowDecimals={false} tick={{ fill: "var(--muted)", fontSize: 11 }} width={28} />
                  <Tooltip
                    cursor={{ fill: "rgba(20,35,58,.06)" }}
                    contentStyle={{ background: "var(--panel)", border: "1px solid var(--line)", borderRadius: 8 }}
                  />
                  <Bar dataKey="acciones" fill="var(--green)" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          ) : (
            <p className="muted">Cargando…</p>
          )}
        </section>
      </div>

      {s && (
        <section className="card">
          <div className="row between">
            <h3>Tus fortalezas y debilidades</h3>
            <Link to="/habilidades" className="link">
              Ver detalle →
            </Link>
          </div>
          {s.totals.attempts === 0 ? (
            <p className="muted">
              Aún no hay datos. Resuelve unos cuantos ejercicios y aquí aparecerá qué se te da mejor y qué debes reforzar.
            </p>
          ) : (
            <div className="grid-2">
              <div>
                <h4 style={{ color: LEVELS.fuerte.color }}>💪 Fortalezas</h4>
                {s.strengths.length ? (
                  <ul className="mini-list">
                    {s.strengths.slice(0, 4).map((k) => (
                      <li key={k.skill}>
                        <span>{k.skill}</span> <strong>{percent(k.accuracy)}</strong>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className="muted small">Todavía ninguna (necesitas al menos 3 intentos por habilidad).</p>
                )}
              </div>
              <div>
                <h4 style={{ color: LEVELS.debil.color }}>🎯 A reforzar</h4>
                {s.weaknesses.length ? (
                  <ul className="mini-list">
                    {s.weaknesses.slice(0, 4).map((k) => (
                      <li key={k.skill}>
                        <span>{k.skill}</span> <strong>{percent(k.accuracy)}</strong>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className="muted small">¡Nada urgente por ahora!</p>
                )}
              </div>
            </div>
          )}
        </section>
      )}
    </div>
  );
}
