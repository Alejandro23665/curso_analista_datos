export const LEVELS = {
  fuerte: { label: "Fortaleza", color: "var(--green)" },
  regular: { label: "Regular", color: "var(--yellow)" },
  debil: { label: "A reforzar", color: "var(--red)" },
  en_progreso: { label: "En progreso", color: "var(--cyan)" },
  sin_datos: { label: "Sin practicar", color: "var(--muted)" },
};

export const KINDS = {
  python: { icon: "🐍", label: "Python" },
  sql: { icon: "🗄️", label: "SQL" },
  quiz: { icon: "❓", label: "Quiz" },
  checklist: { icon: "✅", label: "Lista" },
};

export const STATUS = {
  completado: { label: "Completado", icon: "✓" },
  en_curso: { label: "En curso", icon: "◐" },
  pendiente: { label: "Pendiente", icon: "○" },
};

export function percent(value) {
  return value === null || value === undefined ? "—" : Math.round(value * 100) + "%";
}

export function formatDate(iso) {
  if (!iso) return "—";
  const [year, month, day] = iso.split("-").map(Number);
  return new Date(year, month - 1, day).toLocaleDateString("es", { day: "numeric", month: "long", year: "numeric" });
}
