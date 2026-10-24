export default function ResultTable({ columns = [], rows = [], truncated = false }) {
  if (!columns.length) return null;
  return (
    <div className="result">
      <div className="table-wrap result-scroll">
        <table>
          <thead>
            <tr>
              {columns.map((column, index) => (
                <th key={index}>{column}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.map((row, rowIndex) => (
              <tr key={rowIndex}>
                {row.map((value, columnIndex) => (
                  <td key={columnIndex}>{value === null ? <span className="null">NULL</span> : String(value)}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <p className="muted small">
        {rows.length} fila{rows.length === 1 ? "" : "s"}
        {truncated ? " (se muestran solo las primeras)" : ""}
      </p>
    </div>
  );
}
