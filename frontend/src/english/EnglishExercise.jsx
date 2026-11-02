import { useEffect, useRef, useState } from "react";
import { Check, CircleHelp, Headphones, Keyboard, Languages, Mic, PenLine, Square, TriangleAlert } from "lucide-react";
import { Verdict } from "../components/ExercisePanel.jsx";
import Markdown from "../components/Markdown.jsx";
import AudioButtons from "./AudioButtons.jsx";
import { canListen, listen } from "./speech.js";

export const EN_KINDS = {
  choice: { Icon: CircleHelp, label: "Elegir" },
  listen: { Icon: Headphones, label: "Escucha" },
  fill: { Icon: PenLine, label: "Completar" },
  translate: { Icon: Languages, label: "Traducir" },
  dictation: { Icon: Keyboard, label: "Dictado" },
  speak: { Icon: Mic, label: "Hablar" },
};

const INSTRUCTIONS = {
  listen: "Escucha el audio (puedes repetirlo) y responde. El texto aparece al acertar.",
  fill: "Escribe la palabra que falta.",
  translate: "Traduce al inglés.",
  dictation: "Escucha y escribe exactamente lo que oyes.",
};

// `onSubmit(body)` envía la respuesta al servidor y devuelve el resultado de la corrección.
export default function EnglishExercise({ exercise, index, solved, onSubmit }) {
  const { Icon, label } = EN_KINDS[exercise.kind];
  return (
    <section className="exercise">
      <header className="exercise-head">
        <h2>Ejercicio {index}</h2>
        <span className="tag">
          <Icon size={14} aria-hidden="true" /> {label}
        </span>
        {solved && (
          <span className="tag ok">
            <Check size={14} aria-hidden="true" /> Resuelto
          </span>
        )}
      </header>
      {INSTRUCTIONS[exercise.kind] && <p className="muted">{INSTRUCTIONS[exercise.kind]}</p>}
      {exercise.kind === "choice" && <ChoiceExercise exercise={exercise} onSubmit={onSubmit} />}
      {exercise.kind === "listen" && <ChoiceExercise exercise={exercise} onSubmit={onSubmit} audio />}
      {exercise.kind === "fill" && <FillExercise exercise={exercise} onSubmit={onSubmit} />}
      {exercise.kind === "translate" && <TextExercise exercise={exercise} onSubmit={onSubmit} />}
      {exercise.kind === "dictation" && <TextExercise exercise={exercise} onSubmit={onSubmit} />}
      {exercise.kind === "speak" && <SpeakExercise exercise={exercise} onSubmit={onSubmit} />}
    </section>
  );
}

function useSubmit(onSubmit) {
  const [result, setResult] = useState(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  async function send(body) {
    setBusy(true);
    setError("");
    try {
      setResult(await onSubmit(body));
    } catch (e) {
      setError(e.message);
    } finally {
      setBusy(false);
    }
  }
  return { result, setResult, busy, error, send };
}

function ErrorLine({ children }) {
  return (
    <p className="verdict bad" role="alert">
      <TriangleAlert size={18} aria-hidden="true" /> {children}
    </p>
  );
}

function ChoiceExercise({ exercise, onSubmit, audio = false }) {
  const [choice, setChoice] = useState(null);
  const { result, setResult, busy, error, send } = useSubmit(onSubmit);
  const locked = Boolean(result && result.correct);

  return (
    <div className="stack">
      {audio && (
        <div className="en-audio">
          <Headphones size={20} aria-hidden="true" />
          <AudioButtons text={exercise.audio} />
        </div>
      )}
      <div className="exercise-prompt">
        <Markdown>{exercise.prompt}</Markdown>
      </div>
      <ul className="options">
        {exercise.options.map((text, index) => {
          let state = "";
          if (result && choice === index) state = result.correct ? " right" : " wrong";
          return (
            <li key={index}>
              <label className={"option" + (choice === index ? " selected" : "") + state}>
                <input
                  type="radio"
                  name={exercise.id}
                  checked={choice === index}
                  disabled={busy || locked}
                  onChange={() => {
                    setChoice(index);
                    setResult(null);
                  }}
                />
                <span>{text}</span>
              </label>
            </li>
          );
        })}
      </ul>
      <div className="actions">
        <button className="btn primary" disabled={busy || locked || choice === null} onClick={() => send({ answer: choice })}>
          Responder
        </button>
      </div>
      {error && <ErrorLine>{error}</ErrorLine>}
      {result && (
        <div className="console" aria-live="polite">
          {result.correct ? <Verdict ok>Correcto.</Verdict> : <Verdict>No es esa. Vuelve a escuchar o a leer e inténtalo otra vez.</Verdict>}
          {result.correct && result.explanation && <Markdown>{result.explanation}</Markdown>}
          {result.correct && result.transcript && (
            <p className="en-transcript" lang="en">
              <strong>Transcripción:</strong> {result.transcript}
            </p>
          )}
        </div>
      )}
    </div>
  );
}

function FillExercise({ exercise, onSubmit }) {
  const [text, setText] = useState("");
  const { result, setResult, busy, error, send } = useSubmit(onSubmit);
  const [before, after] = exercise.sentence.split("___");
  const input = useRef(null);
  useEffect(() => input.current && input.current.focus(), []);

  function submit(event) {
    event.preventDefault();
    if (text.trim()) send({ text });
  }

  return (
    <form onSubmit={submit} className="stack">
      <p className="en-sentence" lang="en">
        {before}
        <input
          ref={input}
          className={"en-gap" + (result ? (result.correct ? " right" : " wrong") : "")}
          value={text}
          onChange={(event) => {
            setText(event.target.value);
            setResult(null);
          }}
          aria-label="Palabra que falta"
          autoComplete="off"
          autoCapitalize="off"
          spellCheck="false"
        />
        {after}
      </p>
      {exercise.es && <p className="muted small">{exercise.es}</p>}
      <div className="actions">
        <button className="btn primary" disabled={busy || !text.trim()}>
          Comprobar
        </button>
        <AudioButtons text={exercise.sentence.replace("___", "...")} compact />
      </div>
      {error && <ErrorLine>{error}</ErrorLine>}
      {result && (
        <div className="console" aria-live="polite">
          {result.correct ? <Verdict ok>Correcto.</Verdict> : <Verdict>Aún no.</Verdict>}
          {result.correct ? (
            result.explanation && <Markdown>{result.explanation}</Markdown>
          ) : (
            <RevealAnswer expected={result.expected} explanation={result.explanation} />
          )}
        </div>
      )}
    </form>
  );
}

function RevealAnswer({ expected, explanation = "" }) {
  const [show, setShow] = useState(false);
  return show ? (
    <>
      <p>
        Respuesta: <strong lang="en">{expected}</strong>
      </p>
      {explanation && <Markdown>{explanation}</Markdown>}
    </>
  ) : (
    <div>
      <button type="button" className="btn ghost small" onClick={() => setShow(true)}>
        Ver la respuesta
      </button>
    </div>
  );
}

function TextExercise({ exercise, onSubmit }) {
  const [text, setText] = useState("");
  const { result, setResult, busy, error, send } = useSubmit(onSubmit);
  const dictation = exercise.kind === "dictation";

  function submit(event) {
    event.preventDefault();
    if (text.trim()) send({ text });
  }

  return (
    <form onSubmit={submit} className="stack">
      {dictation ? (
        <div className="en-audio">
          <Headphones size={20} aria-hidden="true" />
          <AudioButtons text={exercise.text} />
        </div>
      ) : (
        <p className="en-sentence">«{exercise.es}»</p>
      )}
      <textarea
        className="en-answer"
        rows={2}
        value={text}
        lang="en"
        aria-label={dictation ? "Lo que oyes" : "Tu traducción"}
        placeholder={dictation ? "Escribe lo que oyes…" : "Your translation…"}
        onChange={(event) => {
          setText(event.target.value);
          setResult(null);
        }}
        onKeyDown={(event) => {
          if (event.key === "Enter" && !event.shiftKey) submit(event);
        }}
        autoComplete="off"
        autoCapitalize="off"
        spellCheck="false"
      />
      <div className="actions">
        <button className="btn primary" disabled={busy || !text.trim()}>
          Comprobar
        </button>
        <span className="muted small">Enter para comprobar · no importan mayúsculas, puntuación ni contracciones (I'm = I am)</span>
      </div>
      {error && <ErrorLine>{error}</ErrorLine>}
      {result && <TextResult result={result} es={dictation ? exercise.es : ""} />}
    </form>
  );
}

function Score({ result }) {
  return "Parecido " + Math.round(result.score * 100) + " %" + (result.correct ? "" : " (hace falta " + Math.round(result.threshold * 100) + " %)");
}

function TextResult({ result, es }) {
  return (
    <div className="console" aria-live="polite">
      <Verdict ok={result.correct} detail={<Score result={result} />}>
        {result.correct ? "Correcto." : "Casi."}
      </Verdict>
      {(result.missing.length > 0 || result.extra.length > 0) && (
        <p className="small">
          {result.missing.length > 0 && (
            <>
              Faltó o cambió:{" "}
              {result.missing.map((w, i) => (
                <mark key={"m" + i} className="en-missing">
                  {w}
                </mark>
              ))}{" "}
            </>
          )}
          {result.extra.length > 0 && (
            <>
              Sobró:{" "}
              {result.extra.map((w, i) => (
                <mark key={"e" + i} className="en-extra">
                  {w}
                </mark>
              ))}
            </>
          )}
        </p>
      )}
      {result.correct || result.score >= 0.5 ? (
        <p className="row">
          <span>
            {result.correct ? "Referencia" : "Respuesta esperada"}: <strong lang="en">{result.expected}</strong>
          </span>
          <AudioButtons text={result.expected} compact />
        </p>
      ) : (
        <RevealAnswer expected={result.expected} />
      )}
      {es && <p className="muted small">{es}</p>}
      {result.explanation && <Markdown>{result.explanation}</Markdown>}
    </div>
  );
}

function SpeakExercise({ exercise, onSubmit }) {
  const [recording, setRecording] = useState(null);
  const [micError, setMicError] = useState("");
  const [typed, setTyped] = useState("");
  const { result, busy, error, send } = useSubmit(onSubmit);
  const supported = canListen();

  async function record() {
    setMicError("");
    const session = listen();
    setRecording(session);
    try {
      const heard = await session.promise;
      if (heard) await send({ text: heard });
      else setMicError("No se reconoció ninguna frase. Inténtalo de nuevo.");
    } catch (e) {
      setMicError(e.message);
    } finally {
      setRecording(null);
    }
  }

  return (
    <div className="stack">
      <div className="exercise-prompt">
        <Markdown>{exercise.prompt}</Markdown>
      </div>
      {exercise.target && (
        <div className="en-target">
          <p className="en-sentence" lang="en">
            {exercise.target}
          </p>
          <AudioButtons text={exercise.target} label="Escuchar el modelo" />
        </div>
      )}
      {supported ? (
        <div className="actions">
          {recording ? (
            <button className="btn primary en-recording" onClick={() => recording.stop()}>
              <Square size={14} aria-hidden="true" /> Detener
            </button>
          ) : (
            <button className="btn primary" disabled={busy} onClick={record}>
              <Mic size={16} aria-hidden="true" /> {result ? "Intentar de nuevo" : "Hablar"}
            </button>
          )}
          {recording && (
            <span className="muted small" aria-live="polite">
              Escuchando… di la frase y espera un momento.
            </span>
          )}
        </div>
      ) : (
        <form
          className="stack"
          onSubmit={(event) => {
            event.preventDefault();
            if (typed.trim()) send({ text: typed });
          }}
        >
          <p className="notice">
            <TriangleAlert size={16} aria-hidden="true" />
            <span>
              Tu navegador no tiene reconocimiento de voz (funciona en Chrome y Edge). Di la frase en voz alta igualmente y escríbela aquí
              para comprobarla.
            </span>
          </p>
          <textarea className="en-answer" rows={2} lang="en" aria-label="La frase que dijiste" value={typed} onChange={(event) => setTyped(event.target.value)} />
          <div className="actions">
            <button className="btn primary" disabled={busy || !typed.trim()}>
              Comprobar
            </button>
          </div>
        </form>
      )}
      {(micError || error) && <ErrorLine>{micError || error}</ErrorLine>}
      {result && (
        <div className="console" aria-live="polite">
          <p className="small">
            Se entendió: <em lang="en">«{result.heard}»</em>
          </p>
          <Verdict ok={result.correct} detail={"Parecido " + Math.round(result.score * 100) + " %"}>
            {result.correct ? "Muy bien: se te entiende." : "Aún no se entiende del todo."}
          </Verdict>
          {result.missing.length > 0 && (
            <p className="small">
              Palabras que no se reconocieron:{" "}
              {result.missing.map((w, i) => (
                <mark key={i} className="en-missing">
                  {w}
                </mark>
              ))}
              <span className="muted"> — escucha el modelo y fíjate en su pronunciación.</span>
            </p>
          )}
          <p className="row">
            <span>
              Frase esperada: <strong lang="en">{result.expected}</strong>
            </span>
            <AudioButtons text={result.expected} compact />
          </p>
        </div>
      )}
    </div>
  );
}
