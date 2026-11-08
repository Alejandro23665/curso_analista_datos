// Indicador de carga: cuatro cuadritos de cuaderno que se rellenan en círculo.
// `inline` lo hace pequeño para usarlo dentro de una línea de texto (ejecutar código, cargar tablas...).
export default function Loading({ text = "Cargando…", inline = false }) {
  const Tag = inline ? "span" : "div";
  return (
    <Tag className={inline ? "loader inline" : "loading"} role="status" aria-live="polite">
      <span className="loader-cells" aria-hidden="true">
        <i />
        <i />
        <i />
        <i />
      </span>
      <span>{text}</span>
    </Tag>
  );
}
