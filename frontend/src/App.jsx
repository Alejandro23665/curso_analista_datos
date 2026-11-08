import { useEffect, useState } from "react";
import { Link, NavLink, Route, Routes, useLocation } from "react-router-dom";
import { ArrowRight, Compass, Languages, LayoutGrid, LogOut, PanelLeftClose, PanelLeftOpen, RotateCcw, Route as RouteIcon, Target, Trophy } from "lucide-react";
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
import Interest from "./pages/Interest.jsx";
import Interests from "./pages/Interests.jsx";
import Progress from "./pages/Progress.jsx";
import Review from "./pages/Review.jsx";
import Topic from "./pages/Topic.jsx";
import { GameBadge, GameProvider, useGame } from "./study/game.jsx";
import { TimerProvider, TimerWidget } from "./study/timer.jsx";
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
  { to: "/repaso", label: "Repaso", Icon: RotateCcw },
  { to: "/ruta", label: "Ruta", Icon: RouteIcon },
  { to: "/intereses", label: "Intereses", Icon: Compass },
  { to: "/ingles", label: "Inglés", Icon: Languages },
  { to: "/habilidades", label: "Habilidades", Icon: Target },
  { to: "/progreso", label: "Progreso", Icon: Trophy },
];

// El temporizador avisa a la motivación cuando un bloque termina con su descanso (para actualizar la XP).
function StudyProviders({ children }) {
  const { refresh } = useGame();
  return <TimerProvider onBlockDone={refresh}>{children}</TimerProvider>;
}

const RAIL_KEY = "datapath:rail-hidden";

export default function App() {
  // required: el servidor pide contraseña; ok: hay una sesión válida
  const [auth, setAuth] = useState({ checked: false, required: false, ok: true });
  // Menú lateral oculto (preferencia guardada en este navegador); el contador sigue visible en una barra flotante.
  const [railHidden, setRailHidden] = useState(() => {
    try {
      return localStorage.getItem(RAIL_KEY) === "1";
    } catch (_) {
      return false;
    }
  });
  const toggleRail = () =>
    setRailHidden((hidden) => {
      try {
        localStorage.setItem(RAIL_KEY, hidden ? "0" : "1");
      } catch (_) {
        /* sin almacenamiento */
      }
      return !hidden;
    });

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
    <GameProvider>
    <StudyProviders>
    <div className={"app" + (railHidden ? " rail-hidden" : "")}>
      {railHidden ? (
        <div className="float-bar">
          <button className="float-menu" onClick={toggleRail} aria-label="Mostrar el menú lateral" title="Mostrar el menú">
            <PanelLeftOpen size={18} aria-hidden="true" />
          </button>
          <TimerWidget />
        </div>
      ) : (
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
          <GameBadge />
          <TimerWidget />
          <NextNote />
          <button className="rail-logout" onClick={toggleRail}>
            <PanelLeftClose size={16} aria-hidden="true" />
            <span>Ocultar menú</span>
          </button>
          {auth.required && (
            <button className="rail-logout" onClick={logout}>
              <LogOut size={16} aria-hidden="true" />
              <span>Salir</span>
            </button>
          )}
        </div>
      </aside>
      )}
      <main className="main">
        <NextNote strip />
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/ruta" element={<Roadmap />} />
          <Route path="/habilidades" element={<Skills />} />
          <Route path="/tema/:slug" element={<Topic />} />
          <Route path="/repaso" element={<Review />} />
          <Route path="/progreso" element={<Progress />} />
          <Route path="/intereses" element={<Interests />} />
          <Route path="/intereses/:slug" element={<Interest />} />
          <Route path="/ingles" element={<English />} />
          <Route path="/ingles/prueba" element={<EnglishPlacement />} />
          <Route path="/ingles/unidad/:slug" element={<EnglishUnit />} />
          <Route path="/ingles/vocabulario" element={<EnglishVocab />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </main>
    </div>
    </StudyProviders>
    </GameProvider>
  );
}
