import { createContext, useCallback, useContext, useEffect, useRef, useState } from "react";
import { Link } from "react-router-dom";
import {
  Award, BookCheck, Brain, BrainCircuit, CalendarCheck, CalendarRange, Clover, Crown, Flame, Footprints, Gem, Hourglass, Library,
  Map, Medal, Rocket, ShieldCheck, Sparkles, Star, Swords, Target, Timer, TrendingUp, Trophy, Zap,
} from "lucide-react";
import { api } from "../api.js";
import { beep } from "./alerts.js";

// Motivación: XP, nivel, racha y logros. Celebra cada avance: sonido y +XP al acertar, golpes de suerte (XP doble),
// aciertos seguidos, racha, y una celebración a pantalla completa al completar un tema, subir de nivel o cumplir la meta.
// Los datos salen siempre del servidor (/api/game); aquí solo se celebran los cambios.

const SEEN_KEY = "datapath:achievements:seen";
const SOUND_KEY = "datapath:sonidos";
const COMBO_MILESTONES = [3, 5, 10, 20];
const STREAK_MILESTONES = [3, 7, 14, 30, 60, 100];

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

export function soundsOn() {
  try {
    return localStorage.getItem(SOUND_KEY) !== "0";
  } catch (_) {
    return true;
  }
}

export function setSounds(on) {
  try {
    localStorage.setItem(SOUND_KEY, on ? "1" : "0");
  } catch (_) {
    /* sin almacenamiento */
  }
}

function play(kind) {
  if (soundsOn()) beep(kind);
}

// Solo los iconos que usan los logros y los avisos (importar toda la librería engordaría la página).
const ICONS = {
  Award, BookCheck, Brain, BrainCircuit, CalendarCheck, CalendarRange, Clover, Crown, Flame, Footprints, Gem, Hourglass, Library,
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
  const [big, setBig] = useState(null);
  const combo = useRef(0);
  const previous = useRef(null);
  const queue = useRef([]);

  const push = useCallback((toast) => {
    const id = Math.random().toString(36).slice(2);
    setToasts((list) => [...list.slice(-3), { id, ...toast }]);
    setTimeout(() => setToasts((list) => list.filter((t) => t.id !== id)), toast.long ? 6000 : 3500);
  }, []);

  // Celebraciones grandes: de una en una (si llegan varias, se encolan).
  const showNext = useCallback(() => {
    const next = queue.current.shift();
    setBig(next || null);
    if (next) play("big");
  }, []);

  const celebrate = useCallback(
    (item) => {
      queue.current.push(item);
      setBig((current) => {
        if (current) return current;
        const next = queue.current.shift();
        if (next) play("big");
        return next;
      });
    },
    []
  );

  useEffect(() => {
    if (!big) return undefined;
    const id = setTimeout(showNext, 4200);
    return () => clearTimeout(id);
  }, [big, showNext]);

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
    if (before) {
      if (data.level.level > before.level.level) {
        celebrate({ icon: "TrendingUp", title: "¡Nivel " + data.level.level + "!", text: "Ahora eres " + data.level.title + "." });
      }
      if (before.today_xp < data.daily_goal && data.today_xp >= data.daily_goal) {
        celebrate({ icon: "Target", title: "¡Meta de hoy cumplida!", text: data.today_xp + " XP hoy. Lo que sumes ahora es extra." });
      }
      if (data.streak.current > before.streak.current) {
        const n = data.streak.current;
        if (STREAK_MILESTONES.includes(n)) {
          celebrate({ icon: "Flame", title: n + " días seguidos", text: "Tu racha está encendida. No la sueltes." });
        } else {
          push({ kind: "combo", title: "Racha: " + n + (n === 1 ? " día" : " días"), text: "Hoy ya cuenta.", icon: "Flame" });
        }
      }
    }
    previous.current = data;
    setGame(data);
    return data;
  }, [push, celebrate]);

  useEffect(() => {
    refresh();
  }, [refresh]);

  // Se llama tras responder cualquier ejercicio con la respuesta del servidor.
  // extra.topicCompleted: el tema acaba de completarse con esta respuesta.
  const afterSubmit = useCallback(
    (result, extra = {}) => {
      if (!result) return;
      if (result.correct) {
        combo.current += 1;
        play(result.lucky ? "lucky" : "win");
        if (result.lucky) {
          push({ kind: "lucky", title: "¡Golpe de suerte! +" + result.xp_gained + " XP", text: "XP doble en este ejercicio.", icon: "Clover", long: true });
        } else if (result.xp_gained > 0) {
          push({ kind: "xp", title: "+" + result.xp_gained + " XP", text: "", icon: "Zap" });
        }
        if (COMBO_MILESTONES.includes(combo.current)) {
          push({ kind: "combo", title: combo.current + " aciertos seguidos", text: "Estás en racha.", icon: "Flame" });
        }
      } else {
        combo.current = 0;
        if (result.xp_gained > 0) push({ kind: "xp", title: "+" + result.xp_gained + " XP", text: "Por intentarlo en el repaso.", icon: "Zap" });
      }
      if (extra.topicCompleted) {
        celebrate({ icon: "BookCheck", title: "¡Tema completado!", text: extra.topicTitle || "Teoría y ejercicios, todo hecho." });
      }
      refresh();
    },
    [push, refresh, celebrate]
  );

  return (
    <GameContext.Provider value={{ game, refresh, afterSubmit, push, celebrate }}>
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
            {(t.kind === "achievement" || t.kind === "lucky") && <span className="burst" aria-hidden="true">{Array.from({ length: 8 }, (_, i) => <i key={i} />)}</span>}
          </div>
        ))}
      </div>
      {big && (
        <div className="celebration" role="status" aria-live="polite" onClick={showNext}>
          <div className="confetti" aria-hidden="true">
            {Array.from({ length: 36 }, (_, i) => (
              <i key={i} style={{ "--x": ((i * 53) % 100) + "vw", "--d": (i % 9) * 0.12 + "s", "--r": (i * 47) % 360 + "deg" }} />
            ))}
          </div>
          <div className="celebration-card">
            <span className="celebration-icon">
              <AchievementIcon name={big.icon} size={40} />
            </span>
            <h2>{big.title}</h2>
            <p>{big.text}</p>
            <span className="muted small">Toca para continuar</span>
          </div>
        </div>
      )}
    </GameContext.Provider>
  );
}

export function useGame() {
  return useContext(GameContext);
}

// Resumen compacto en la barra lateral: nivel, XP del día frente a la meta y racha. Late al ganar XP.
export function GameBadge() {
  const { game } = useGame();
  const [bump, setBump] = useState(false);
  const lastXp = useRef(null);

  useEffect(() => {
    if (!game) return undefined;
    const grew = lastXp.current !== null && game.level.xp > lastXp.current;
    lastXp.current = game.level.xp;
    if (!grew) return undefined;
    setBump(true);
    const id = setTimeout(() => setBump(false), 700);
    return () => clearTimeout(id);
  }, [game]);

  if (!game) return null;
  const goal = Math.min(1, game.today_xp / game.daily_goal);
  const circumference = 2 * Math.PI * 15;
  return (
    <Link
      to="/progreso"
      className={"game-badge" + (bump ? " bump" : "") + (goal >= 1 ? " goal-done" : "")}
      aria-label={"Nivel " + game.level.level + ", " + game.today_xp + " de " + game.daily_goal + " XP hoy, racha de " + game.streak.current + " días"}
    >
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
