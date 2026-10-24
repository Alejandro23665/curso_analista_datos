import { useState } from "react";
import { api } from "../api.js";

export default function Login({ onSuccess }) {
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  async function submit(event) {
    event.preventDefault();
    setBusy(true);
    setError("");
    try {
      await api.login(password);
      onSuccess();
    } catch (err) {
      setError(err.message || "No se pudo iniciar sesión");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="login-wrap">
      <form className="card login" onSubmit={submit}>
        <div className="brand login-brand">
          <span className="brand-mark" aria-hidden="true">
            <i /> <i /> <i />
          </span>
          DataPath
        </div>
        <p className="muted">Introduce tu contraseña para continuar.</p>
        <label htmlFor="password" className="small muted">
          Contraseña
        </label>
        <input
          id="password"
          type="password"
          autoComplete="current-password"
          value={password}
          onChange={(event) => setPassword(event.target.value)}
          autoFocus
        />
        {error && <p className="login-error">{error}</p>}
        <button className="btn primary" type="submit" disabled={busy || !password}>
          {busy ? "Entrando…" : "Entrar"}
        </button>
      </form>
    </div>
  );
}
