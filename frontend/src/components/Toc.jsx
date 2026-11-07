import { useEffect, useState } from "react";
import { headingsOf } from "./Markdown.jsx";

// Índice de un capítulo largo: enlaza cada sección y resalta la que estás leyendo.
export default function Toc({ markdown, bookmarkKey }) {
  const headings = headingsOf(markdown);
  const [active, setActive] = useState(headings[0] ? headings[0].id : null);

  useEffect(() => {
    const elements = headings.map((h) => document.getElementById(h.id)).filter(Boolean);
    if (!elements.length) return undefined;
    const observer = new IntersectionObserver(
      (entries) => {
        const visible = entries.filter((e) => e.isIntersecting).sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
        if (visible.length) {
          setActive(visible[0].target.id);
          if (bookmarkKey) {
            try {
              localStorage.setItem(bookmarkKey, visible[0].target.id);
            } catch (_) {
              /* sin almacenamiento */
            }
          }
        }
      },
      { rootMargin: "0px 0px -70% 0px" }
    );
    elements.forEach((el) => observer.observe(el));
    return () => observer.disconnect();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [markdown, bookmarkKey]);

  if (headings.length < 3) return null;
  return (
    <nav className="toc" aria-label="En este capítulo">
      <p className="toc-title">En este capítulo</p>
      <ol>
        {headings.map((h) => (
          <li key={h.id}>
            <a href={"#" + h.id} className={h.id === active ? "active" : ""} aria-current={h.id === active ? "location" : undefined}>
              {h.text}
            </a>
          </li>
        ))}
      </ol>
    </nav>
  );
}
