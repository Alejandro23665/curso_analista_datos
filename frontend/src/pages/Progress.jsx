import { useState } from "react";
import { Flame, Lock, ShieldCheck, Target, Timer, Volume2, VolumeX } from "lucide-react";
import { useGame, AchievementIcon, setSounds, soundsOn } from "../study/game.jsx";
import { percent } from "../util.js";
import Loading from "../components/Loading.jsx";

// Tu progreso de estudio: nivel, racha con protectores, meta diaria, resumen semanal, calendario y logros.

const MONTHS = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"];

function heat(xp) {
  if (!xp) return 0;
  if (xp < 30) return 1;
  if (xp < 60) return 2;
  if (xp < 120) return 3;
  return 4;
}

function Delta({ now, before, unit = "" }) {
  if (before === null || before === undefined || now === null || now === undefined) return null;
  const diff = now - before;
  if (!diff) return <small className="muted">igual que la semana anterior</small>;
  return (
    <small className={diff > 0 ? "delta up" : "delta down"}>
      {diff > 0 ? "+" : ""}
      {unit === "%" ? Math.round(diff * 100) + " pp" : diff} frente a la semana anterior
    </small>
  );
}

function Calendar({ days }) {
  const weeks = [];
  for (let i = 0; i < days.length; i += 7) weeks.push(days.slice(i, i + 7));
  return (
    <div className="heatmap-wrap">
      <div className="heatmap" role="img" aria-label="Calendario de estudio de las últimas 26 semanas">
        {weeks.map((week, w) => {
          const first = new Date(week[0].date + "T00:00");
          const label = first.getDate() <= 7 ? MONTHS[first.getMonth()] : "";
          return (
            <div key={week[0].date} className="heat-week">
              <span className="heat-month">{label}</span>
              {week.map((d) => (
                <span
                  key={d.date}
                  className={"heat-cell h" + heat(d.xp) + (d.frozen ? " frozen" : "")}
                  title={d.date + ": " + d.xp + " XP" + (d.frozen ? " (protector usado)" : "")}
                />
              ))}
            </div>
          );
        })}
      </div>
      <span className="legend" aria-hidden="true">
        Menos
        {[0, 1, 2, 3, 4].map((h) => (
          <i key={h} className={"heat-cell h" + h} />
        ))}
        Más
        <i className="heat-cell frozen" /> Protector usado
      </span>
    </div>
  );
}

export default function Progress() {
  const { game } = useGame();
  if (!game) return <Loading text="Cargando tu progreso…" />;

  const { level, streak, weekly } = game;
  const unlocked = game.achievements.filter((a) => a.unlocked).length;
  const goalPct = Math.min(100, Math.round((game.today_xp / game.daily_goal) * 100));

  return (
    <div className="page">
      <header className="page-head">
        <h1>
          Nivel {level.level}: <span className="hl">{level.title}</span>
        </h1>
        <div className="level-bar">
          <div className="meter">
            <span style={{ width: Math.round((level.into_level / level.for_next) * 100) + "%" }} />
          </div>
          <span className="muted small num">
            {level.into_level} / {level.for_next} XP para el nivel {level.level + 1} · {level.xp} XP en total
          </span>
        </div>
      </header>

      <dl className="ledger">
        <div>
          <dt>
            <Flame size={15} aria-hidden="true" /> Racha
          </dt>
          <dd>
            {streak.current} {streak.current === 1 ? "día" : "días"}
            <small>{streak.today_done ? "Hoy ya cuenta" : "Estudia hoy para mantenerla"} · mejor: {streak.best}</small>
          </dd>
        </div>
        <div>
          <dt>
            <ShieldCheck size={15} aria-hidden="true" /> Protectores
          </dt>
          <dd>
            {streak.freezes} de 2<small>Ganas uno cada 7 días seguidos. Si un día no estudias, se gasta uno y la racha sigue.</small>
          </dd>
        </div>
        <div>
          <dt>
            <Target size={15} aria-hidden="true" /> Meta de hoy
          </dt>
          <dd>
            {game.today_xp} / {game.daily_goal} XP
            <small>
              <span className="meter mini">
                <span style={{ width: goalPct + "%" }} />
              </span>
            </small>
          </dd>
        </div>
        <div>
          <dt>
            <Timer size={15} aria-hidden="true" /> Bloques hoy
          </dt>
          <dd>
            {game.blocks_today}
            <small>con su descanso respetado</small>
          </dd>
        </div>
      </dl>

      <section className="module">
        <div className="module-head">
          <h2>Tu semana</h2>
          <p className="muted small">Últimos 7 días frente a los 7 anteriores.</p>
        </div>
        <dl className="ledger">
          <div>
            <dt>XP</dt>
            <dd>
              {weekly.this.xp}
              <Delta now={weekly.this.xp} before={weekly.previous.xp} />
            </dd>
          </div>
          <div>
            <dt>Ejercicios nuevos resueltos</dt>
            <dd>
              {weekly.this.solved}
              <Delta now={weekly.this.solved} before={weekly.previous.solved} />
            </dd>
          </div>
          <div>
            <dt>Precisión</dt>
            <dd>
              {percent(weekly.this.accuracy)}
              <Delta now={weekly.this.accuracy} before={weekly.previous.accuracy} unit="%" />
            </dd>
          </div>
          <div>
            <dt>Tiempo en bloques</dt>
            <dd>
              {Math.floor(weekly.this.minutes / 60)} h {weekly.this.minutes % 60} min
              <small>
                {weekly.this.blocks} {weekly.this.blocks === 1 ? "bloque" : "bloques"}
              </small>
            </dd>
          </div>
        </dl>
      </section>

      <section className="module">
        <h2>Calendario de estudio</h2>
        <Calendar days={game.calendar} />
      </section>

      <section className="module">
        <div className="module-head">
          <h2>Logros</h2>
          <span className="muted small num">
            {unlocked} de {game.achievements.length}
          </span>
        </div>
        <ul className="achievements">
          {game.achievements.map((a) => (
            <li key={a.key} className={a.unlocked ? "unlocked" : "locked"}>
              <span className="ach-icon">{a.unlocked ? <AchievementIcon name={a.icon} size={22} /> : <Lock size={18} aria-hidden="true" />}</span>
              <div>
                <strong>{a.title}</strong>
                <span className="small muted">{a.description}</span>
                {!a.unlocked && a.target > 1 && (
                  <span className="ach-progress num">
                    <span className="meter mini">
                      <span style={{ width: Math.round((a.value / a.target) * 100) + "%" }} />
                    </span>
                    {a.value}/{a.target}
                  </span>
                )}
              </div>
            </li>
          ))}
        </ul>
      </section>

      <section className="module">
        <h2>Cómo se gana XP</h2>
        <ul className="ruled xp-rules">
          <li>
            <span>Resolver un ejercicio por primera vez</span> <strong>10 XP (+5 si es a la primera)</strong>
          </li>
          <li>
            <span>Golpe de suerte: más o menos 1 de cada 6 ejercicios nuevos da el doble</span> <strong>XP × 2</strong>
          </li>
          <li>
            <span>Acertar un ejercicio del repaso del día</span> <strong>8 XP (2 si fallas)</strong>
          </li>
          <li>
            <span>Superar el desafío del día</span> <strong>25 XP</strong>
          </li>
          <li>
            <span>Completar un bloque de estudio respetando su descanso</span> <strong>20 XP</strong>
          </li>
          <li>
            <span>Marcar como leída la teoría de un tema o una lección de inglés</span> <strong>15 XP</strong>
          </li>
          <li>
            <span>Repasar una tarjeta de vocabulario de inglés</span> <strong>2 XP</strong>
          </li>
        </ul>
        <p className="muted small">
          La XP premia lo que de verdad te hace aprender: acertar a la primera, repasar y descansar.
        </p>
        <SoundToggle />
      </section>
    </div>
  );
}

function SoundToggle() {
  const [on, setOn] = useState(soundsOn);
  const Icon = on ? Volume2 : VolumeX;
  return (
    <label className="row small">
      <input
        type="checkbox"
        checked={on}
        onChange={(event) => {
          setSounds(event.target.checked);
          setOn(event.target.checked);
        }}
      />
      <Icon size={16} aria-hidden="true" /> Sonidos al acertar y en las celebraciones
    </label>
  );
}
