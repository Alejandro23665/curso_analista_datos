const BASE = import.meta.env.VITE_API_URL || "";

// Se emite cuando el servidor responde 401: la app muestra la pantalla de acceso.
export const UNAUTHORIZED_EVENT = "datapath:unauthorized";

async function request(path, options = {}, { quiet401 = false } = {}) {
  const response = await fetch(BASE + "/api" + path, {
    headers: { "Content-Type": "application/json" },
    credentials: "include",
    ...options,
  });
  if (response.status === 401 && !quiet401) {
    window.dispatchEvent(new Event(UNAUTHORIZED_EVENT));
  }
  if (!response.ok) {
    let detail = response.statusText;
    try {
      const body = await response.json();
      detail = body.detail || detail;
    } catch (_) {
      /* respuesta sin JSON */
    }
    throw new Error(typeof detail === "string" ? detail : JSON.stringify(detail));
  }
  return response.json();
}

const send = (method, body) => ({ method, body: JSON.stringify(body) });

export const api = {
  session: () => request("/session"),
  login: (password) => request("/login", send("POST", { password }), { quiet401: true }),
  logout: () => request("/logout", send("POST", {})),
  progress: (track) => request("/progress" + (track ? "?track=" + encodeURIComponent(track) : "")),
  stats: () => request("/stats"),
  topic: (slug, track) => request("/topics/" + slug + (track ? "?track=" + encodeURIComponent(track) : "")),
  setTheory: (slug, done) => request("/topics/" + slug + "/theory", send("POST", { done })),
  saveNote: (slug, content) => request("/topics/" + slug + "/note", send("PUT", { content })),
  runSql: (query) => request("/sql/run", send("POST", { query })),
  schema: () => request("/sandbox/schema"),
  submit: (exerciseId, body) => request("/exercises/" + exerciseId + "/submit", send("POST", body)),
  studyEvent: (event) => request("/study/events", send("POST", event)),
  game: () => request("/game"),
  review: () => request("/review"),
  interests: () => request("/interests"),
  interest: (slug) => request("/interests/" + slug),
  english: {
    overview: () => request("/english/overview"),
    unit: (slug) => request("/english/units/" + slug),
    setLesson: (slug, done) => request("/english/units/" + slug + "/lesson", send("POST", { done })),
    submit: (exerciseId, body) => request("/english/exercises/" + exerciseId + "/submit", send("POST", body)),
    placement: () => request("/english/placement"),
    sendPlacement: (answers) => request("/english/placement", send("POST", { answers })),
    vocab: () => request("/english/vocab"),
    grade: (cardId, grade) => request("/english/vocab/" + cardId, send("POST", { grade })),
  },
};
