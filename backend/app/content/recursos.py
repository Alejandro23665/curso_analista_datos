"""Recursos recomendados por tema ("Para profundizar"). Se añaden al final de la teoría."""

_YT = "https://www.youtube.com/watch?v="

RECURSOS = {
    "ia-llm-fundamentos": [
        ("Video", "7 conceptos de IA que DEBES conocer — Ringa Tech (15 min)", _YT + "IHpLbziFGEQ"),
        ("Video", "Todo lo que necesitas saber de AI Engineering en 26 minutos — BettaTech", _YT + "kIbr5lN-2F8"),
        ("Libro", "AI Engineering — Chip Huyen (O'Reilly): la referencia para construir aplicaciones con modelos fundacionales", None),
    ],
    "ia-llm-rag": [
        ("Video", "Qué aprender en 2026: MCP, RAG, CLI y agentes — Fazt (sección RAG y bases vectoriales)", _YT + "lJLitlFAJfM"),
    ],
    "ia-agentes": [
        ("Video", "Qué aprender en 2026: MCP, RAG, CLI y agentes — Fazt", _YT + "lJLitlFAJfM"),
        ("Documentación", "Model Context Protocol: documentación oficial", "https://modelcontextprotocol.io"),
    ],
    "ia-evals-seguridad": [
        ("Video", "Todo lo que necesitas saber de AI Engineering en 26 minutos — BettaTech", _YT + "kIbr5lN-2F8"),
        ("Referencia", "OWASP Top 10 para aplicaciones con LLMs", "https://genai.owasp.org/llm-top-10/"),
    ],
    "ia-agentes-codigo": [
        ("Video", "How Senior Engineers Actually Build with AI in 2026 — JavaScript Mastery (proyecto en JS: quédate con el método)", _YT + "9dKA2hq4vf0"),
        ("Video", "Deja de hacer solo Front + Back + DB — Fazt", _YT + "6u6pEaageRQ"),
    ],
    "frontend-ia": [
        ("Documentación", "React: aprende React (documentación oficial)", "https://react.dev/learn"),
        ("Documentación", "TypeScript Handbook", "https://www.typescriptlang.org/docs/handbook/intro.html"),
        ("Documentación", "MDN: Server-sent events", "https://developer.mozilla.org/en-US/docs/Web/API/Server-sent_events"),
    ],
    "empleo-ia": [
        ("Video", "Cómo la IA está transformando las entrevistas técnicas — Patri Juane (20 min; las preguntas de entrevistas asistidas por IA, desde el minuto 15:50)", _YT + "9Ok4IVsZvPw"),
    ],
    "algoritmos-entrevistas": [
        ("Práctica", "NeetCode: problemas de entrevista agrupados por patrón, con explicaciones", "https://neetcode.io"),
        ("Práctica", "LeetCode: empieza por los problemas Easy de arrays, hash maps y pilas", "https://leetcode.com"),
    ],
    "sys-apis": [
        ("Curso", "System Design Course: APIs, Databases, Caching, CDNs, Load Balancing — freeCodeCamp (2 h, en inglés)", _YT + "C842vFY5kRo"),
    ],
    "sys-diseno": [
        ("Curso", "System Design Course: APIs, Databases, Caching, CDNs, Load Balancing — freeCodeCamp (2 h, en inglés)", _YT + "C842vFY5kRo"),
        ("Libro", "Designing Data-Intensive Applications — Martin Kleppmann: la referencia sobre bases de datos y sistemas distribuidos", None),
        ("Video", "20 conceptos clave de System Design — Patri Juane (25 min, en español)", _YT + "AqHnDVhyz2s"),
        ("Video", "Entrevistas de Systems Design: guía paso a paso — Patri Juane (16 min)", _YT + "SnlC8z8VlUs"),
    ],
    "sys-arquitectura": [
        ("Video", "Arquitectura de Software Completa: Monolitos, Microservicios, EDA, Sagas y CQRS (1 h 18 min)", _YT + "sofWhc9fvzA"),
    ],
    "sys-distribuida": [
        ("Video", "Arquitectura de Software Completa: Monolitos, Microservicios, EDA, Sagas y CQRS (1 h 18 min)", _YT + "sofWhc9fvzA"),
        ("Libro", "Designing Data-Intensive Applications — Martin Kleppmann", None),
    ],
    "startup-mvp": [
        ("Video", "La habilidad más importante de un Ingeniero no es programar (complementario, 27 min)", _YT + "vl6LOZNku1U"),
    ],
}


def seccion_recursos(slug):
    recursos = RECURSOS.get(slug)
    if not recursos:
        return ""
    lineas = ["", "## Para profundizar", ""]
    for tipo, titulo, url in recursos:
        lineas.append("- **%s:** %s" % (tipo, "[%s](%s)" % (titulo, url) if url else titulo))
    lineas.append("")
    lineas.append("> Los videos dan el panorama; la profundidad sale de construir, de los ejercicios y de la documentación oficial.")
    return "\n".join(lineas) + "\n"
