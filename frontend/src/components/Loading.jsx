// Indicador de carga: un pequeño gráfico de líneas que se dibuja solo sobre papel cuadriculado,
// y un punto resaltado que aparece al final del trazo.
// `inline` lo hace pequeño para usarlo dentro de una línea de texto (ejecutar código, cargar tablas...).
export default function Loading({ text = "Cargando…", inline = false }) {
  const Tag = inline ? "span" : "div";
  return (
    <Tag className={inline ? "loader inline" : "loading"} role="status" aria-live="polite">
      <span className="loader-chart" aria-hidden="true">
        <svg viewBox="0 0 64 40">
          <polyline points="4,34 15,25 25,29 37,15 47,19 59,7" pathLength="100" />
          <circle cx="59" cy="7" r="3.5" />
        </svg>
      </span>
      <span>{text}</span>
    </Tag>
  );
}
