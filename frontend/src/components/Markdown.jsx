import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import CodeBlock from "./CodeBlock.jsx";

function textOf(node) {
  if (node === null || node === undefined || typeof node === "boolean") return "";
  if (typeof node === "string" || typeof node === "number") return String(node);
  if (Array.isArray(node)) return node.map(textOf).join("");
  return textOf(node.props && node.props.children);
}

const components = {
  a: ({ node, ...props }) => <a {...props} target="_blank" rel="noreferrer" />,
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
