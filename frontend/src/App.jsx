import { useEffect, useState } from "react";
import { Link, NavLink, Route, Routes } from "react-router-dom";
import { api, UNAUTHORIZED_EVENT } from "./api.js";
import Dashboard from "./pages/Dashboard.jsx";
import Login from "./pages/Login.jsx";
import Roadmap from "./pages/Roadmap.jsx";
import Skills from "./pages/Skills.jsx";
import Topic from "./pages/Topic.jsx";

function NotFound() {
  return (
    <div className="page">
      <div className="card center">
        <h2>Página no encontrada</h2>
        <Link className="btn primary" to="/">
          Volver al inicio
        </Link>
      </div>
    </div>
  );
}

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

  if (!auth.checked) return <div className="page muted">Cargando…</div>;
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
      <header className="topbar">
        <NavLink to="/" className="brand">
          <span className="brand-mark" aria-hidden="true">
            <i /> <i /> <i />
          </span>
          DataPath
        </NavLink>
        <nav>
          <NavLink to="/" end>
            Inicio
          </NavLink>
          <NavLink to="/ruta">Ruta de aprendizaje</NavLink>
          <NavLink to="/habilidades">Fortalezas y debilidades</NavLink>
        </nav>
        {auth.required && (
          <button className="btn ghost small push" onClick={logout}>
            Salir
          </button>
        )}
      </header>
      <main>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/ruta" element={<Roadmap />} />
          <Route path="/habilidades" element={<Skills />} />
          <Route path="/tema/:slug" element={<Topic />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </main>
    </div>
  );
}
