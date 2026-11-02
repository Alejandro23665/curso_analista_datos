---
name: DataPath
description: Plataforma de estudio personal dibujada como el cuaderno cuadriculado del propio alumno.
colors:
  paper: "#fafbfd"
  paper-2: "#f2f5fa"
  paper-3: "#e9eef6"
  sheet: "#ffffff"
  grid: "#dce4f2"
  rule: "#d3dbe8"
  rule-strong: "#b9c4d6"
  ink: "#15203a"
  ink-soft: "#4a5874"
  blue: "#1d3fb0"
  blue-hover: "#16318d"
  blue-wash: "#e7ecfb"
  cover: "#12204a"
  cover-2: "#1c2d63"
  cover-ink: "#eef1fb"
  cover-muted: "#aab6d9"
  margin: "#cf2f3b"
  margin-wash: "#fde9ea"
  hl: "#fff176"
  hl-strong: "#ffe94a"
  hl-green: "#bdf0a4"
  hl-wash: "#fffbe0"
  hl-wash-rule: "#f0de6a"
  ok: "#1f7a37"
  warn: "#9a5b00"
  warn-wash: "#fff3dc"
  bad: "#c22a35"
  muted-cell: "#c5cfe0"
  code-bg: "#111a33"
  code-bar: "#0c1429"
  code-rule: "#1d2a4f"
  code-text: "#e7ecf7"
typography:
  display:
    fontFamily: "Bricolage Grotesque Variable, Bricolage Grotesque, Segoe UI, sans-serif"
    fontSize: "clamp(1.9rem, 1.4rem + 1.6vw, 2.6rem)"
    fontWeight: 750
    lineHeight: 1.15
    letterSpacing: "-0.025em"
  figure:
    fontFamily: "Bricolage Grotesque Variable, Bricolage Grotesque, Segoe UI, sans-serif"
    fontSize: "2.4rem"
    fontWeight: 700
    lineHeight: 1
    letterSpacing: "-0.03em"
    fontFeature: "tnum"
  headline:
    fontFamily: "Bricolage Grotesque Variable, Bricolage Grotesque, Segoe UI, sans-serif"
    fontSize: "1.45rem"
    fontWeight: 700
    lineHeight: 1.15
    letterSpacing: "-0.015em"
  title:
    fontFamily: "Bricolage Grotesque Variable, Bricolage Grotesque, Segoe UI, sans-serif"
    fontSize: "1.12rem"
    fontWeight: 700
    lineHeight: 1.15
    letterSpacing: "-0.01em"
  body:
    fontFamily: "Inter Variable, Inter, Segoe UI, system-ui, sans-serif"
    fontSize: "15.5px"
    fontWeight: 400
    lineHeight: 1.6
    fontFeature: "cv11, ss01"
  reading:
    fontFamily: "Inter Variable, Inter, Segoe UI, system-ui, sans-serif"
    fontSize: "1.01rem"
    fontWeight: 400
    lineHeight: 1.7
  label:
    fontFamily: "Inter Variable, Inter, Segoe UI, system-ui, sans-serif"
    fontSize: "0.84rem"
    fontWeight: 600
    lineHeight: 1.3
  mono:
    fontFamily: "JetBrains Mono Variable, JetBrains Mono, Consolas, Menlo, monospace"
    fontSize: "0.9rem"
    fontWeight: 400
    lineHeight: 1.7
rounded:
  cell-sm: "2px"
  cell: "3px"
  tag: "4px"
  md: "6px"
spacing:
  s1: "4px"
  s2: "8px"
  s3: "12px"
  s4: "16px"
  s5: "24px"
  s6: "36px"
  s7: "48px"
  s8: "72px"
  cell: "24px"
  rail: "248px"
components:
  button-primary:
    backgroundColor: "{colors.blue}"
    textColor: "{colors.sheet}"
    typography: "{typography.label}"
    rounded: "{rounded.md}"
    padding: "0 16px"
    height: "40px"
  button-primary-hover:
    backgroundColor: "{colors.blue-hover}"
    textColor: "{colors.sheet}"
  button-secondary:
    backgroundColor: "{colors.sheet}"
    textColor: "{colors.ink}"
    rounded: "{rounded.md}"
    padding: "0 16px"
    height: "40px"
  button-ghost:
    backgroundColor: "transparent"
    textColor: "{colors.blue}"
    rounded: "{rounded.md}"
    padding: "0 16px"
    height: "40px"
  button-ghost-hover:
    backgroundColor: "{colors.blue-wash}"
    textColor: "{colors.blue-hover}"
  button-small:
    rounded: "{rounded.md}"
    padding: "0 12px"
    height: "32px"
  tag:
    backgroundColor: "{colors.paper-3}"
    textColor: "{colors.ink}"
    rounded: "{rounded.tag}"
    padding: "2px 8px"
  tag-next:
    backgroundColor: "{colors.hl}"
    textColor: "{colors.ink}"
    rounded: "{rounded.tag}"
    padding: "2px 8px"
  tag-ok:
    backgroundColor: "{colors.hl-green}"
    textColor: "#13461f"
    rounded: "{rounded.tag}"
    padding: "2px 8px"
  tag-level:
    backgroundColor: "{colors.blue}"
    textColor: "{colors.sheet}"
    rounded: "{rounded.tag}"
    padding: "2px 8px"
  nav-item:
    backgroundColor: "transparent"
    textColor: "{colors.cover-muted}"
    rounded: "{rounded.md}"
    padding: "9px 12px"
  nav-item-hover:
    backgroundColor: "{colors.cover-2}"
    textColor: "{colors.cover-ink}"
  nav-item-active:
    backgroundColor: "{colors.cover-ink}"
    textColor: "{colors.cover}"
  rail:
    backgroundColor: "{colors.cover}"
    textColor: "{colors.cover-ink}"
    width: "{spacing.rail}"
    padding: "24px 16px 16px"
  square-todo:
    backgroundColor: "{colors.sheet}"
    rounded: "{rounded.cell}"
    size: "18px"
  square-done:
    backgroundColor: "{colors.blue}"
    rounded: "{rounded.cell}"
    size: "18px"
  square-next:
    backgroundColor: "{colors.hl-strong}"
    rounded: "{rounded.cell}"
    size: "18px"
  panel:
    backgroundColor: "{colors.paper-2}"
    rounded: "{rounded.md}"
    padding: "24px"
  input-field:
    backgroundColor: "{colors.sheet}"
    textColor: "{colors.ink}"
    rounded: "{rounded.md}"
    padding: "0 12px"
    height: "40px"
  codeblock:
    backgroundColor: "{colors.code-bg}"
    textColor: "{colors.code-text}"
    typography: "{typography.mono}"
    rounded: "{rounded.md}"
    padding: "16px"
---

# Design System: DataPath

## Overview

**Creative North Star: "El cuaderno cuadriculado"**

DataPath es el cuaderno del propio alumno. El fondo es papel blanco frío, la barra lateral es la tapa azul tinta del cuaderno, las acciones y los enlaces están escritos con bolígrafo Bic azul, las hojas de lectura llevan el margen rojo doble y lo que toca después está pasado con resaltador amarillo. El avance se cuenta en cuadritos: cada tema es una celda que se rellena a bolígrafo, se rellena a medias mientras está en curso o se resalta cuando es el siguiente.

La densidad es de cuaderno de estudio, no de panel de SaaS: módulos separados por una regla fina de tinta en lugar de tarjetas con sombra, cifras grandes con números tabulares, filas de temas con el mismo mobiliario fijo (cuadrito de estado, título, horas, porcentaje). Nada es decorativo: cada color tiene un significado de cuaderno (tinta, resaltador, margen, bolígrafo rojo) y se usa solo para ese significado. El papel cuadriculado de 24 px aparece únicamente donde se cuenta el avance.

Se rechaza explícitamente el panel gris genérico con anillos de progreso verdes y tarjetas de estadística del mismo tamaño.

**Key Characteristics:**
- Papel blanco frío (`paper`) con tapa azul tinta (`cover`) a la izquierda.
- Progreso dibujado como cuadritos del cuaderno, no como anillos ni barras gruesas.
- Resaltador amarillo para "siguiente / actual", verde para "resuelto", rojo de bolígrafo para errores.
- Módulos con regla superior de tinta; bordes finos; sin sombras en la página.
- Bricolage Grotesque para títulos y cifras, Inter para lectura, JetBrains Mono para código.
- Una sola animación con autor: el barrido del resaltador.

## Colors

Una paleta de papelería: papel frío y azulado, tinta azul marino, bolígrafo Bic, margen rojo y resaltadores fluorescentes, cada uno con un único significado.

### Primary
- **Tinta Bic** (`blue`): acción principal, enlaces, cuadritos completados, pestaña activa, barras de las gráficas, foco. Su versión `blue-hover` es el trazo más apretado al pasar el ratón; `blue-wash` es el fondo de selección (opción elegida, ejercicio activo, cita, sombra de foco de los campos).

### Secondary
- **Tapa del cuaderno** (`cover`): fondo de la barra lateral y del acceso. `cover-2` es el relieve de la tapa (hover de la navegación, borde de la nota "Siguiente"); `cover-ink` el texto claro sobre la tapa y el fondo del elemento de navegación activo; `cover-muted` el texto secundario sobre la tapa.

### Tertiary
- **Resaltador amarillo** (`hl`, `hl-strong`): exclusivamente "lo siguiente" o "lo actual": barrido sobre el título del siguiente tema, cuadrito siguiente (`hl-strong`), etiqueta "siguiente", selección de texto, hueco del dictado de inglés. `hl-wash` con su borde `hl-wash-rule` es el papel amarillento de los avisos, las pistas, la fila del siguiente tema y la tira "Siguiente" en móvil.
- **Resaltador verde** (`hl-green`): resuelto o correcto (etiqueta "ok", hueco acertado, punto de lenguaje bash en el código).
- **Margen rojo** (`margin`): la regla doble de las hojas de lectura y el borde del cuadrito con errores; `margin-wash` es el fondo de la opción incorrecta y de la palabra que falta.

### Neutral
- **Papel** (`paper`): fondo de la aplicación. `paper-2` es el papel de los paneles, la consola y el canal del editor; `paper-3` el fondo de etiquetas, código en línea y pista de las barras.
- **Hoja** (`sheet`, blanco puro): superficies sobre el papel donde se escribe o se cuenta: botones secundarios, opciones, hoja de ruta, cuadritos vacíos, campos. En el CSS aparece como literal `#ffffff`.
- **Cuadrícula** (`grid`): las líneas del papel cuadriculado y de las gráficas.
- **Reglas** (`rule`, `rule-strong`): separadores de filas y bordes finos; `rule-strong` para bordes de controles y celdas vacías. `muted-cell` es el borde del cuadrito pendiente.
- **Tinta** (`ink`, `ink-soft`): texto principal y regla superior de los módulos; `ink-soft` para texto secundario y metadatos.
- **Estado** (`ok`, `warn`, `bad`, `warn-wash`): veredictos de los ejercicios y niveles de habilidad (fortaleza, regular, a reforzar). Se usan en texto e iconos, no como fondos grandes.
- **Página pasada a limpio** (`code-bg`, `code-bar`, `code-rule`, `code-text`): los bloques de código son la única superficie oscura dentro de la página.

### Named Rules
**The Highlighter Rule.** El amarillo significa "siguiente" o "actual" y nada más. Si algo está resaltado y no es lo que toca, sobra el resaltador.

**The Ink Means Done Rule.** Un cuadrito relleno de `blue` es trabajo hecho; medio relleno en diagonal, en curso; resaltado, el siguiente; vacío, pendiente; borde rojo, con errores. Estos cinco estados son el vocabulario completo del progreso.

## Typography

**Display Font:** Bricolage Grotesque Variable (con Segoe UI)
**Body Font:** Inter Variable (con Segoe UI, system-ui), con `cv11` y `ss01`
**Label/Mono Font:** JetBrains Mono Variable (con Consolas, Menlo)

**Character:** Una grotesca con carácter de rotulador para títulos y cifras sobre una Inter tranquila que aguanta horas de lectura; el código va en una mono redonda y legible.

### Hierarchy
- **Display** (750, `clamp(1.9rem, 1.4rem + 1.6vw, 2.6rem)`, 1.15, -0.025em): título de cada página y del siguiente tema en el panel (máx. 22ch).
- **Figure** (700, 2.4rem, 1, -0.03em, tabular): cifras grandes de porcentaje, racha y horas; 1.9rem en cabeceras de sección, 2rem en móvil.
- **Headline** (700, 1.45rem, 1.15): títulos de módulo y de ejercicio (1.4rem).
- **Title** (700, 1.12rem, 1.15): subtítulos de lista y de bloque.
- **Body** (400, 15.5px, 1.6): interfaz general.
- **Reading** (400, 1.01rem, 1.7, máx. 64ch): teoría en Markdown dentro de la hoja con margen rojo.
- **Label** (600, 0.84rem): etiquetas de libro de cuentas, cabeceras de tabla (0.82rem), campos de formulario.
- **Mono** (0.9rem, 1.7): bloques de código, editor, esquema SQL, apuntes.

### Named Rules
**The Tabular Numbers Rule.** Toda cifra que mide avance (porcentajes, horas, aciertos, columnas de tabla) usa números tabulares para que las columnas se lean como un libro de cuentas.

**The Scale Contrast Rule.** La jerarquía sale del contraste de tamaño entre display y cuerpo, no de mayúsculas ni de color.

## Layout

Rejilla de dos columnas: barra lateral fija de 248 px (`rail`) a la izquierda, a toda altura y pegajosa, y una columna principal con página centrada de máx. 1120 px (860 px en la variante estrecha) y relleno de 36 px. Las secciones de página se separan 36 px.

Todo el espaciado sale del cuadro de 24 px (`cell`): fracciones y múltiplos 4, 8, 12, 16, 24, 36, 48, 72. En la hoja de ruta del panel, cada línea ocupa una fila de la cuadrícula y deja otra libre (doble espacio), y los cuadritos son celdas de 23 px alineadas con las líneas del papel; la columna de nombre mide 7 celdas y la de porcentaje 2.

La práctica usa una columna lateral pegajosa de 264 px (lista de ejercicios y esquema) junto al editor. Las filas de tema tienen columnas fijas: cuadrito (24 px), título, cuadritos de ejercicios, porcentaje (48 px).

Responsive: a 1080 px la página baja a 24 px de relleno y la práctica a 220 px. A 900 px la barra lateral se convierte en barra superior horizontal pegajosa (sin nombre de marca ni nota "Siguiente"), aparece la tira amarilla "Siguiente" bajo ella, todas las rejillas pasan a una columna y la hoja de ruta pone los cuadritos en una segunda fila. A 560 px la navegación apila icono sobre texto.

## Elevation & Depth

Plano por defecto. La profundidad se transmite con papel tonal (`paper`, `paper-2`, `sheet`), reglas finas y la regla superior de tinta de los módulos, nunca con sombras de tarjeta. Los estados usan anillos interiores (`inset 0 0 0 1-2px`) en lugar de elevación.

### Shadow Vocabulary
- **Etiqueta de la tapa** (`box-shadow: 0 18px 40px rgba(0, 0, 0, .35)`): solo la tarjeta de acceso sobre la tapa azul; es el único objeto levantado del sistema.
- **Halo de foco de campo** (`box-shadow: 0 0 0 3px var(--blue-wash)`): campos de texto, selectores y apuntes al enfocar.
- **Anillo de selección** (`box-shadow: inset 0 0 0 1px var(--blue)`): ruta actual, editor enfocado.

### Named Rules
**The Hairline Module Rule.** Un módulo empieza con una regla de tinta de 1 px y 16 px de aire; no se envuelve en una tarjeta con sombra.

## Shapes

Esquinas apenas suavizadas, como papel cortado: 6 px (`md`) para controles, paneles y bloques de código; 4 px para etiquetas y filas; 3 px para los cuadritos; 2 px para cuadritos pequeños y la marca. En la hoja de ruta los cuadritos pierden el radio y el borde para ser celdas exactas de la cuadrícula. El margen rojo es una doble línea vertical de 1 px separada 4 px, al 55 % de opacidad. Los bordes son siempre de 1 px (1.5 px en los cuadritos; 2 px en el subrayado de campos de acceso y huecos de dictado).

## Components

### Buttons
Tinta sobre papel: firmes, planos, sin degradados.
- **Shape:** esquinas suaves (6 px), altura mínima de 40 px (32 px en la variante pequeña y la de icono).
- **Primary:** relleno `blue` con texto blanco, 600 a 0.93rem, relleno horizontal de 16 px.
- **Hover / Focus:** el primario oscurece a `blue-hover`; el secundario oscurece el borde a `ink-soft`; al pulsar baja 1 px. Foco con contorno de 2 px `blue` desplazado 2 px.
- **Secondary:** hoja blanca con borde `rule-strong` y texto `ink`.
- **Ghost:** transparente con texto `blue`; al pasar, fondo `blue-wash`.
- **Disabled:** 45 % de opacidad.

### Chips
- **Style:** etiquetas pequeñas (0.8rem, 600) con fondo `paper-3` y radio de 4 px; variantes con resaltador amarillo (siguiente), verde (resuelto) y tinta azul (nivel, en display).
- **State:** como botón, la etiqueta actual queda en hoja blanca con borde y texto `blue`; como enlace, hover `blue-wash`.

### Cards / Containers
- **Corner Style:** 6 px.
- **Background:** `paper-2` en paneles y consola; hoja blanca en hoja de ruta, rutas y opciones.
- **Shadow Strategy:** ninguna (ver Elevation & Depth).
- **Border:** 1 px `rule`; la ruta actual añade un anillo interior `blue`.
- **Internal Padding:** 24 px en paneles, 16 px en elementos de ruta.
- **Libro de cuentas:** etiqueta arriba y valor en display debajo, entre reglas finas, en columnas automáticas de mín. 160 px.

### Inputs / Fields
- **Style:** hoja blanca, borde 1 px `rule-strong`, radio 6 px, 40 px de alto. En el acceso, el campo es papel `paper-2` con subrayado de 2 px `blue`. Los apuntes son un área mono con renglones de 28 px dibujados en `grid`.
- **Focus:** el borde pasa a `blue` con halo de 3 px `blue-wash`.
- **Error / Disabled:** errores en texto `bad`; las opciones de quiz incorrectas en `margin-wash` con borde `bad`, las correctas con borde `ok`.

### Navigation
La barra lateral es la tapa del cuaderno (`cover`). Marca arriba (cuatro cuadritos: uno relleno de tinta clara, otro resaltado), navegación con icono y texto en 600 a 0.95rem sobre `cover-muted`; hover en `cover-2`; el elemento activo se invierte a `cover-ink` con texto `cover` e icono `blue`. Al pie, la nota "Siguiente" con el título del siguiente tema resaltado, presente en todas las páginas. Las pestañas dentro de un tema son texto con subrayado de 2 px `blue` en la activa. En móvil la tapa es una barra superior y la nota se convierte en la tira amarilla bajo ella.

### Cuadritos (componente firma)
Cada tema o ejercicio es un cuadrito de 18 px (12 px pequeño, 24 px grande) con borde de 1.5 px y radio de 3 px, separados 3 px. Estados: vacío (borde `muted-cell`), completado (relleno `blue`), en curso (diagonal 135° mitad `blue`), siguiente (`hl-strong` con borde `ink`), con errores (borde `margin`). Los cuadritos enlazados crecen al 118 % con borde `blue` al pasar. Siempre llevan nombre accesible y leyenda cuando aparecen en grupo.

### Resaltador
El trazo amarillo se dibuja como un degradado de bordes irregulares que cubre el 78 % inferior de la línea y barre de izquierda a derecha una vez (0.9 s, `cubic-bezier(.16, 1, .3, 1)`, con 0.15 s de retraso). Variante verde para lo resuelto. Dentro de la nota de la barra lateral no se anima.

### Bloques de código
La página "pasada a limpio" en oscuro: fondo `code-bg`, barra de cabecera `code-bar` con el lenguaje en mono 0.74rem precedido de un cuadrito de color por lenguaje (amarillo Python, celeste SQL, verde bash), botón de copiar con borde fino. Resaltado de sintaxis propio en rosa, verde, ámbar, azul y turquesa claros.

## Do's and Don'ts

### Do:
- **Do** dibujar el avance con cuadritos y sus cinco estados (vacío, en curso, completado, siguiente, con errores).
- **Do** reservar el resaltador amarillo (`hl`, `hl-strong`, `hl-wash`) para lo siguiente o lo actual, y el verde (`hl-green`) para lo resuelto.
- **Do** separar módulos con una regla superior de 1 px `ink` y 16 px de aire.
- **Do** derivar todo espaciado del cuadro de 24 px (4, 8, 12, 16, 24, 36, 48, 72).
- **Do** usar números tabulares en toda cifra de avance y Bricolage Grotesque para las cifras grandes.
- **Do** poner la teoría en la hoja con margen rojo doble, a 1.01rem/1.7 y máx. 64ch.
- **Do** limitar el papel cuadriculado (`grid`, celda de 24 px) a las superficies donde se cuenta el avance.
- **Do** respetar `prefers-reduced-motion`: el barrido y las transiciones se anulan.

### Don't:
- **Don't** usar anillos de progreso, tarjetas de estadística del mismo tamaño ni el gris genérico de panel SaaS.
- **Don't** poner sombras en superficies de la página; la única elevación es la etiqueta de acceso sobre la tapa.
- **Don't** usar el amarillo, el verde o el rojo como decoración: cada uno tiene un significado de cuaderno.
- **Don't** añadir una segunda animación con autor; el barrido del resaltador es el único gesto.
- **Don't** cubrir de cuadrícula las hojas de lectura ni los formularios.
