// Ejecuta el código Python del alumno en un Web Worker con Pyodide (Python en WebAssembly).
// Así el navegador no se congela con un bucle infinito y el código nunca toca el servidor.
const PYODIDE_VERSION = "0.26.4";
importScripts("https://cdn.jsdelivr.net/pyodide/v" + PYODIDE_VERSION + "/full/pyodide.js");

const WRAPPER = `
import sys, io, json, traceback

def __run(user_code, tests):
    ns = {"__name__": "__main__"}
    buffer = io.StringIO()
    previous = sys.stdout
    sys.stdout = buffer
    result = {"passed": False, "error": None, "feedback": None}
    try:
        exec(compile(user_code, "<tu_codigo>", "exec"), ns)
    except BaseException:
        result["error"] = traceback.format_exc(limit=-3)
    else:
        try:
            exec(compile(tests, "<pruebas>", "exec"), ns)
            result["passed"] = True
        except AssertionError as exc:
            result["feedback"] = str(exc) or "Alguna comprobacion no se cumplio."
        except BaseException:
            result["error"] = traceback.format_exc(limit=-3)
    finally:
        sys.stdout = previous
    result["output"] = buffer.getvalue()
    return json.dumps(result)
`;

let ready = null;
const loaded = new Set();

async function init() {
  const pyodide = await loadPyodide();
  pyodide.runPython('import os\nos.environ["MPLBACKEND"] = "agg"');
  pyodide.runPython(WRAPPER);
  return pyodide;
}

self.onmessage = async (event) => {
  const { id, code, tests, packages } = event.data;
  try {
    if (!ready) ready = init();
    const pyodide = await ready;
    const needed = (packages || []).filter((p) => !loaded.has(p));
    if (needed.length) {
      self.postMessage({ id, status: "loading", message: "Cargando " + needed.join(", ") + "…" });
      await pyodide.loadPackage(needed);
      needed.forEach((p) => loaded.add(p));
    }
    self.postMessage({ id, status: "running" });
    pyodide.globals.set("__user_code", code);
    pyodide.globals.set("__tests", tests);
    const raw = pyodide.runPython("__run(__user_code, __tests)");
    self.postMessage({ id, status: "done", result: JSON.parse(raw) });
  } catch (error) {
    ready = ready && null;
    self.postMessage({ id, status: "error", error: String(error) });
  }
};
