import { createContext, useCallback, useContext, useState } from "react";

// Ruta de aprendizaje seleccionada (se recuerda en este navegador).
const STORAGE_KEY = "datapath:track";
const TrackContext = createContext({ track: null, setTrack: () => {} });

function load() {
  try {
    return localStorage.getItem(STORAGE_KEY);
  } catch (_) {
    return null;
  }
}

export function TrackProvider({ children }) {
  const [track, setTrackState] = useState(load);
  const setTrack = useCallback((slug) => {
    setTrackState(slug);
    try {
      localStorage.setItem(STORAGE_KEY, slug);
    } catch (_) {
      /* sin almacenamiento: solo dura esta sesión */
    }
  }, []);
  return <TrackContext.Provider value={{ track, setTrack }}>{children}</TrackContext.Provider>;
}

export function useTrack() {
  return useContext(TrackContext);
}
