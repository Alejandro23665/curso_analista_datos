import { useMemo, useState } from "react";
import { languageLabel, normalizeLanguage, tokenize } from "../highlight.js";

// Bloque de código de la teoría: fondo oscuro, colores por tipo de elemento y botón para copiar.
export default function CodeBlock({ code, lang }) {
  const language = normalizeLanguage(lang, code);
  const parts = useMemo(() => tokenize(code, language), [code, language]);
  const [copied, setCopied] = useState(false);

  async function copy() {
    try {
      await navigator.clipboard.writeText(code);
    } catch (_) {
      const area = document.createElement("textarea");
      area.value = code;
      document.body.appendChild(area);
      area.select();
      document.execCommand("copy");
      area.remove();
    }
    setCopied(true);
    setTimeout(() => setCopied(false), 1500);
  }

  return (
    <figure className="codeblock">
      <figcaption>
        <span className={"lang lang-" + language}>{languageLabel(language)}</span>
        <button type="button" onClick={copy} aria-label="Copiar código">
          {copied ? "✓ Copiado" : "Copiar"}
        </button>
      </figcaption>
      <pre>
        <code>
          {parts.map((part, index) =>
            part.type ? (
              <span key={index} className={"tok-" + part.type}>
                {part.text}
              </span>
            ) : (
              part.text
            )
          )}
        </code>
      </pre>
    </figure>
  );
}
