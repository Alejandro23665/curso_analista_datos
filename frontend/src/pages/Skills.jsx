import { Link } from "react-router-dom";
import { Bar, BarChart, CartesianGrid, Cell, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { api } from "../api.js";
import { useAsync } from "../hooks.js";
import { LEVELS, percent } from "../util.js";

function Badge({ level }) {
  const meta = LEVELS[level];
  return (
    <span className="badge" style={{ color: meta.color, borderColor: meta.color }}>
      {meta.label}
    </span>
  );
}

function SkillCard({ skill }) {
  return (
    <li className="skill-card">
      <div className="row between">
        <strong>{skill.skill}</strong>
        <span style={{ color: LEVELS[skill.level].color }}>{percent(skill.accuracy)}</span>
      </div>
      <p className="muted small">
        {skill.correct} aciertos de {skill.attempts} intentos
      </p>
      <div className="row wrap">
        {skill.topics.map((topic) => (
          <Link key={topic.slug} className="chip link" to={"/tema/" + topic.slug + "?tab=practica"}>
            {topic.title}
          </Link>
        ))}
      </div>
    </li>
  );
}

function Group({ title, color, skills, empty }) {
  return (
    <section className="card">
      <h3 style={{ color }}>{title}</h3>
      {skills.length ? <ul className="skill-grid">{skills.map((s) => <SkillCard key={s.skill} skill={s} />)}</ul> : <p className="muted">{empty}</p>}
    </section>
  );
}

export default function Skills() {
  const { data, loading, error, reload } = useAsync(() => api.stats(), []);

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

  const practiced = data.skills.filter((s) => s.attempts > 0);
  const chart = practiced.map((s) => ({ nombre: s.skill, precision: Math.round(s.accuracy * 100), nivel: s.level }));
  const inProgress = data.skills.filter((s) => s.level === "en_progreso" || s.level === "regular");
  const untouched = data.skills.filter((s) => s.level === "sin_datos");

  return (
    <div className="page">
      <header className="page-head">
        <h1>Fortalezas y debilidades</h1>
        <p className="muted">
          Se calcula con tus intentos en los ejercicios, agrupados por habilidad. Una habilidad se clasifica a partir de 3 intentos:
          ≥ 75 % de aciertos es fortaleza y &lt; 50 % es a reforzar.
        </p>
      </header>

      {practiced.length === 0 ? (
        <div className="card center">
          <h3>Todavía no hay datos</h3>
          <p className="muted">Resuelve ejercicios de cualquier tema y vuelve aquí para ver tu diagnóstico.</p>
          <Link className="btn primary" to="/ruta">
            Ir a la ruta
          </Link>
        </div>
      ) : (
        <>
          <section className="card">
            <h3>Precisión por habilidad</h3>
            <div className="chart">
              <ResponsiveContainer width="100%" height={Math.max(180, chart.length * 34)}>
                <BarChart data={chart} layout="vertical" margin={{ left: 12, right: 24 }}>
                  <CartesianGrid stroke="var(--line)" horizontal={false} />
                  <XAxis type="number" domain={[0, 100]} unit="%" tick={{ fill: "var(--muted)", fontSize: 11 }} />
                  <YAxis type="category" dataKey="nombre" width={230} tick={{ fill: "var(--text)", fontSize: 12 }} />
                  <Tooltip
                    cursor={{ fill: "rgba(20,35,58,.06)" }}
                    contentStyle={{ background: "var(--panel)", border: "1px solid var(--line)", borderRadius: 8 }}
                    formatter={(value) => [value + "%", "Precisión"]}
                  />
                  <Bar dataKey="precision" radius={[0, 4, 4, 0]}>
                    {chart.map((row) => (
                      <Cell key={row.nombre} fill={LEVELS[row.nivel].color} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </section>

          <Group title="💪 Fortalezas" color={LEVELS.fuerte.color} skills={data.strengths} empty="Aún no hay habilidades con 3 o más intentos y ≥ 75 % de aciertos." />
          <Group title="🎯 A reforzar" color={LEVELS.debil.color} skills={data.weaknesses} empty="No tienes debilidades claras ahora mismo. ¡Bien!" />

          {data.review_topics.length > 0 && (
            <section className="card">
              <h3>📌 Plan de repaso sugerido</h3>
              <p className="muted">Empieza por estos temas, en este orden:</p>
              <ol className="review">
                {data.review_topics.map((topic) => (
                  <li key={topic.slug}>
                    <Link className="link" to={"/tema/" + topic.slug + "?tab=practica"}>
                      {topic.title}
                    </Link>
                  </li>
                ))}
              </ol>
            </section>
          )}

          <Group title="En progreso" color={LEVELS.en_progreso.color} skills={inProgress} empty="Nada en progreso." />
        </>
      )}

      <section className="card">
        <h3>Todas las habilidades</h3>
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Habilidad</th>
                <th>Intentos</th>
                <th>Aciertos</th>
                <th>Precisión</th>
                <th>Nivel</th>
              </tr>
            </thead>
            <tbody>
              {data.skills.map((s) => (
                <tr key={s.skill}>
                  <td>{s.skill}</td>
                  <td>{s.attempts}</td>
                  <td>{s.correct}</td>
                  <td>{percent(s.accuracy)}</td>
                  <td>
                    <Badge level={s.level} />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        {untouched.length > 0 && <p className="muted small">{untouched.length} habilidades aún sin practicar.</p>}
      </section>
    </div>
  );
}
