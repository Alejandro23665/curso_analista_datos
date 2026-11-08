import { Database } from "lucide-react";
import { api } from "../api.js";
import { useAsync } from "../hooks.js";
import Loading from "./Loading.jsx";

// Muestra las tablas de práctica para consultarlas mientras escribes SQL.
export default function SchemaPanel() {
  const { data, loading, error } = useAsync(() => api.schema(), []);
  return (
    <aside className="schema">
      <h2>
        <Database size={16} aria-hidden="true" /> Tablas de práctica
      </h2>
      {loading && <p className="muted small"><Loading inline text="Cargando tablas…" /></p>}
      {error && <p className="muted small">No se pudieron cargar las tablas: {error.message}</p>}
      {data &&
        data.tables.map((table) => (
          <details key={table.name} open={table.name === "orders"}>
            <summary>{table.name}</summary>
            <ul>
              {table.columns.map((column) => (
                <li key={column.name}>
                  <code>{column.name}</code> <span className="muted">{column.type}</span>
                </li>
              ))}
            </ul>
          </details>
        ))}
    </aside>
  );
}
