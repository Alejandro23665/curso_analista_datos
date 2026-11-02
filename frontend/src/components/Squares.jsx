import { Link } from "react-router-dom";
import { STATUS } from "../util.js";

// Los cuadritos del cuaderno: cada uno es un tema (o un ejercicio). done = relleno a bolígrafo,
// doing = medio relleno, next = resaltado, todo = vacío.
export default function Squares({ items, size = "", label }) {
  return (
    <span className={"squares " + size} role="list" aria-label={label}>
      {items.map((item) =>
        item.to ? (
          <Link key={item.key} role="listitem" to={item.to} className={"sq " + item.state} title={item.title} aria-label={item.title} />
        ) : (
          <span key={item.key} role="listitem" className={"sq " + item.state} title={item.title} aria-label={item.title} />
        )
      )}
    </span>
  );
}

// Cuadrito de un tema a partir de su estado; el siguiente pendiente se resalta.
export function topicSquare(topic, nextSlug, base = "/tema/") {
  const state = topic.slug === nextSlug ? "next" : STATUS[topic.status].square;
  return { key: topic.slug, state, title: topic.title + " · " + topic.percent + "%", to: base + topic.slug };
}

// Un cuadrito por ejercicio: los resueltos van rellenos.
export function exerciseSquares(solved, total) {
  return Array.from({ length: total }, (_, i) => ({
    key: i,
    state: i < solved ? "done" : "todo",
    title: i < solved ? "Ejercicio resuelto" : "Ejercicio pendiente",
  }));
}

export function SquaresLegend() {
  return (
    <span className="legend" aria-hidden="true">
      <span>
        <i className="sq done" /> Completado
      </span>
      <span>
        <i className="sq doing" /> En curso
      </span>
      <span>
        <i className="sq next" /> Siguiente
      </span>
      <span>
        <i className="sq" /> Pendiente
      </span>
    </span>
  );
}
