import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import CodeBlock from "./CodeBlock.jsx";

function textOf(node) {
  if (node === null || node === undefined || typeof node === "boolean") return "";
  if (typeof node === "string" || typeof node === "number") return String(node);
  if (Array.isArray(node)) return node.map(textOf).join("");
  return textOf(node.props && node.props.children);
}

// "2. Tipos de datos" -> "2-tipos-de-datos" (sin tildes), para enlazar las secciones desde el índice.
export function slugify(text) {
  return text
    .toLowerCase()
    .normalize("NFD")
    .replace(/[̀-ͯ]/g, "")
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-|-$/g, "");
}

// Títulos de nivel 2 de un texto Markdown, ignorando los bloques de código.
export function headingsOf(markdown) {
  const result = [];
  let inCode = false;
  for (const line of (markdown || "").split("\n")) {
    if (line.trim().startsWith("```")) inCode = !inCode;
    else if (!inCode && line.startsWith("## ")) {
      const text = line.slice(3).replace(/[`*]/g, "").trim();
      result.push({ id: slugify(text), text });
    }
  }
  return result;
}

const components = {
  a: ({ node, ...props }) => <a {...props} target="_blank" rel="noreferrer" />,
  h2: ({ node, children, ...props }) => (
    <h2 id={slugify(textOf(children))} {...props}>
      {children}
    </h2>
  ),
  table: ({ node, ...props }) => (
    <div className="table-wrap">
      <table {...props} />
    </div>
  ),
  // Los bloques ```lenguaje llegan como <pre><code class="language-x">.
  pre: ({ node, children }) => {
    const child = Array.isArray(children) ? children[0] : children;
    const className = (child && child.props && child.props.className) || "";
    const lang = (className.match(/language-([\w-]+)/) || [])[1];
    return <CodeBlock code={textOf(child).replace(/\n$/, "")} lang={lang} />;
  },
};

export default function Markdown({ children }) {
  return (
    <div className="markdown">
      <ReactMarkdown remarkPlugins={[remarkGfm]} components={components}>
        {children || ""}
      </ReactMarkdown>
    </div>
  );
}
