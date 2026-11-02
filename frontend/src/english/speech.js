// Voz del navegador para la vista de inglés: leer en voz alta (speechSynthesis) y reconocer lo que dices (SpeechRecognition).
// Todo ocurre en el navegador: no hace falta ninguna clave ni servicio externo.

const VOICE_KEY = "datapath:en-voice";
const RATE_KEY = "datapath:en-rate";

export const canSpeak = () => typeof window !== "undefined" && "speechSynthesis" in window;
const Recognition = typeof window !== "undefined" ? window.SpeechRecognition || window.webkitSpeechRecognition : null;
export const canListen = () => Boolean(Recognition);

let voices = [];
function loadVoices() {
  voices = window.speechSynthesis.getVoices();
}
if (canSpeak()) {
  loadVoices();
  window.speechSynthesis.addEventListener("voiceschanged", loadVoices);
}

function read(key, fallback) {
  try {
    return localStorage.getItem(key) ?? fallback;
  } catch (_) {
    return fallback;
  }
}

function write(key, value) {
  try {
    localStorage.setItem(key, value);
  } catch (_) {
    /* sin almacenamiento: solo dura esta sesión */
  }
}

export function englishVoices() {
  return voices.filter((v) => v.lang && v.lang.toLowerCase().startsWith("en"));
}

export function getSettings() {
  return { voice: read(VOICE_KEY, ""), rate: Number(read(RATE_KEY, "1")) || 1 };
}

export function saveSettings({ voice, rate }) {
  if (voice !== undefined) write(VOICE_KEY, voice);
  if (rate !== undefined) write(RATE_KEY, String(rate));
}

function chooseVoice() {
  const list = englishVoices();
  const { voice } = getSettings();
  return (
    list.find((v) => v.name === voice) ||
    list.find((v) => v.lang === "en-US" && /natural|google|online/i.test(v.name)) ||
    list.find((v) => v.lang === "en-US") ||
    list[0] ||
    null
  );
}

// Lee el texto en inglés. `slow` lo lee más despacio que la velocidad elegida. Devuelve una promesa que termina al acabar.
export function speak(text, { slow = false } = {}) {
  if (!canSpeak()) return Promise.resolve();
  const synth = window.speechSynthesis;
  synth.cancel();
  return new Promise((resolve) => {
    const utterance = new SpeechSynthesisUtterance(text);
    const voice = chooseVoice();
    if (voice) utterance.voice = voice;
    utterance.lang = voice ? voice.lang : "en-US";
    utterance.rate = getSettings().rate * (slow ? 0.7 : 1);
    utterance.onend = resolve;
    utterance.onerror = resolve;
    synth.speak(utterance);
  });
}

const RECOGNITION_ERRORS = {
  "not-allowed": "El navegador no tiene permiso para usar el micrófono.",
  "service-not-allowed": "El navegador no permite el reconocimiento de voz en esta página.",
  "no-speech": "No se oyó nada. Acércate al micrófono e inténtalo de nuevo.",
  "audio-capture": "No se encontró ningún micrófono.",
  network: "El reconocimiento de voz necesita conexión a internet.",
};

// Escucha una frase en inglés. Devuelve { promise, stop }; la promesa da el texto reconocido.
export function listen() {
  const recognition = new Recognition();
  recognition.lang = "en-US";
  recognition.interimResults = false;
  recognition.continuous = false;
  recognition.maxAlternatives = 1;
  const promise = new Promise((resolve, reject) => {
    let heard = "";
    recognition.onresult = (event) => {
      heard = Array.from(event.results)
        .map((result) => result[0].transcript)
        .join(" ")
        .trim();
    };
    recognition.onerror = (event) => {
      if (event.error === "aborted") return;
      reject(new Error(RECOGNITION_ERRORS[event.error] || "Error de reconocimiento de voz: " + event.error));
    };
    recognition.onend = () => resolve(heard);
  });
  recognition.start();
  return { promise, stop: () => recognition.stop() };
}
