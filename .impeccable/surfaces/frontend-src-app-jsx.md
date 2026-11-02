---
version: 1
slug: "frontend-src-app-jsx"
primary_target: "frontend/src/App.jsx"
related_targets: ["frontend/src/styles.css"]
---

# Surface brief: DataPath app shell (all routes)

Scope: the whole study app (panel, ruta, tema, habilidades, inglés, login). Mode: Operate. Build path: code-led (Operate).
Audience and job: one junior developer studying ~5 h/day; open the app, see what comes next, read, practise, track progress.
Constraints: no content, endpoint or behaviour changes; Spanish UI; light scene (home study during the day and evening, long reading).
Unattended: the user delegated every visual decision ("dejo el diseño en tu criterio"); the assigned direction was taken without a decision round.

## Direction contract

THESIS: the app is the student's own cuaderno cuadriculado. Progress is counted in squares and the next step is literally highlighted, refusing the category default of a grey SaaS dashboard with green progress rings and same-size stat cards.

OWN-WORLD: cool paper-white ground, a deep ink-blue rail like a notebook cover, Bic-blue ink for primary action and links, a thin double red margin rule on reading columns, fluorescent yellow highlighter for "next / current", green highlighter for solved, red pen for errors. Faint blue 24px graph grid only where progress is counted. Hairline-ruled modules, no soft cards. Bricolage Grotesque display, Inter body, JetBrains Mono for code.

STORY: on any screen the student knows where they are and what is next; they see the path filling in square by square and trust the numbers because nothing is decorative.

FIRST VIEWPORT: left ink rail (brand, nav, "Siguiente" note pinned at its foot). Main column: page title in display type; on the panel, the next topic as a highlighted line with its continue button beside it, then the route drawn as a grid of squares (one per topic, coloured by status) with big tabular numbers for percent, streak and hours.

FORM: cuaderno cuadriculado, candidate 4 of 7 (1 Metro de Caracas map, 2 Cruz-Diez chromatic bands, 3 baseball scorecard, 4 graph-paper notebook, 5 exam bubble sheet, 6 academic transcript, 7 por-puesto route placards). seed:862884e4ebc07e41. Signature move: progress as notebook squares, with a highlighter sweep (one authored motion) marking the next step. Raises: from japanese-high-density-web (declined) hairline module density instead of inflated cards; from crouwel-grid-specimen (declined) every spacing token derived from the 24px cell; from terminal-yellow-wayfinding (competitive) the next step is signed persistently in the rail on every page; from variable-font-specimen (declined) hierarchy by scale contrast with big tabular numerals; from character-goods-catalog (declined) every topic row carries the same fixed furniture (status square, hours, exercise squares). boarding-pass-and-gate-board: competitive, not adopted.

FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance
