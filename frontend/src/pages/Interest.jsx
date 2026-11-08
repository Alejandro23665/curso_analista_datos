import { Link, useParams } from "react-router-dom";
import { ArrowLeft, ArrowRight, Cpu } from "lucide-react";
import { api } from "../api.js";
import Markdown from "../components/Markdown.jsx";
import Squares, { exerciseSquares, SquaresLegend } from "../components/Squares.jsx";
import { useAsync } from "../hooks.js";
import { STATUS } from "../util.js";

// Un área de interés: sus bloques y temas, con el mismo cuaderno de cuadritos que la ruta.
export default function Interest() {
  const { slug } = useParams();
  const { data, loading, error, reload } = useAsync(() => api.interest(slug), [slug]);

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

  const nextSlug = data.next_topic && data.next_topic.slug;

  return (
    <div className="page">
      <Link to="/intereses" className="link-arrow back">
        <ArrowLeft size={14} aria-hidden="true" /> Temas de interés
      </Link>

      <header className="page-head">
        <h1>{data.title}</h1>
        <p className="muted">{data.description}</p>
        <div className="row between">
          <p className="muted small num">
            {data.topics_total} temas · {data.total_hours} horas · {data.percent}% completado
          </p>
          <SquaresLegend />
        </div>
        {data.next_topic && (
          <div className="actions">
            <Link className="btn primary" to={"/tema/" + data.next_topic.slug + "?area=" + data.slug}>
              {data.next_topic.percent > 0 ? "Continuar con " : "Empezar con "} {data.next_topic.title} <ArrowRight size={16} aria-hidden="true" />
            </Link>
          </div>
        )}
      </header>

      {data.notice && (
        <aside className="notice">
          <Cpu size={18} aria-hidden="true" />
          <div className="markdown-inline">
            <Markdown>{data.notice}</Markdown>
          </div>
        </aside>
      )}

      {data.blocks.map((block) => (
        <section key={block.slug} className="section-block">
          <div className="section-head">
            <div>
              <h2>{block.title}</h2>
              {block.description && <p className="muted">{block.description}</p>}
            </div>
            <span className="figure">
              {block.percent}
              <small>%</small>
            </span>
          </div>
          <ul className="topic-rows">
            {block.topics.map((topic) => {
              const isNext = topic.slug === nextSlug;
              const square = isNext ? "next" : STATUS[topic.status].square;
              return (
                <li key={topic.slug}>
                  <Link to={"/tema/" + topic.slug + "?area=" + data.slug} className={"topic-row" + (isNext ? " next" : "")}>
                    <span className={"sq " + square} aria-label={isNext ? "Siguiente" : STATUS[topic.status].label} />
                    <span className="title">
                      {topic.title}
                      <small className="num">
                        {topic.hours} h{isNext && " · siguiente"}
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
