import { useEffect, useState } from "react";
import { Link, NavLink, Route, Routes, useLocation } from "react-router-dom";
import { ArrowRight, Languages, LayoutGrid, LogOut, Route as RouteIcon, Target } from "lucide-react";
import { api, UNAUTHORIZED_EVENT } from "./api.js";
import BrandMark from "./components/BrandMark.jsx";
import { useAsync } from "./hooks.js";
import Dashboard from "./pages/Dashboard.jsx";
import English from "./pages/English.jsx";
import EnglishPlacement from "./pages/EnglishPlacement.jsx";
import EnglishUnit from "./pages/EnglishUnit.jsx";
import EnglishVocab from "./pages/EnglishVocab.jsx";
import Login from "./pages/Login.jsx";
import Roadmap from "./pages/Roadmap.jsx";
import Skills from "./pages/Skills.jsx";
import Topic from "./pages/Topic.jsx";
import { useTrack } from "./track.jsx";

function NotFound() {
  return (
    <div className="page narrow">
      <div className="empty">
        <h2>Página no encontrada</h2>
        <Link className="btn primary" to="/">
          Volver al panel
        </Link>
      </div>
    </div>
  );
}

// El siguiente paso de la ruta, firmado en la barra lateral en todas las páginas.
function NextNote({ strip = false }) {
  const { pathname } = useLocation();
  const { track } = useTrack();
  const { data } = useAsync(() => api.progress(track), [track, pathname]);
  const next = data && data.next_topic;
  if (!next) return null;
  if (strip)
    return (
      <Link className="next-strip" to={"/tema/" + next.slug}>
        <span>Siguiente:</span>
        <strong>{next.title}</strong>
        <ArrowRight size={16} aria-hidden="true" />
      </Link>
    );
  return (
    <Link className="next-note" to={"/tema/" + next.slug}>
      <span className="label">
        Siguiente <ArrowRight size={14} aria-hidden="true" />
      </span>
      <strong>
        <span className="hl">{next.title}</span>
      </strong>
    </Link>
  );
}

const NAV = [
  { to: "/", label: "Panel", Icon: LayoutGrid, end: true },
  { to: "/ruta", label: "Ruta", Icon: RouteIcon },
  { to: "/habilidades", label: "Habilidades", Icon: Target },
  { to: "/ingles", label: "Inglés", Icon: Languages },
];

export default function App() {
  // required: el servidor pide contraseña; ok: hay una sesión válida
  const [auth, setAuth] = useState({ checked: false, required: false, ok: true });

  useEffect(() => {
    api
      .session()
      .then((s) => setAuth({ checked: true, required: s.auth_required, ok: s.authenticated }))
      .catch(() => setAuth({ checked: true, required: false, ok: true }));
    const onUnauthorized = () => setAuth((previous) => ({ ...previous, required: true, ok: false }));
    window.addEventListener(UNAUTHORIZED_EVENT, onUnauthorized);
    return () => window.removeEventListener(UNAUTHORIZED_EVENT, onUnauthorized);
  }, []);

  if (!auth.checked) return <div className="loading">Cargando…</div>;
  if (auth.required && !auth.ok) return <Login onSuccess={() => setAuth((previous) => ({ ...previous, ok: true }))} />;

  async function logout() {
    try {
      await api.logout();
    } finally {
      setAuth((previous) => ({ ...previous, ok: false }));
    }
  }

  return (
    <div className="app">
      <aside className="rail">
        <NavLink to="/" className="brand" aria-label="DataPath, ir al panel">
          <BrandMark />
          <span className="brand-name">DataPath</span>
        </NavLink>
        <nav className="nav" aria-label="Secciones">
          {NAV.map(({ to, label, Icon, end }) => (
            <NavLink key={to} to={to} end={end} aria-label={label}>
              <Icon size={18} aria-hidden="true" />
              <span>{label}</span>
            </NavLink>
          ))}
        </nav>
        <div className="rail-foot">
          <NextNote />
          {auth.required && (
            <button className="rail-logout" onClick={logout}>
              <LogOut size={16} aria-hidden="true" />
              <span>Salir</span>
            </button>
          )}
        </div>
      </aside>
      <main className="main">
        <NextNote strip />
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/ruta" element={<Roadmap />} />
          <Route path="/habilidades" element={<Skills />} />
          <Route path="/tema/:slug" element={<Topic />} />
          <Route path="/ingles" element={<English />} />
          <Route path="/ingles/prueba" element={<EnglishPlacement />} />
          <Route path="/ingles/unidad/:slug" element={<EnglishUnit />} />
          <Route path="/ingles/vocabulario" element={<EnglishVocab />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </main>
    </div>
  );
}
