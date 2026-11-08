import { Link } from "react-router-dom";
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { ArrowRight, TrendingDown, TrendingUp } from "lucide-react";
import { api } from "../api.js";
import Squares, { SquaresLegend, topicSquare } from "../components/Squares.jsx";
import { useAsync } from "../hooks.js";
import { useTrack } from "../track.jsx";
import { formatDate, percent } from "../util.js";
import Loading from "../components/Loading.jsx";

function Tracks({ tracks, current, onSelect }) {
  return (
    <section className="module">
      <div className="module-head">
        <h2>Tus rutas</h2>
        <p className="muted small">Los temas compartidos cuentan en todas las rutas que los incluyen.</p>
      </div>
      <div className="track-list">
        {tracks.map((t) => (
          <article key={t.slug} className={"track-item" + (t.slug === current ? " current" : "")}>
            <div className="row between">
              <h3>{t.title}</h3>
              <strong className="num">{t.percent}%</strong>
            </div>
            <p className="muted small">{t.description}</p>
            <div className="meter">
              <span style={{ width: t.percent + "%" }} />
            </div>
            <div className="row between">
              <span className="muted small num">
                {t.topics_completed}/{t.topics_total} temas · {t.total_hours} h
              </span>
              {t.slug === current ? (
                <span className="tag ok">Ruta actual</span>
              ) : (
                <button className="btn small" onClick={() => onSelect(t.slug)}>
                  Seguir esta ruta
                </button>
              )}
            </div>
          </article>
        ))}
      </div>
    </section>
  );
}

export default function Dashboard() {
  const { track, setTrack } = useTrack();
  const progress = useAsync(() => api.progress(track), [track]);
  const stats = useAsync(() => api.stats(), []);

  if (progress.loading && !progress.data) return <Loading text="Cargando tu progreso…" />;
  if (progress.error)
    return (
      <div className="page narrow">
        <div className="empty">
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
  const nextSlug = next && next.slug;

  return (
    <div className="page">
      <section className="next-block">
        {next ? (
          <div>
            <h1>
              Sigue con <span className="hl">{next.title}</span>
            </h1>
            <p className="lede">{next.summary}</p>
            <p className="meta">
              <span>{next.phase}</span>
              <span className="num">
                {next.solved}/{next.total} ejercicios
              </span>
              <span className="num">{next.percent}% hecho</span>
            </p>
          </div>
        ) : (
          <div>
            <h1>
              Completaste <span className="hl green">toda la ruta</span>
            </h1>
            <p className="lede">Ahora toca lo más importante: publicar tus proyectos y empezar a postular.</p>
          </div>
        )}
        {next && (
          <div className="actions">
            <Link className="btn primary" to={"/tema/" + next.slug}>
              {next.percent > 0 ? "Continuar" : "Empezar"} <ArrowRight size={16} aria-hidden="true" />
            </Link>
            <Link className="btn" to="/ruta">
              Ver toda la ruta
            </Link>
          </div>
        )}
      </section>

      <section className="module">
        <div className="module-head">
          <h2>{p.track.title}, cuadro a cuadro</h2>
          <SquaresLegend />
        </div>
        <div className="route-sheet">
          <div className="route-summary">
            <div className="figure-wrap">
              <span className="figure">
                {p.overall_percent}
                <small>%</small>
              </span>
              <span>de la ruta</span>
            </div>
            <div className="figure-wrap">
              <span className="figure">
                {p.topics_completed}
                <small>/{p.topics_total}</small>
              </span>
              <span>temas completados</span>
            </div>
            <div className="figure-wrap">
              <span className="figure">
                {p.remaining_hours}
                <small>h</small>
              </span>
              <span>{p.days_left ? "restantes · fin ≈ " + formatDate(p.eta_date) : "restantes"}</span>
            </div>
          </div>
          <div className="route-lines">
            {p.phases.map((phase) => (
              <div key={phase.slug} className="route-line">
                <Squares label={phase.title} items={phase.topics.map((t) => topicSquare(t, nextSlug))} />
                <span className="name" title={phase.title}>
                  {phase.title}
                </span>
                <span className="pct">{phase.percent}%</span>
              </div>
            ))}
          </div>
        </div>
        <p className="muted small">Estimación con {p.hours_per_day} h de estudio al día, todos los días. Cada cuadro es un tema: tócalo para abrirlo.</p>
      </section>

      <dl className="ledger">
        <div>
          <dt>Racha de estudio</dt>
          <dd>
            {p.streak} {p.streak === 1 ? "día" : "días"}
          </dd>
        </div>
        <div>
          <dt>Ejercicios resueltos</dt>
          <dd>{s ? s.totals.exercises_solved + " / " + s.totals.exercises_total : "—"}</dd>
        </div>
        <div>
          <dt>Precisión en intentos</dt>
          <dd>
            {s ? percent(s.totals.accuracy) : "—"}
            {s && <small>{s.totals.attempts} intentos</small>}
          </dd>
        </div>
      </dl>

      {p.tracks.length > 1 && <Tracks tracks={p.tracks} current={p.track.slug} onSelect={setTrack} />}

      <div className="cols">
        <section className="module">
          <h2>Actividad, últimos 28 días</h2>
          {s ? (
            <div className="chart">
              <ResponsiveContainer width="100%" height={220}>
                <BarChart data={s.activity.map((d) => ({ dia: d.date.slice(5), acciones: d.count }))} margin={{ left: -8, right: 4 }}>
                  <CartesianGrid stroke="var(--grid)" vertical={false} />
                  <XAxis dataKey="dia" tick={{ fill: "var(--ink-soft)", fontSize: 11 }} interval={3} tickLine={false} axisLine={{ stroke: "var(--rule)" }} />
                  <YAxis allowDecimals={false} tick={{ fill: "var(--ink-soft)", fontSize: 11 }} width={32} tickLine={false} axisLine={false} />
                  <Tooltip
                    cursor={{ fill: "rgba(29, 63, 176, .06)" }}
                    contentStyle={{ background: "#fff", border: "1px solid var(--rule)", borderRadius: 6, fontSize: 13 }}
                    formatter={(value) => [value, "acciones"]}
                  />
                  <Bar dataKey="acciones" fill="var(--blue)" radius={[2, 2, 0, 0]} maxBarSize={18} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          ) : (
            <p className="muted"><Loading inline /></p>
          )}
        </section>

        <section className="module">
          <div className="module-head">
            <h2>Fortalezas y debilidades</h2>
            <Link to="/habilidades" className="link-arrow">
              Ver detalle <ArrowRight size={14} aria-hidden="true" />
            </Link>
          </div>
          {!s ? (
            <p className="muted"><Loading inline /></p>
          ) : s.totals.attempts === 0 ? (
            <p className="muted">
              Aún no hay datos. Resuelve unos cuantos ejercicios y aquí aparecerá qué se te da mejor y qué debes reforzar.
            </p>
          ) : (
            <div className="skill-lists">
              <div>
                <h3>
                  <TrendingUp size={18} color="var(--ok)" aria-hidden="true" /> Fortalezas
                </h3>
                {s.strengths.length ? (
                  <ul className="ruled">
                    {s.strengths.slice(0, 4).map((k) => (
                      <li key={k.skill}>
                        <span>{k.skill}</span> <strong>{percent(k.accuracy)}</strong>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className="muted small">Todavía ninguna: hacen falta al menos 3 intentos por habilidad.</p>
                )}
              </div>
              <div>
                <h3>
                  <TrendingDown size={18} color="var(--bad)" aria-hidden="true" /> A reforzar
                </h3>
                {s.weaknesses.length ? (
                  <ul className="ruled">
                    {s.weaknesses.slice(0, 4).map((k) => (
                      <li key={k.skill}>
                        <span>{k.skill}</span> <strong>{percent(k.accuracy)}</strong>
                      </li>
                    ))}
                  </ul>
                ) : (
                  <p className="muted small">Nada urgente por ahora.</p>
                )}
              </div>
            </div>
          )}
        </section>
      </div>
    </div>
  );
}
