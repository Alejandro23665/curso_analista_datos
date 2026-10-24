import { useMemo, useRef } from "react";
import CodeMirror from "@uiw/react-codemirror";
import { python } from "@codemirror/lang-python";
import { sql, PostgreSQL } from "@codemirror/lang-sql";
import { keymap } from "@codemirror/view";
import { Prec } from "@codemirror/state";

// Editor con resaltado de sintaxis. Ctrl/Cmd + Enter ejecuta el código.
export default function CodeEditor({ value, onChange, language = "python", height = "260px", onRun, readOnly = false }) {
  const runRef = useRef(onRun);
  runRef.current = onRun;

  const extensions = useMemo(
    () => [
      language === "sql" ? sql({ dialect: PostgreSQL }) : python(),
      Prec.highest(
        keymap.of([
          {
            key: "Mod-Enter",
            run: () => {
              if (runRef.current) runRef.current();
              return true;
            },
          },
        ])
      ),
    ],
    [language]
  );

  return (
    <div className="editor">
      <CodeMirror
        value={value}
        height={height}
        theme="light"
        extensions={extensions}
        onChange={onChange}
        readOnly={readOnly}
        basicSetup={{ lineNumbers: true, foldGutter: false, highlightActiveLine: !readOnly }}
      />
    </div>
  );
}
