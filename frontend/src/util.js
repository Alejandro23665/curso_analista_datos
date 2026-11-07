import { CircleHelp, Code, Database, ListChecks, ListOrdered, SquareTerminal } from "lucide-react";

export const LEVELS = {
  fuerte: { label: "Fortaleza", color: "var(--ok)" },
  regular: { label: "Regular", color: "var(--warn)" },
  debil: { label: "A reforzar", color: "var(--bad)" },
  en_progreso: { label: "En progreso", color: "var(--blue)" },
  sin_datos: { label: "Sin practicar", color: "var(--muted-cell)" },
};

export const KINDS = {
  python: { Icon: Code, label: "Python" },
  sql: { Icon: Database, label: "SQL" },
  quiz: { Icon: CircleHelp, label: "Quiz" },
  checklist: { Icon: ListChecks, label: "Lista" },
  parsons: { Icon: ListOrdered, label: "Ordenar" },
  predict: { Icon: SquareTerminal, label: "¿Qué imprime?" },
};

export const STATUS = {
  completado: { label: "Completado", square: "done" },
  en_curso: { label: "En curso", square: "doing" },
  pendiente: { label: "Pendiente", square: "todo" },
};

export function percent(value) {
  return value === null || value === undefined ? "—" : Math.round(value * 100) + "%";
}

export function formatDate(iso) {
  if (!iso) return "—";
  const [year, month, day] = iso.split("-").map(Number);
  return new Date(year, month - 1, day).toLocaleDateString("es", { day: "numeric", month: "long", year: "numeric" });
}
