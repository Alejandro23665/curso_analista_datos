import { createContext, useCallback, useContext, useEffect, useRef, useState } from "react";
import { Link } from "react-router-dom";
import {
  Award, BookCheck, Brain, BrainCircuit, CalendarCheck, CalendarRange, Crown, Flame, Footprints, Gem, Hourglass, Library,
  Map, Medal, Rocket, ShieldCheck, Sparkles, Star, Swords, Target, Timer, TrendingUp, Trophy, Zap,
} from "lucide-react";
import { api } from "../api.js";

// Motivación: XP, nivel, racha y logros. Muestra avisos al ganar XP, encadenar aciertos, subir de nivel o
// desbloquear un logro. Los datos salen siempre del servidor (/api/game); aquí solo se celebran los cambios.

const SEEN_KEY = "datapath:achievements:seen";
const COMBO_MILESTONES = [3, 5, 10, 20];

function readSeen() {
  try {
    const value = JSON.parse(localStorage.getItem(SEEN_KEY));
    return Array.isArray(value) ? new Set(value) : null;
  } catch (_) {
    return null;
  }
}

function writeSeen(set) {
  try {
    localStorage.setItem(SEEN_KEY, JSON.stringify([...set]));
  } catch (_) {
    /* sin almacenamiento */
  }
}

// Solo los iconos que usan los logros y los avisos (importar toda la librería engordaría la página).
const ICONS = {
  Award, BookCheck, Brain, BrainCircuit, CalendarCheck, CalendarRange, Crown, Flame, Footprints, Gem, Hourglass, Library,
  Map, Medal, Rocket, ShieldCheck, Sparkles, Star, Swords, Target, Timer, TrendingUp, Trophy, Zap,
};

export function AchievementIcon({ name, size = 18 }) {
  const Icon = ICONS[name] || Award;
  return <Icon size={size} aria-hidden="true" />;
}

const GameContext = createContext(null);

export function GameProvider({ children }) {
  const [game, setGame] = useState(null);
  const [toasts, setToasts] = useState([]);
  const combo = useRef(0);
  const previous = useRef(null);

  const push = useCallback((toast) => {
    const id = Math.random().toString(36).slice(2);
    setToasts((list) => [...list.slice(-3), { id, ...toast }]);
    setTimeout(() => setToasts((list) => list.filter((t) => t.id !== id)), toast.long ? 6000 : 3500);
  }, []);

  const refresh = useCallback(async () => {
    let data;
    try {
      data = await api.game();
    } catch (_) {
      return null;
    }
    const before = previous.current;
    const unlocked = data.achievements.filter((a) => a.unlocked).map((a) => a.key);
    let seen = readSeen();
    if (!seen) {
      seen = new Set(unlocked); // primera vez: no celebrar lo que ya estaba conseguido
      writeSeen(seen);
    }
    const fresh = data.achievements.filter((a) => a.unlocked && !seen.has(a.key));
    fresh.forEach((a) => push({ kind: "achievement", title: "Logro desbloqueado: " + a.title, text: a.description, icon: a.icon, long: true }));
    if (fresh.length) writeSeen(new Set([...seen, ...fresh.map((a) => a.key)]));
    if (before && data.level.level > before.level.level) {
      push({ kind: "level", title: "Nivel " + data.level.level + ": " + data.level.title, text: "Sigue así.", icon: "TrendingUp", long: true });
    }
    if (before && before.today_xp < data.daily_goal && data.today_xp >= data.daily_goal) {
      push({ kind: "goal", title: "Meta diaria cumplida", text: data.today_xp + " XP hoy.", icon: "Target", long: true });
    }
    previous.current = data;
    setGame(data);
    return data;
  }, [push]);

  useEffect(() => {
    refresh();
  }, [refresh]);

  // Se llama tras responder cualquier ejercicio con la respuesta del servidor.
  const afterSubmit = useCallback(
    (result) => {
      if (!result) return;
      if (result.correct) {
        combo.current += 1;
        if (result.xp_gained > 0) push({ kind: "xp", title: "+" + result.xp_gained + " XP", text: "", icon: "Zap" });
        if (COMBO_MILESTONES.includes(combo.current)) {
          push({ kind: "combo", title: combo.current + " aciertos seguidos", text: "Estás en racha.", icon: "Flame" });
        }
      } else {
        combo.current = 0;
        if (result.xp_gained > 0) push({ kind: "xp", title: "+" + result.xp_gained + " XP", text: "Por intentarlo en el repaso.", icon: "Zap" });
      }
      refresh();
    },
    [push, refresh]
  );

  return (
    <GameContext.Provider value={{ game, refresh, afterSubmit, push }}>
      {children}
      <div className="toasts" aria-live="polite">
        {toasts.map((t) => (
          <div key={t.id} className={"toast toast-" + t.kind}>
            <span className="toast-icon">
              <AchievementIcon name={t.icon} />
            </span>
            <div>
              <strong>{t.title}</strong>
              {t.text && <span>{t.text}</span>}
            </div>
            {(t.kind === "achievement" || t.kind === "level") && <span className="burst" aria-hidden="true">{Array.from({ length: 8 }, (_, i) => <i key={i} />)}</span>}
          </div>
        ))}
      </div>
    </GameContext.Provider>
  );
}

export function useGame() {
  return useContext(GameContext);
}

// Resumen compacto en la barra lateral: nivel, XP del día frente a la meta y racha.
export function GameBadge() {
  const { game } = useGame();
  if (!game) return null;
  const goal = Math.min(1, game.today_xp / game.daily_goal);
  const circumference = 2 * Math.PI * 15;
  return (
    <Link to="/progreso" className="game-badge" aria-label={"Nivel " + game.level.level + ", " + game.today_xp + " de " + game.daily_goal + " XP hoy, racha de " + game.streak.current + " días"}>
      <svg viewBox="0 0 36 36" className="goal-ring" aria-hidden="true">
        <circle cx="18" cy="18" r="15" className="track" />
        <circle cx="18" cy="18" r="15" className="fill" strokeDasharray={circumference} strokeDashoffset={circumference * (1 - goal)} />
        <text x="18" y="22" textAnchor="middle">{game.level.level}</text>
      </svg>
      <span className="game-badge-text">
        <strong className="num">{game.today_xp}/{game.daily_goal} XP</strong>
        <span className="num">
          <Flame size={13} aria-hidden="true" /> {game.streak.current} {game.streak.current === 1 ? "día" : "días"}
        </span>
      </span>
    </Link>
  );
}
