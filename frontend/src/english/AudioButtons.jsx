import { useState } from "react";
import { Turtle, Volume2 } from "lucide-react";
import { canSpeak, speak } from "./speech.js";

// Botones para escuchar un texto en inglés a velocidad normal o lenta.
export default function AudioButtons({ text, label = "Escuchar", compact = false }) {
  const [playing, setPlaying] = useState(false);
  if (!canSpeak()) return <span className="muted small">Tu navegador no puede leer en voz alta.</span>;

  async function play(slow) {
    setPlaying(true);
    try {
      await speak(text, { slow });
    } finally {
      setPlaying(false);
    }
  }

  return (
    <span className="audio-buttons">
      <button
        type="button"
        className={"btn small" + (compact ? " ghost icon" : "")}
        onClick={() => play(false)}
        aria-label={label}
        title={label}
      >
        <Volume2 size={16} aria-hidden="true" />
        {!compact && label}
      </button>
      <button type="button" className={"btn small ghost" + (compact ? " icon" : "")} onClick={() => play(true)} aria-label="Escuchar despacio" title="Más despacio">
        <Turtle size={16} aria-hidden="true" />
        {!compact && "Despacio"}
      </button>
      {playing && !compact && (
        <span className="muted small" aria-live="polite">
          Reproduciendo…
        </span>
      )}
    </span>
  );
}
