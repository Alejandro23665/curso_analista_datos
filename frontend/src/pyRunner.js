// Cliente del worker de Pyodide. Devuelve { passed, error, feedback, output }.
let worker = null;
let counter = 0;
const pending = new Map();

const LOAD_TIMEOUT_MS = 180000; // la primera vez hay que descargar Python (y pandas, etc.)

function failAll(message) {
  for (const entry of pending.values()) entry.fail(new Error(message));
  pending.clear();
}

function ensureWorker() {
  if (worker) return worker;
  worker = new Worker("/pyodide-worker.js");
  worker.onmessage = (event) => {
    const { id, status } = event.data;
    const entry = pending.get(id);
    if (!entry) return;
    if (status === "loading") {
      entry.onStatus && entry.onStatus(event.data.message);
    } else if (status === "running") {
      entry.startRunTimer();
    } else {
      pending.delete(id);
      if (status === "done") entry.done(event.data.result);
      else entry.fail(new Error(event.data.error));
    }
  };
  worker.onerror = (event) => {
    worker = null;
    failAll("No se pudo iniciar el intérprete de Python (" + (event.message || "error de carga") + "). Revisa tu conexión a internet.");
  };
  return worker;
}

export function runPython({ code, tests = "", packages = [], timeoutMs = 20000, onStatus }) {
  return new Promise((resolve, reject) => {
    const target = ensureWorker();
    const id = ++counter;
    let timer = null;

    const abort = (message) => {
      pending.delete(id);
      target.terminate();
      if (worker === target) worker = null;
      reject(new Error(message));
    };
    const arm = (ms, message) => {
      clearTimeout(timer);
      timer = setTimeout(() => abort(message), ms);
    };

    arm(LOAD_TIMEOUT_MS, "Tardó demasiado en cargar Python. Revisa tu conexión e inténtalo de nuevo.");
    pending.set(id, {
      onStatus,
      startRunTimer: () => arm(timeoutMs, "Tiempo agotado: ¿hay un bucle infinito? Se reinició el intérprete."),
      done: (result) => {
        clearTimeout(timer);
        resolve(result);
      },
      fail: (error) => {
        clearTimeout(timer);
        reject(error);
      },
    });
    target.postMessage({ id, code, tests, packages });
  });
}

// Descarga Python y los paquetes por adelantado para que el primer "Comprobar" sea rápido.
export function prewarm(packages = []) {
  return runPython({ code: "", tests: "", packages }).catch(() => {});
}
