// Sonidos cortos (sin archivos de audio) para el temporizador y las celebraciones, y notificaciones del sistema.

let context = null;

// Notas (Hz) y separación entre ellas (s) de cada sonido.
const SOUNDS = {
  warn: [[660], 0.18],
  start: [[523, 784], 0.18],
  end: [[784, 659, 523], 0.18],
  win: [[784, 1047], 0.09],                       // acierto: dos notas rápidas hacia arriba
  lucky: [[784, 988, 1175, 1568], 0.08],          // golpe de suerte: arpegio brillante
  big: [[523, 659, 784, 1047], 0.13],             // celebración grande
};

export function beep(kind = "end") {
  try {
    context = context || new (window.AudioContext || window.webkitAudioContext)();
    const [notes, gap] = SOUNDS[kind] || SOUNDS.end;
    notes.forEach((frequency, i) => {
      const oscillator = context.createOscillator();
      const gain = context.createGain();
      const at = context.currentTime + i * gap;
      oscillator.type = "sine";
      oscillator.frequency.value = frequency;
      gain.gain.setValueAtTime(0.0001, at);
      gain.gain.exponentialRampToValueAtTime(0.25, at + 0.02);
      gain.gain.exponentialRampToValueAtTime(0.0001, at + 0.16);
      oscillator.connect(gain).connect(context.destination);
      oscillator.start(at);
      oscillator.stop(at + 0.18);
    });
  } catch (_) {
    /* el navegador no permite audio todavía */
  }
}

export function askNotifications() {
  try {
    if ("Notification" in window && Notification.permission === "default") Notification.requestPermission();
  } catch (_) {
    /* sin notificaciones */
  }
}

export function notify(title, body) {
  try {
    if ("Notification" in window && Notification.permission === "granted" && document.hidden) {
      new Notification(title, { body, tag: "datapath-timer" });
    }
  } catch (_) {
    /* sin notificaciones */
  }
}
