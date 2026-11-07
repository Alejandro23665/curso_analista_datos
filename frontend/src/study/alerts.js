// Avisos del temporizador: un sonido corto (sin archivos de audio) y notificaciones del sistema.

let context = null;

export function beep(kind = "end") {
  try {
    context = context || new (window.AudioContext || window.webkitAudioContext)();
    const notes = kind === "warn" ? [660] : kind === "start" ? [523, 784] : [784, 659, 523];
    notes.forEach((frequency, i) => {
      const oscillator = context.createOscillator();
      const gain = context.createGain();
      const at = context.currentTime + i * 0.18;
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
