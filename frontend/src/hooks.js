import { useCallback, useEffect, useRef, useState } from "react";

// Carga datos asíncronos y los vuelve a pedir cuando cambian las dependencias.
export function useAsync(loader, deps = []) {
  const [state, setState] = useState({ loading: true, data: null, error: null });
  const ticket = useRef(0);

  const run = useCallback(() => {
    const mine = ++ticket.current;
    setState((previous) => ({ ...previous, loading: true, error: null }));
    return loader()
      .then((data) => {
        if (mine === ticket.current) setState({ loading: false, data, error: null });
        return data;
      })
      .catch((error) => {
        if (mine === ticket.current) setState({ loading: false, data: null, error });
      });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps);

  useEffect(() => {
    run();
    return () => {
      ticket.current += 1;
    };
  }, [run]);

  // setData acepta un valor o una función (datos anteriores) => datos nuevos
  const setData = useCallback((updater) => {
    setState((previous) => ({
      loading: false,
      error: null,
      data: typeof updater === "function" ? updater(previous.data) : updater,
    }));
  }, []);

  return { ...state, reload: run, setData };
}
