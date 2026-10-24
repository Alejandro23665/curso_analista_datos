import { api } from "../api.js";
import { useAsync } from "../hooks.js";

// Muestra las tablas de práctica para consultarlas mientras escribes SQL.
export default function SchemaPanel() {
  const { data, loading, error } = useAsync(() => api.schema(), []);
  return (
    <aside className="card schema">
      <h4>🗄️ Tablas de práctica</h4>
      {loading && <p className="muted small">Cargando tablas…</p>}
      {error && <p className="muted small">No se pudieron cargar las tablas: {error.message}</p>}
      {data &&
        data.tables.map((table) => (
          <details key={table.name} open={table.name === "orders"}>
            <summary>{table.name}</summary>
            <ul>
              {table.columns.map((column) => (
                <li key={column.name}>
                  <code>{column.name}</code> <span className="muted small">{column.type}</span>
                </li>
              ))}
            </ul>
          </details>
        ))}
    </aside>
  );
}
