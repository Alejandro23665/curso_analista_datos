# Elegir y aplicar la prueba estadística correcta

En el tema de A/B testing viste la lógica de una prueba de hipótesis con el caso más común: comparar dos proporciones con una prueba z.
Pero los datos reales traen otras preguntas: comparar medias (tiempos, importes), comparar más de dos grupos, cruzar dos variables
categóricas, medir a las mismas personas dos veces. Este capítulo es la caja de herramientas completa y, sobre todo, **cómo elegir**.

## 1. Repaso en un minuto

Toda prueba sigue el mismo esquema:

1. **Hipótesis nula (H₀):** no hay diferencia o no hay relación. Es lo que intentas refutar.
2. **Estadístico de prueba:** un número que mide cuánto se alejan tus datos de lo que esperarías si H₀ fuera cierta, normalmente en
   unidades de "errores estándar".
3. **Valor p:** la probabilidad de ver un estadístico **al menos tan extremo** como el tuyo **si H₀ fuera cierta**.
4. **Decisión:** si p < α (normalmente 0,05), rechazas H₀. Si no, **no** has demostrado que no haya efecto: solo que tus datos no
   bastan para distinguirlo del azar.

Lo que cambia de una prueba a otra es el estadístico y la distribución con la que se compara. La lógica es siempre la misma.

## 2. Comparar medias: la familia t

### Por qué t y no z

Para comparar medias necesitas la desviación de la población, que no conoces: la estimas con la muestra. Esa estimación añade
incertidumbre, sobre todo con muestras pequeñas. La **distribución t de Student** es como una normal con colas más gruesas que tiene
en cuenta ese extra. Depende de los **grados de libertad** (aproximadamente, el tamaño de la muestra menos lo que estimas): con pocos
datos sus colas son gruesas; a partir de unas 30 observaciones es casi idéntica a la normal.

### t de una muestra

¿La media de un grupo es distinta de un valor de referencia? "¿El tiempo medio de respuesta de mi chatbot supera los 2 segundos
prometidos?".

```
t = (media − valor_referencia) / (s / √n)
```

### t para dos grupos independientes: usa la de Welch

¿Las medias de dos grupos distintos difieren? "¿Los clientes que llegan por Instagram gastan más por pedido que los de Google?".

```
t = (media_A − media_B) / √(s_A² / n_A + s_B² / n_B)
```

Existe una versión clásica que supone que los dos grupos tienen la misma varianza. En la práctica casi nunca lo sabes, y la versión de
**Welch** (la fórmula de arriba) funciona bien en ambos casos. Úsala por defecto: en `scipy`, `ttest_ind(a, b, equal_var=False)`.

### t pareada: las mismas unidades medidas dos veces

Si mides a **los mismos** usuarios antes y después, o cada producto en dos tiendas, las observaciones de los dos grupos no son
independientes. Se calcula la **diferencia de cada par** y se hace una t de una muestra sobre esas diferencias contra 0.

Esto tiene una ventaja enorme: elimina la variación **entre** personas (unas son rápidas y otras lentas) y deja solo el cambio. Con
los mismos datos, la prueba pareada suele detectar efectos que la de dos grupos no ve. Usar una prueba de grupos independientes con
datos pareados es un error frecuente que hace perder casi toda la potencia.

### Supuestos de las pruebas t

- **Independencia** entre observaciones (o entre pares, en la pareada). Es el supuesto más importante y el que más se viola: varias
  filas del mismo usuario, días consecutivos de una serie...
- **Normalidad de la media**, no de los datos. Gracias al teorema central del límite, con muestras moderadas (30 o más por grupo) suele
  bastar, salvo con colas muy largas (vistas, ingresos), donde hacen falta muchas más observaciones o una transformación logarítmica.

## 3. Más de dos grupos: ANOVA

Si comparas cuatro tipos de contenido, la tentación es hacer seis pruebas t (todas las parejas). Eso infla los falsos positivos (lo
verás en la sección 6). El **ANOVA de un factor** responde primero a una pregunta global: "¿hay **alguna** diferencia entre las medias?".

La idea: compara la variación **entre** las medias de los grupos con la variación **dentro** de cada grupo.

```
F = variación entre grupos / variación dentro de los grupos
```

Si las medias de los grupos se separan mucho más de lo que varían los datos dentro de cada grupo, F es grande y el valor p pequeño.

Un ANOVA significativo solo dice "algún grupo difiere", no cuál. Para saberlo se hacen comparaciones **post hoc** que controlan los
falsos positivos (la prueba de Tukey es la más usada). En `scipy`: `f_oneway(g1, g2, g3)`; Tukey en `statsmodels` o en
`scipy.stats.tukey_hsd`.

## 4. Variables categóricas: chi-cuadrado

Para dos variables **categóricas** ("tipo de publicación" y "consiguió algún seguidor: sí/no") se construye una **tabla de
contingencia** con los conteos de cada combinación:

| | Consiguió seguidor | No consiguió |
|---|---|---|
| Vídeo | 30 | 10 |
| Carrusel | 10 | 30 |

Si las variables fueran independientes, cada celda tendría un conteo **esperado**:

```
esperado = (total de la fila × total de la columna) / total general
```

El estadístico mide la distancia total entre lo observado y lo esperado:

```
χ² = Σ (observado − esperado)² / esperado
```

Cuanto mayor, menos compatible con la independencia. Se compara con la distribución chi-cuadrado con `(filas − 1) × (columnas − 1)`
grados de libertad. En `scipy`: `chi2_contingency(tabla)`, que devuelve el estadístico, el valor p y los esperados.

Condición: los conteos **esperados** no deberían ser muy pequeños (regla habitual: al menos 5 en cada celda). Con tablas 2×2 y pocos
datos se usa la **prueba exacta de Fisher** (`fisher_exact`).

La prueba z de dos proporciones del tema de A/B testing es, de hecho, equivalente a un chi-cuadrado sobre una tabla 2×2.

## 5. Cuando los supuestos no se cumplen

### Pruebas no paramétricas

Trabajan con los **rangos** (el orden de los datos) en lugar de los valores, así que no les afectan los extremos ni la forma de la
distribución:

| En lugar de... | Usa... | En `scipy` |
|---|---|---|
| t de dos grupos | Mann-Whitney U | `mannwhitneyu` |
| t pareada | Wilcoxon de rangos con signo | `wilcoxon` |
| ANOVA | Kruskal-Wallis | `kruskal` |

Ojo: no comparan exactamente medias, sino si los valores de un grupo tienden a ser mayores que los del otro. Para datos con colas
largas suele ser justo la pregunta que interesa.

### Pruebas de permutación: la idea más versátil

Si H₀ es cierta y el grupo no importa, las etiquetas "A" y "B" son intercambiables. Entonces:

1. Calcula la diferencia observada entre los grupos.
2. Junta todos los datos, **baraja** las etiquetas al azar y recalcula la diferencia. Repite miles de veces.
3. El valor p es la proporción de barajados con una diferencia al menos tan grande como la observada.

No necesita fórmulas ni supuestos de normalidad, y sirve para **cualquier** estadístico: diferencia de medianas, de percentiles 90,
de tasas. Solo exige que, bajo H₀, las etiquetas sean intercambiables (por ejemplo, que la asignación haya sido al azar). La
programarás en los ejercicios; en `scipy` existe `permutation_test`.

El **bootstrap** que viste en inferencia es su pariente: el bootstrap remuestrea para estimar **intervalos**; la permutación baraja
para calcular **valores p**.

## 6. Comparaciones múltiples: el error que más engaña

Con α = 0,05, cada prueba sin efecto real tiene un 5 % de probabilidad de salir "significativa". Si haces muchas:

```
P(al menos un falso positivo) = 1 − (1 − α)^k
```

Con 20 pruebas independientes sin ningún efecto real, la probabilidad de "encontrar algo" es del 64 %. Pasa cuando:

- Miras 20 métricas en un A/B test y celebras la única que salió significativa.
- Segmentas por país, dispositivo, edad y canal hasta que algún subgrupo "funciona".
- Pruebas 15 variantes de un anuncio y te quedas con la ganadora sin volver a probarla.

Soluciones:

- **Bonferroni:** usa α / k en cada prueba. Simple y conservador (con muchas pruebas pierde potencia).
- **Holm:** una versión escalonada de Bonferroni, igual de segura y con algo más de potencia.
- **Benjamini-Hochberg (FDR):** controla la **proporción** de falsos descubrimientos entre los resultados significativos. Es la
  opción habitual cuando exploras muchas hipótesis.
- **Definir de antemano una métrica principal** y tratar el resto como exploratorias que habrá que confirmar.

En `statsmodels`: `multipletests(pvalores, method="holm")` o `method="fdr_bh"`.

### El jardín de los senderos que se bifurcan

Hay una versión más sutil: aunque solo hagas una prueba, si **decides cómo analizar después de ver los datos** (qué outliers quitar,
qué periodo usar, qué segmento mirar), estás eligiendo implícitamente entre muchos análisis posibles. Es el *p-hacking*, muchas veces
involuntario. La defensa es decidir el análisis **antes** de ver los resultados y, cuando eso no es posible, confirmar el hallazgo con
datos nuevos.

## 7. Tamaño del efecto: lo que de verdad importa

El valor p mezcla dos cosas: el tamaño del efecto y el tamaño de la muestra. Con millones de usuarios, una diferencia ridícula sale
significativa; con 20, una diferencia enorme puede no salir. Por eso **informa siempre del tamaño del efecto**, idealmente con su
intervalo de confianza:

- **En unidades originales** (lo más útil para decidir): "los clientes de Instagram gastan 4,20 USD más por pedido (IC 95 %: 1,10 a 7,30)".
- **Estandarizado**, para comparar estudios o métricas distintas: la **d de Cohen**:

```
d = (media_A − media_B) / desviación_combinada
```

Como referencia orientativa: d ≈ 0,2 es pequeño, 0,5 mediano y 0,8 grande. Pero "pequeño" puede valer millones si afecta a mucha
gente, y "grande" puede ser irrelevante si cuesta más de lo que aporta. La importancia la decide el negocio, no la tabla.

Para el chi-cuadrado, la medida habitual es la **V de Cramér** (de 0 a 1); para proporciones, la diferencia absoluta y la relativa.

## 8. Potencia: ¿tu estudio podía encontrar algo?

La **potencia** es la probabilidad de detectar un efecto **si existe**. Depende de cuatro cosas relacionadas: el tamaño del efecto, el
tamaño de la muestra, la variabilidad de los datos y α. Se suele buscar un 80 %.

Su consecuencia más importante: **un resultado no significativo con poca potencia no dice nada**. "Probamos los ganchos con pregunta
con 8 vídeos y no hubo diferencia significativa" no significa que no funcionen: con 8 vídeos casi nada sale significativo.

Calcula el tamaño de muestra **antes** de empezar (lo hiciste para proporciones en el tema de A/B testing; para medias, en
`statsmodels`: `TTestIndPower().solve_power(effect_size=0.3, alpha=0.05, power=0.8)`).

## 9. Cómo elegir la prueba

| Pregunta | Datos | Prueba | Alternativa robusta |
|---|---|---|---|
| ¿Una media difiere de un valor? | 1 grupo numérico | t de una muestra | Wilcoxon / bootstrap |
| ¿Difieren dos medias? | 2 grupos independientes | t de Welch | Mann-Whitney / permutación |
| ¿Cambió algo en las mismas unidades? | 2 medidas pareadas | t pareada | Wilcoxon |
| ¿Difieren 3 o más medias? | 3+ grupos | ANOVA + Tukey | Kruskal-Wallis |
| ¿Difieren dos proporciones? | 2 grupos sí/no | z de proporciones | Fisher (pocos datos) |
| ¿Dos categóricas están relacionadas? | Tabla de contingencia | Chi-cuadrado | Fisher |
| ¿Dos numéricas están relacionadas? | 2 variables numéricas | Correlación / regresión | Spearman |

Y tres preguntas antes de la tabla:

1. **¿Las observaciones son independientes?** Si no, la prueba elegida está mal desde el principio (pareada, datos agrupados,
   series de tiempo).
2. **¿Qué quiero comparar exactamente?** Medias, medianas, proporciones, distribuciones enteras.
3. **¿Hay colas largas o extremos?** Si los hay, transforma (logaritmos) o usa una alternativa robusta.

## 10. Cómo informar un resultado

Una buena línea de resultado incluye: la prueba, el tamaño del efecto con su intervalo, el valor p y el tamaño de muestra.

> "Los vídeos con subtítulos retuvieron de media 3,1 segundos más (IC 95 %: 0,9 a 5,3; t de Welch, p = 0,006; 41 y 38 vídeos)."

Y en la conclusión, la traducción a lenguaje de negocio, sin la jerga.

## Resumen

- La lógica es siempre la misma; cambian el estadístico y la distribución de referencia.
- Medias: t de Welch para grupos independientes, pareada para las mismas unidades, ANOVA para tres o más.
- Categóricas: chi-cuadrado (Fisher con pocos datos).
- Si no se cumplen los supuestos: no paramétricas o permutación.
- Muchas pruebas inflan los falsos positivos: corrige o define una métrica principal.
- Informa el tamaño del efecto con su intervalo, y calcula la potencia antes de empezar.
