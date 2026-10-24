// Resaltado de sintaxis ligero (sin dependencias) para los bloques de código de la teoría.
// Devuelve una lista de fragmentos { type, text } donde type es kw, str, num, com, fn, bi o null.

const words = (list) => new Set(list.trim().split(/\s+/));

const PYTHON_KW = words(`
  def return if elif else for while in not and or is None True False import from as with try except finally
  raise class lambda pass break continue yield global nonlocal assert del async await
`);
const PYTHON_BUILTINS = words(`
  print len range sum min max sorted list dict set tuple int float str bool enumerate zip open type isinstance
  round abs any all map filter super object reversed input
`);
const SQL_KW = words(`
  SELECT FROM WHERE GROUP BY ORDER HAVING JOIN LEFT RIGHT INNER FULL OUTER CROSS ON AS AND OR NOT IN IS NULL
  LIKE ILIKE BETWEEN DISTINCT LIMIT OFFSET WITH CASE WHEN THEN ELSE END OVER PARTITION ASC DESC INSERT INTO
  VALUES UPDATE SET DELETE CREATE TABLE VIEW INDEX PRIMARY KEY FOREIGN REFERENCES UNION ALL EXISTS CONFLICT DO
  NOTHING FILTER INTERVAL ROWS PRECEDING FOLLOWING CURRENT ROW EXPLAIN ANALYZE RETURNING DROP ALTER ADD
  CONSTRAINT UNIQUE DEFAULT CHECK TRUE FALSE
`);
const BASH_KW = words(`
  cd ls pwd cat head tail grep wc curl jq git docker pip python python3 npm npx node source export echo mkdir
  rm cp mv chmod sudo apt copy start set
`);
const DOCKER_KW = words(`FROM WORKDIR COPY RUN CMD ENV EXPOSE ARG ENTRYPOINT VOLUME USER LABEL ADD`);

const NUMBER = String.raw`\b\d+(?:\.\d+)?(?:[eE][+-]?\d+)?\b`;
const IDENT = String.raw`[A-Za-z_][\w.]*`;

// Cada lenguaje: expresión con grupos (en orden de prioridad) y cómo clasificar las palabras.
const LANGS = {
  python: {
    pattern: [
      String.raw`(?<com>#[^\n]*)`,
      String.raw`(?<str>[rRfFbB]{0,2}(?:"""[\s\S]*?"""|'''[\s\S]*?'''|"(?:\\.|[^"\\\n])*"|'(?:\\.|[^'\\\n])*'))`,
      String.raw`(?<num>${NUMBER})`,
      String.raw`(?<word>[A-Za-z_]\w*)`,
    ],
    word: (w, next) => (PYTHON_KW.has(w) ? "kw" : PYTHON_BUILTINS.has(w) ? "bi" : next === "(" ? "fn" : null),
  },
  sql: {
    pattern: [
      String.raw`(?<com>--[^\n]*)`,
      String.raw`(?<str>'(?:''|[^'])*')`,
      String.raw`(?<num>${NUMBER})`,
      String.raw`(?<word>[A-Za-z_]\w*)`,
    ],
    word: (w, next) => (SQL_KW.has(w.toUpperCase()) ? "kw" : next === "(" ? "fn" : null),
  },
  bash: {
    pattern: [
      String.raw`(?<com>(?:^|(?<=\s))#[^\n]*)`,
      String.raw`(?<str>"(?:\\.|[^"\\])*"|'[^']*')`,
      String.raw`(?<word>[A-Za-z_][\w-]*)`,
    ],
    word: (w) => (BASH_KW.has(w) ? "kw" : null),
  },
  dockerfile: {
    pattern: [String.raw`(?<com>#[^\n]*)`, String.raw`(?<str>"(?:\\.|[^"\\])*")`, String.raw`(?<word>[A-Za-z_][\w-]*)`],
    word: (w) => (DOCKER_KW.has(w) ? "kw" : null),
  },
  // Fórmulas de Excel y DAX: funciones en mayúsculas seguidas de "(".
  formula: {
    pattern: [
      String.raw`(?<com>\/\/[^\n]*)`,
      String.raw`(?<str>"(?:""|[^"])*")`,
      String.raw`(?<num>${NUMBER})`,
      String.raw`(?<word>${IDENT})`,
    ],
    word: (w, next) => (next === "(" && w === w.toUpperCase() ? "fn" : null),
  },
};

const LABELS = { python: "Python", sql: "SQL", bash: "Terminal", dockerfile: "Dockerfile", formula: "Fórmula", text: "Ejemplo" };

const compiled = {};
function regexFor(lang) {
  if (!compiled[lang]) compiled[lang] = new RegExp(LANGS[lang].pattern.join("|"), "gm");
  return compiled[lang];
}

// Adivina el lenguaje de un bloque sin etiqueta.
export function detectLanguage(code) {
  const text = code.trim();
  if (/^(SELECT|WITH|INSERT|UPDATE|CREATE|EXPLAIN)\b/i.test(text)) return "sql";
  if (/^=/.test(text) || /\b(CALCULATE|SUMX|DIVIDE|DISTINCTCOUNT|CALENDAR|SUMAR\.SI\.CONJUNTO|BUSCARX)\s*\(/.test(text)) return "formula";
  if (/^\s*(def |import |from \w+ import|print\()/m.test(text)) return "python";
  return "text";
}

export function languageLabel(lang) {
  return LABELS[lang] || LABELS.text;
}

export function normalizeLanguage(lang, code) {
  const key = (lang || "").toLowerCase();
  if (key === "py") return "python";
  if (key === "sh" || key === "shell" || key === "powershell" || key === "ps1") return "bash";
  if (key === "dax" || key === "excel") return "formula";
  if (LANGS[key]) return key;
  return detectLanguage(code);
}

export function tokenize(code, lang) {
  const spec = LANGS[lang];
  if (!spec) return [{ type: null, text: code }];
  const re = regexFor(lang);
  re.lastIndex = 0;
  const parts = [];
  let last = 0;
  let match;
  while ((match = re.exec(code)) !== null) {
    if (match[0] === "") {
      re.lastIndex += 1;
      continue;
    }
    if (match.index > last) parts.push({ type: null, text: code.slice(last, match.index) });
    const groups = match.groups;
    let type = null;
    if (groups.com !== undefined) type = "com";
    else if (groups.str !== undefined) type = "str";
    else if (groups.num !== undefined) type = "num";
    else if (groups.word !== undefined) {
      const rest = code.slice(re.lastIndex);
      const next = (rest.match(/^\s*(\S)/) || [])[1];
      type = spec.word(groups.word, next);
    }
    parts.push({ type, text: match[0] });
    last = re.lastIndex;
  }
  if (last < code.length) parts.push({ type: null, text: code.slice(last) });
  return parts;
}
