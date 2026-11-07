import { createContext, useCallback, useContext, useEffect, useRef, useState } from "react";
import { createPortal } from "react-dom";
import { Coffee, Pause, Play, Settings2, Square, Timer, X } from "lucide-react";
import { api } from "../api.js";
import { askNotifications, beep, notify } from "./alerts.js";

// Temporizador de estudio estilo pomodoro. Guarda la hora de inicio de cada fase (no un contador), así sigue
// funcionando aunque recargues o cierres la pestaña, y todas las pestañas de DataPath ven el mismo estado.
//
// Fases: idle → study (o paused) → break (la página se bloquea) → ready (descanso terminado) → study...

const KEY = "datapath:timer:v1";
const SKIP_PHRASE = "Elijo saltarme el descanso";
const HOLD_SECONDS = 10;

export const PRESETS = [
  { label: "Pomodoro 25/5", study: 25, short: 5, long: 15, every: 4 },
  { label: "Clásico 50/10", study: 50, short: 10, long: 20, every: 3 },
  { label: "Profundo 90/20", study: 90, short: 20, long: 30, every: 2 },
];

const DEFAULT = {
  config: { study: 50, short: 10, long: 20, every: 3, sound: true },
  phase: "idle",
  start: 0,
  duration: 0,
  remaining: 0,
  cycle: 0,
  breakKind: "short",
  blockMinutes: 0,
  warned: false,
  day: "",
  blocksToday: 0,
  skippedToday: 0,
};

const BREAK_TIPS = [
  "Levántate y camina un poco, aunque sea por la casa.",
  "Bebe un vaso de agua.",
  "Mira algo lejano por la ventana durante un minuto: tus ojos lo agradecen.",
  "Estira el cuello, los hombros y la espalda.",
  "Respira hondo: cuatro segundos dentro, cuatro fuera, cinco veces.",
  "No mires el móvil: el descanso también es para la cabeza.",
  "Repasa mentalmente, sin mirar, la idea más importante del último bloque.",
];

function todayKey() {
  return new Date().toLocaleDateString("en-CA");
}

function load() {
  try {
    const saved = JSON.parse(localStorage.getItem(KEY));
    if (saved && saved.config) return { ...DEFAULT, ...saved, config: { ...DEFAULT.config, ...saved.config } };
  } catch (_) {
    /* sin almacenamiento */
  }
  return DEFAULT;
}

function save(state) {
  try {
    localStorage.setItem(KEY, JSON.stringify(state));
  } catch (_) {
    /* sin almacenamiento */
  }
}

function secondsLeft(state, now) {
  if (state.phase === "paused") return state.remaining;
  if (state.phase !== "study" && state.phase !== "break") return 0;
  return Math.max(0, Math.ceil((state.start + state.duration * 1000 - now) / 1000));
}

export function formatClock(seconds) {
  const m = Math.floor(seconds / 60);
  const s = seconds % 60;
  return String(m).padStart(2, "0") + ":" + String(s).padStart(2, "0");
}

function sendEvent(kind, ref, minutes = 0) {
  api.studyEvent({ kind, ref: String(ref), minutes }).catch(() => {});
}

const TimerContext = createContext(null);

export function TimerProvider({ children, onBlockDone }) {
  const [state, setState] = useState(load);
  const [now, setNow] = useState(Date.now());
  const stateRef = useRef(state);
  stateRef.current = state;
  const onDone = useRef(onBlockDone);
  onDone.current = onBlockDone;

  // Escribe un estado nuevo solo si nadie (otra pestaña) cambió la fase mientras tanto.
  const commit = useCallback((expected, next) => {
    const stored = load();
    if (expected && (stored.phase !== expected.phase || stored.start !== expected.start)) {
      setState(stored);
      return false;
    }
    const day = todayKey();
    // Los contadores de "hoy" vuelven a cero al cambiar de día.
    const value = next.day === day ? next : { ...next, day, blocksToday: 0, skippedToday: 0 };
    save(value);
    setState(value);
    return true;
  }, []);

  // Otras pestañas: adoptan el estado guardado.
  useEffect(() => {
    const onStorage = (event) => {
      if (event.key === KEY) setState(load());
    };
    window.addEventListener("storage", onStorage);
    return () => window.removeEventListener("storage", onStorage);
  }, []);

  // Reloj: un tic por segundo y las transiciones de fase.
  useEffect(() => {
    const tick = () => {
      const current = stateRef.current;
      const time = Date.now();
      setNow(time);
      const left = secondsLeft(current, time);
      const sound = current.config.sound;

      if (current.phase === "study" && left > 0 && left <= 60 && !current.warned && current.duration > 60) {
        if (commit(current, { ...current, warned: true })) {
          if (sound) beep("warn");
          notify("Queda 1 minuto", "Termina la idea o el ejercicio que tienes a medias.");
        }
      } else if (current.phase === "study" && left === 0) {
        const cycle = current.cycle + 1;
        const breakKind = cycle % current.config.every === 0 ? "long" : "short";
        const end = current.start + current.duration * 1000;
        const next = {
          ...current, phase: "break", start: end, duration: current.config[breakKind] * 60, cycle, breakKind, warned: false,
          day: todayKey(), blocksToday: (current.day === todayKey() ? current.blocksToday : 0) + 1,
        };
        if (commit(current, next)) {
          sendEvent("pomodoro", current.start, current.blockMinutes);
          if (sound) beep("end");
          notify("Hora de descansar", "Bloque completado. La página se bloquea durante el descanso.");
        }
      } else if (current.phase === "break" && left === 0) {
        if (commit(current, { ...current, phase: "ready", duration: 0 })) {
          sendEvent("break_done", current.start, current.config[current.breakKind]);
          if (sound) beep("start");
          notify("Descanso terminado", "Cuando quieras, empieza el siguiente bloque.");
          onDone.current && onDone.current();
        }
      }
    };
    tick();
    const id = setInterval(tick, 1000);
    return () => clearInterval(id);
  }, [commit]);

  // Durante el descanso, el resto de la página no recibe foco ni teclado.
  useEffect(() => {
    const app = document.querySelector(".app");
    if (!app) return undefined;
    app.inert = state.phase === "break";
    return () => {
      app.inert = false;
    };
  }, [state.phase]);

  const actions = {
    start() {
      askNotifications();
      const current = load();
      if (current.config.sound) beep("start");
      commit(null, {
        ...current, phase: "study", start: Date.now(), duration: current.config.study * 60,
        blockMinutes: current.config.study, warned: false,
      });
    },
    pause() {
      const current = load();
      if (current.phase !== "study") return;
      commit(current, { ...current, phase: "paused", remaining: secondsLeft(current, Date.now()) });
    },
    resume() {
      const current = load();
      if (current.phase !== "paused") return;
      commit(current, { ...current, phase: "study", start: Date.now(), duration: current.remaining });
    },
    stop() {
      const current = load();
      if (current.phase === "break") return;
      commit(null, { ...current, phase: "idle", duration: 0, cycle: current.phase === "ready" ? current.cycle : 0 });
    },
    skipBreak() {
      const current = load();
      if (current.phase !== "break") return;
      if (commit(current, {
        ...current, phase: "ready", duration: 0, day: todayKey(),
        blocksToday: current.day === todayKey() ? current.blocksToday : 0,
        skippedToday: (current.day === todayKey() ? current.skippedToday : 0) + 1,
      })) {
        sendEvent("break_skipped", current.start, 0);
      }
    },
    setConfig(patch) {
      const current = load();
      commit(null, { ...current, config: { ...current.config, ...patch } });
    },
  };

  const value = { state, left: secondsLeft(state, now), actions };
  return (
    <TimerContext.Provider value={value}>
      {children}
      {state.phase === "break" && <BreakLock left={value.left} state={state} onSkip={actions.skipBreak} />}
    </TimerContext.Provider>
  );
}

export function useTimer() {
  return useContext(TimerContext);
}

// ---------------------------------------------------------------------------
// Pantalla de descanso (bloquea toda la página)
// ---------------------------------------------------------------------------

function BreakLock({ left, state, onSkip }) {
  const [skipping, setSkipping] = useState(false);
  const tip = BREAK_TIPS[Math.floor(state.start / 1000) % BREAK_TIPS.length];
  const total = state.duration || 1;
  return (
    <div className="break-lock" role="dialog" aria-modal="true" aria-labelledby="break-title">
      <div className="break-card">
        <Coffee size={36} aria-hidden="true" />
        <h2 id="break-title">{state.breakKind === "long" ? "Descanso largo" : "Descanso"}</h2>
        <p className="break-clock num" aria-live="off">
          {formatClock(left)}
        </p>
        <div className="meter break-meter" aria-hidden="true">
          <span style={{ width: Math.round(100 - (left / total) * 100) + "%" }} />
        </div>
        <p className="break-tip">{tip}</p>
        <p className="muted small">
          Lo que estudiaste se asienta mientras descansas. DataPath se desbloquea solo cuando termine el descanso.
        </p>
        {skipping ? <SkipForm onSkip={onSkip} onCancel={() => setSkipping(false)} /> : (
          <button className="btn ghost small break-skip" onClick={() => setSkipping(true)}>
            Necesito saltarme el descanso
          </button>
        )}
      </div>
    </div>
  );
}

// Salida de emergencia con fricción: mantener pulsado 10 s y escribir la frase.
function SkipForm({ onSkip, onCancel }) {
  const [held, setHeld] = useState(0);
  const [holding, setHolding] = useState(false);
  const [text, setText] = useState("");

  useEffect(() => {
    if (!holding || held >= HOLD_SECONDS) return undefined;
    const id = setTimeout(() => setHeld((value) => value + 1), 1000);
    return () => clearTimeout(id);
  }, [holding, held]);

  const phraseOk = text.trim().toLowerCase() === SKIP_PHRASE.toLowerCase();
  const holdOk = held >= HOLD_SECONDS;
  const release = () => {
    setHolding(false);
    if (held < HOLD_SECONDS) setHeld(0);
  };

  return (
    <div className="skip-form">
      <p className="small">
        Solo para urgencias. Quedará registrado en tus estadísticas y este bloque no sumará XP.
      </p>
      <button
        type="button"
        className={"btn hold" + (holdOk ? " done" : "")}
        onPointerDown={() => setHolding(true)}
        onPointerUp={release}
        onPointerLeave={release}
        onKeyDown={(event) => (event.key === " " || event.key === "Enter") && setHolding(true)}
        onKeyUp={release}
        disabled={holdOk}
      >
        <span className="hold-fill" style={{ width: (held / HOLD_SECONDS) * 100 + "%" }} aria-hidden="true" />
        <span className="hold-label">{holdOk ? "Listo" : "Mantén pulsado " + (HOLD_SECONDS - held) + " s"}</span>
      </button>
      <label className="small">
        Escribe: <strong>{SKIP_PHRASE}</strong>
        <input value={text} onChange={(event) => setText(event.target.value)} autoComplete="off" spellCheck="false" />
      </label>
      <div className="row">
        <button className="btn small" onClick={onCancel}>
          Mejor descanso
        </button>
        <button className="btn small danger" disabled={!phraseOk || !holdOk} onClick={onSkip}>
          Saltar el descanso
        </button>
      </div>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Control en la barra lateral
// ---------------------------------------------------------------------------

const PHASE_LABEL = { idle: "Temporizador", study: "Estudiando", paused: "En pausa", break: "Descanso", ready: "Descanso terminado" };

export function TimerWidget() {
  const { state, left, actions } = useTimer();
  const [open, setOpen] = useState(false);
  const running = state.phase === "study" || state.phase === "paused";

  return (
    <div className={"timer-widget phase-" + state.phase}>
      <button className="timer-main" onClick={() => setOpen(true)} aria-label="Abrir el temporizador de estudio">
        <Timer size={16} aria-hidden="true" />
        <span className="timer-phase">{PHASE_LABEL[state.phase]}</span>
        {running && <strong className="num">{formatClock(left)}</strong>}
      </button>
      {state.phase === "ready" && (
        <button className="btn small primary timer-next" onClick={actions.start}>
          <Play size={14} aria-hidden="true" /> Seguir
        </button>
      )}
      {open && createPortal(<TimerPanel onClose={() => setOpen(false)} />, document.body)}
    </div>
  );
}

function TimerPanel({ onClose }) {
  const { state, left, actions } = useTimer();
  const { config } = state;
  const [showSettings, setShowSettings] = useState(state.phase === "idle");
  const running = state.phase === "study" || state.phase === "paused";

  useEffect(() => {
    const onKey = (event) => event.key === "Escape" && onClose();
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [onClose]);

  const number = (key, label, min, max) => (
    <label className="timer-field">
      <span>{label}</span>
      <input
        type="number"
        min={min}
        max={max}
        value={config[key]}
        onChange={(event) => {
          const value = Math.round(Number(event.target.value));
          if (value >= min && value <= max) actions.setConfig({ [key]: value });
        }}
      />
    </label>
  );

  return (
    <div className="timer-backdrop" onClick={onClose}>
      <section className="timer-panel" role="dialog" aria-modal="true" aria-label="Temporizador de estudio" onClick={(e) => e.stopPropagation()}>
        <header className="row between">
          <h2>Temporizador de estudio</h2>
          <button className="btn ghost icon" onClick={onClose} aria-label="Cerrar">
            <X size={18} aria-hidden="true" />
          </button>
        </header>

        <p className="timer-big num">{running ? formatClock(left) : formatClock(config.study * 60)}</p>
        <p className="muted small">
          {state.phase === "idle" && "Bloques de " + config.study + " min con descansos de " + config.short + " min (uno largo de " + config.long + " min cada " + config.every + " bloques). En el descanso la página se bloquea."}
          {running && "Bloque " + (state.cycle + 1) + ". Un minuto antes del descanso te aviso para que termines lo que tengas a medias."}
          {state.phase === "ready" && "Descanso terminado. Empieza el siguiente bloque cuando quieras."}
        </p>

        <div className="actions">
          {(state.phase === "idle" || state.phase === "ready") && (
            <button className="btn primary" onClick={actions.start}>
              <Play size={16} aria-hidden="true" /> {state.phase === "ready" ? "Siguiente bloque" : "Empezar a estudiar"}
            </button>
          )}
          {state.phase === "study" && (
            <button className="btn" onClick={actions.pause}>
              <Pause size={16} aria-hidden="true" /> Pausar
            </button>
          )}
          {state.phase === "paused" && (
            <button className="btn primary" onClick={actions.resume}>
              <Play size={16} aria-hidden="true" /> Reanudar
            </button>
          )}
          {(running || state.phase === "ready") && (
            <button className="btn ghost" onClick={actions.stop}>
              <Square size={14} aria-hidden="true" /> Terminar sesión
            </button>
          )}
          <button className="btn ghost" onClick={() => setShowSettings((v) => !v)} aria-expanded={showSettings}>
            <Settings2 size={16} aria-hidden="true" /> Ajustes
          </button>
        </div>

        <p className="muted small num">
          Hoy: {state.day === todayKey() ? state.blocksToday : 0} bloques completados
          {state.day === todayKey() && state.skippedToday ? " · " + state.skippedToday + " descansos saltados" : ""}
        </p>

        {showSettings && (
          <div className="timer-settings">
            <div className="row">
              {PRESETS.map((p) => (
                <button key={p.label} className="tag" type="button" onClick={() => actions.setConfig({ study: p.study, short: p.short, long: p.long, every: p.every })}>
                  {p.label}
                </button>
              ))}
            </div>
            <div className="timer-fields">
              {number("study", "Estudio (min)", 1, 180)}
              {number("short", "Descanso corto (min)", 1, 60)}
              {number("long", "Descanso largo (min)", 1, 90)}
              {number("every", "Largo cada (bloques)", 1, 12)}
            </div>
            <label className="row small">
              <input type="checkbox" checked={config.sound} onChange={(event) => actions.setConfig({ sound: event.target.checked })} />
              Sonido al cambiar de fase
            </label>
            <p className="muted small">Los cambios se aplican desde el siguiente bloque.</p>
          </div>
        )}
      </section>
    </div>
  );
}
