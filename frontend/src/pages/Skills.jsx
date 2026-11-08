import { Link } from "react-router-dom";
import { Bar, BarChart, CartesianGrid, Cell, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { ArrowRight, TrendingDown, TrendingUp } from "lucide-react";
import { api } from "../api.js";
import { useAsync } from "../hooks.js";
import { LEVELS, percent } from "../util.js";
import Loading from "../components/Loading.jsx";

function LevelLabel({ level }) {
  const meta = LEVELS[level];
  return (
    <span className="small">
      <span className="level-dot" style={{ background: meta.color }} aria-hidden="true" />
      {meta.label}
    </span>
  );
}

function SkillList({ skills, empty }) {
  if (!skills.length) return <p className="muted">{empty}</p>;
  return (
    <ul className="skill-entries">
      {skills.map((skill) => (
        <li key={skill.skill}>
          <div>
            <strong>{skill.skill}</strong>
            <p className="muted small num">
              {skill.correct} aciertos de {skill.attempts} intentos
            </p>
          </div>
          <span className="acc" style={{ color: LEVELS[skill.level].color }}>
            {percent(skill.accuracy)}
          </span>
          <div className="tags">
            {skill.topics.map((topic) => (
              <Link key={topic.slug} className="tag" to={"/tema/" + topic.slug + "?tab=practica"}>
                {topic.title}
              </Link>
            ))}
          </div>
        </li>
      ))}
    </ul>
  );
}

export default function Skills() {
  const { data, loading, error, reload } = useAsync(() => api.stats(), []);

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

  const practiced = data.skills.filter((s) => s.attempts > 0);
  const chart = practiced.map((s) => ({ nombre: s.skill, precision: Math.round(s.accuracy * 100), nivel: s.level }));
  const inProgress = data.skills.filter((s) => s.level === "en_progreso" || s.level === "regular");
  const untouched = data.skills.filter((s) => s.level === "sin_datos");

  return (
    <div className="page">
      <header className="page-head">
        <h1>Fortalezas y debilidades</h1>
        <p className="muted">
          Se calcula con tus intentos en los ejercicios, agrupados por habilidad. Una habilidad se clasifica a partir de 3 intentos: 75 % de
          aciertos o más es fortaleza, menos de 50 % es a reforzar.
        </p>
      </header>

      {practiced.length === 0 ? (
        <div className="empty">
          <h2>Todavía no hay datos</h2>
          <p className="muted">Resuelve ejercicios de cualquier tema y vuelve aquí para ver tu diagnóstico.</p>
          <Link className="btn primary" to="/ruta">
            Ir a la ruta <ArrowRight size={16} aria-hidden="true" />
          </Link>
        </div>
      ) : (
        <>
          <section className="module">
            <h2>Precisión por habilidad</h2>
            <div className="chart">
              <ResponsiveContainer width="100%" height={Math.max(180, chart.length * 34)}>
                <BarChart data={chart} layout="vertical" margin={{ left: 8, right: 24 }}>
                  <CartesianGrid stroke="var(--grid)" horizontal={false} />
                  <XAxis type="number" domain={[0, 100]} unit="%" tick={{ fill: "var(--ink-soft)", fontSize: 11 }} tickLine={false} axisLine={{ stroke: "var(--rule)" }} />
                  <YAxis type="category" dataKey="nombre" width={230} tick={{ fill: "var(--ink)", fontSize: 12 }} tickLine={false} axisLine={false} />
                  <Tooltip
                    cursor={{ fill: "rgba(29, 63, 176, .06)" }}
                    contentStyle={{ background: "#fff", border: "1px solid var(--rule)", borderRadius: 6, fontSize: 13 }}
                    formatter={(value) => [value + "%", "Precisión"]}
                  />
                  <Bar dataKey="precision" radius={[0, 2, 2, 0]} maxBarSize={18}>
                    {chart.map((row) => (
                      <Cell key={row.nombre} fill={LEVELS[row.nivel].color} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </section>

          <div className="cols">
            <section className="module">
              <h2 className="row">
                <TrendingUp size={20} color="var(--ok)" aria-hidden="true" /> Fortalezas
              </h2>
              <SkillList skills={data.strengths} empty="Aún no hay habilidades con 3 o más intentos y 75 % de aciertos." />
            </section>
            <section className="module">
              <h2 className="row">
                <TrendingDown size={20} color="var(--bad)" aria-hidden="true" /> A reforzar
              </h2>
              <SkillList skills={data.weaknesses} empty="No tienes debilidades claras ahora mismo." />
            </section>
          </div>

          {data.review_topics.length > 0 && (
            <section className="module">
              <h2>Plan de repaso sugerido</h2>
              <p className="muted">Empieza por estos temas, en este orden:</p>
              <ol className="review-list">
                {data.review_topics.map((topic) => (
                  <li key={topic.slug}>
                    <Link to={"/tema/" + topic.slug + "?tab=practica"}>{topic.title}</Link>
                  </li>
                ))}
              </ol>
            </section>
          )}

          <section className="module">
            <h2>En progreso</h2>
            <SkillList skills={inProgress} empty="Nada en progreso." />
          </section>
        </>
      )}

      <section className="module">
        <div className="module-head">
          <h2>Todas las habilidades</h2>
          {untouched.length > 0 && <p className="muted small">{untouched.length} aún sin practicar.</p>}
        </div>
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
                    <LevelLabel level={s.level} />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}
