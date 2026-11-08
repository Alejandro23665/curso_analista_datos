# Del dato a la conclusión: el proceso del análisis

Analizar datos no es abrir un archivo y "ver qué sale". Es responder una pregunta con evidencia, de forma que otra persona pueda
revisar tus pasos y llegar a lo mismo. Este capítulo es el mapa: qué pasos hay, en qué orden y qué errores se cometen en cada uno.
El resto del área (pandas, gráficos, estadística) son las herramientas de cada paso.

## 1. El ciclo completo

```
pregunta → datos → limpieza → exploración → análisis → conclusión → comunicación
    ↑                                                                  │
    └──────────────── casi siempre surge una pregunta nueva ───────────┘
```

No es una línea recta: al explorar descubres que faltan datos, al analizar descubres que la pregunta estaba mal planteada. Es normal
volver atrás. Lo que no es normal es saltarse pasos.

## 2. La pregunta: el paso que más se salta

Una buena pregunta de análisis tiene tres partes:

1. **Qué comparar o medir:** "vídeos con gancho en forma de pregunta frente al resto".
2. **Con qué métrica:** "retención a los 3 segundos".
3. **En qué población y periodo:** "mis vídeos de los últimos 60 días".

Y detrás, siempre, **una decisión**: "si los ganchos con pregunta retienen más, los usaré en la mitad de mis vídeos". Si ningún resultado
posible cambiaría lo que vas a hacer, el análisis sobra.

Las preguntas se suelen clasificar en cuatro tipos, de menor a mayor dificultad:

| Tipo | Pregunta | Ejemplo | Herramienta típica |
|---|---|---|---|
| **Descriptiva** | ¿Qué pasó? | ¿Cuántas ventas hubo por país en octubre? | Agregaciones, gráficos |
| **Diagnóstica** | ¿Por qué pasó? | ¿Por qué bajaron las ventas en Chile? | Segmentar, comparar, causalidad |
| **Predictiva** | ¿Qué pasará? | ¿Cuánto venderemos en diciembre? | Series de tiempo, regresión, ML |
| **Prescriptiva** | ¿Qué deberíamos hacer? | ¿A qué país dirigimos la publicidad? | Experimentos, optimización |

La mayor parte del trabajo real es descriptivo y diagnóstico. No subestimes lo descriptivo: un recuento bien hecho y bien presentado
resuelve muchas más decisiones que un modelo complicado.

## 3. Conocer los datos antes de tocarlos

### La unidad de análisis

Lo primero es saber **qué representa cada fila**: un pedido, un cliente, un día, un vídeo. Esa es la **granularidad** de la tabla.
Y la pregunta tiene la suya: "¿los clientes que compran más veces gastan más por pedido?" es una pregunta **sobre clientes**, así que
si la tabla tiene una fila por pedido, primero tienes que resumir cada cliente en una fila (número de pedidos, ticket medio) y después
comparar clientes.

Mezclar granularidades produce errores silenciosos. El más común es el **promedio de los promedios**: si una tienda tiene 100 pedidos de
10 USD de media y otra 10 pedidos de 50 USD, el ticket medio global no es (10 + 50) / 2 = 30, sino (100·10 + 10·50) / 110 ≈ 13,6. Cada
grupo tiene que pesar según su tamaño.

### Tipos de variables

El tipo de variable decide qué cálculos tienen sentido:

| Tipo | Ejemplos | Qué puedes calcular |
|---|---|---|
| **Nominal** (categorías sin orden) | país, tipo de publicación, canal | conteos, porcentajes, moda |
| **Ordinal** (categorías con orden) | nivel de satisfacción, talla S/M/L | lo anterior + mediana y percentiles |
| **Numérica discreta** (conteos) | número de pedidos, likes | todo, pero ojo con las medias de conteos pequeños |
| **Numérica continua** | precio, duración, temperatura | todo |

Trampas típicas: los códigos postales o los identificadores son números, pero son nominales (su media no significa nada). Y promediar
una escala ordinal ("Poco = 2, Bastante = 3") supone que la distancia entre respuestas es igual, algo que nadie ha comprobado: es
más honesto reportar el porcentaje de cada respuesta o la mediana.

### Preguntas que siempre hay que hacerle a un dataset

- ¿Quién lo generó, cómo y para qué? Un dato registrado para facturar no es igual que uno de una encuesta.
- ¿Qué periodo cubre? ¿Hay huecos?
- ¿Qué **no** está? Los clientes que nunca compraron, los vídeos que borraste, los usuarios que no respondieron la encuesta.
- ¿Cómo se define cada columna? "Usuario activo" puede significar cinco cosas distintas según el equipo.

## 4. Limpieza

Los datos reales vienen con vacíos, duplicados, formatos mezclados ("Mexico", "México", "MX"), valores imposibles (edad 250, precio
negativo) y fechas en zonas horarias distintas. Limpiar suele llevar más de la mitad del tiempo. Tres reglas:

1. **No borres sin entender.** Un valor extremo puede ser un error o tu cliente más importante.
2. **Documenta cada decisión** ("eliminé 37 pedidos de prueba con importe 0"). Si cambian los datos, sabrás rehacerlo.
3. **Cuenta antes y después.** Si un filtro o un *join* cambia el número de filas de forma inesperada, para y averigua por qué.

Los temas de pandas de este bloque te enseñan a hacerlo.

## 5. Exploración

Aquí miras los datos sin una hipótesis cerrada, para entenderlos: distribuciones de cada variable, relaciones entre pares, evolución
en el tiempo, diferencias entre segmentos. Las operaciones son siempre las mismas:

- **Agrupar y resumir:** por país, por mes, por tipo de contenido.
- **Comparar:** este grupo con aquel, este periodo con el anterior.
- **Mirar distribuciones, no solo promedios:** histograma, mediana, percentiles.

Un consejo práctico: en la exploración haz muchos gráficos rápidos y feos. Los gráficos cuidados son para comunicar, al final.

## 6. Tasas, no conteos: comparar con justicia

Comparar valores absolutos entre grupos de distinto tamaño casi siempre engaña:

- "México tiene más quejas que Uruguay" → claro, tiene más clientes. Compara **quejas por cada 1 000 clientes**.
- "La cuenta A tiene más vistas que la B" → si A tiene 2 millones de seguidores y B 4 000, compara **vistas por seguidor**.
- "Este vídeo tiene más likes" → compara la **tasa de interacción**: (likes + comentarios + compartidos) / vistas.

Toda tasa tiene un **numerador** y un **denominador**, y las discusiones sobre métricas casi siempre son sobre el denominador:
¿conversión sobre visitas o sobre usuarios? ¿interacción sobre vistas o sobre seguidores? Escríbelo siempre de forma explícita.

Y cuidado con las tasas sobre muy pocos casos: un vídeo con 2 likes de 2 vistas tiene una tasa del 100 % que no significa nada. En el
tema de estadística bayesiana verás cómo ordenar rankings sin que ganen los casos con pocos datos.

## 7. Análisis y conclusión

El análisis es la parte formal: calcular la diferencia entre grupos con su incertidumbre, ajustar un modelo, hacer una prueba. Antes de
escribir la conclusión, desconfía de tu resultado:

- **¿Es ruido?** Con pocos datos, las diferencias aparecen y desaparecen solas. Para eso sirven los intervalos y las pruebas.
- **¿Hay otra explicación?** Un confusor, un sesgo de selección, la estacionalidad, un cambio en cómo se registran los datos.
- **¿Se sostiene si cambio algo razonable?** Otro periodo, otro segmento, sin los valores extremos. Si la conclusión desaparece, era frágil.

Una conclusión útil tiene tres partes: **qué encontraste, con cuánta seguridad y qué harías**.

> "Los vídeos con gancho en forma de pregunta retuvieron un 22 % más a los 3 segundos (32 vídeos de cada tipo, intervalo del 95 %:
> de +8 % a +36 %). Propongo usar ese gancho en la mitad de los vídeos del próximo mes y medir de nuevo."

## 8. Reproducibilidad

Si dentro de un mes no puedes repetir tu análisis, no vale mucho. Trabaja con scripts o *notebooks* que vayan del dato crudo al
resultado sin pasos a mano, guarda la versión de los datos que usaste y fija las semillas aleatorias. Además de evitar errores, te
permite actualizar el análisis cuando lleguen datos nuevos en minutos.

## 9. Dónde conseguir datos

- **Para practicar:** Kaggle (miles de datasets y análisis de otras personas; revisa siempre su origen), Google Dataset Search, el
  repositorio UCI y Hugging Face Datasets (sobre todo texto).
- **Datos públicos del mundo real:** Our World in Data, Banco Mundial, CEPAL y los portales de datos abiertos de cada gobierno.
- **Tendencias y redes:** Google Trends (interés de búsqueda relativo, 0 a 100), TikTok Creative Center (hashtags, canciones y anuncios
  en tendencia) y, sobre todo, **tus propias estadísticas** de Instagram y TikTok: son los datos de tu audiencia.
- **Datos que construyes tú:** una hoja de cálculo en la que registras cada vídeo con sus características (duración, tipo de gancho,
  tema), una encuesta, los datos de un cliente. Muchas veces el dataset que necesitas no existe y hay que crearlo.

Sobre las redes, dos avisos. TikTok e Instagram no dan sus datos libremente (TikTok tiene una API de investigación solo para académicos
y el *scraping* masivo va contra sus condiciones). Y si recopilas solo vídeos virales caes en el **sesgo de supervivencia**: para saber
qué hace viral a un vídeo necesitas también los que no lo fueron. Lo verás a fondo en el tema de causalidad.

## Resumen

- Empieza por una pregunta concreta ligada a una decisión.
- Entiende qué es cada fila, qué tipo es cada variable y qué falta en los datos.
- Limpia documentando cada decisión y contando filas antes y después.
- Compara tasas, no conteos, y pondera cuando juntes grupos.
- Antes de concluir, busca el ruido, la explicación alternativa y la fragilidad.
- Concluye con qué encontraste, con cuánta seguridad y qué harías.
