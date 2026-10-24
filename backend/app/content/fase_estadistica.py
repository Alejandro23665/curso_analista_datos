from ._helpers import checklist, py, quiz

TOPICS = [
    {
        "slug": "estadistica",
        "phase": "estadistica",
        "title": "Estadística descriptiva y distribuciones",
        "summary": "Centro, dispersión, percentiles, forma de una distribución, la normal, puntuaciones z y valores atípicos.",
        "hours": 8,
        "theory": r"""
# Estadística descriptiva y distribuciones

La estadística descriptiva **resume** muchos datos en pocos números y gráficos. Es lo primero que haces con cualquier dataset y
lo que más usarás en el día a día como analista.

## 1. Medidas de centro: ¿cuál es el valor "típico"?

| Medida | Qué es | Cuándo usarla |
|---|---|---|
| **Media** | Suma / cantidad | Datos simétricos y sin valores extremos |
| **Mediana** | El valor del medio al ordenar | Ingresos, precios, tiempos (distribuciones sesgadas) |
| **Moda** | El valor más frecuente | Variables categóricas |

Ejemplo: sueldos `[1000, 1100, 1200, 1300, 50000]`. La media es 10 920 y la mediana 1200. **La media se deja arrastrar por los extremos;
la mediana no.** Si alguien te da un promedio de ingresos, pregunta por la mediana.

## 2. Medidas de dispersión: ¿cuánto varían los datos?

- **Rango:** máximo − mínimo. Muy sensible a extremos.
- **Varianza y desviación estándar:** distancia típica de los datos a la media. La desviación está en las mismas unidades que los datos.
  La versión **muestral** divide entre `n − 1` (es la que usa `df["x"].std()` en pandas).
- **Percentiles:** el percentil 90 (p90) es el valor por debajo del cual está el 90 % de los datos. En tecnología se usa mucho: "el p95 del tiempo de respuesta es 800 ms".
- **Rango intercuartílico (IQR):** `Q3 − Q1`, el ancho del 50 % central. Es robusto frente a extremos.

Dos grupos pueden tener **la misma media y ser muy distintos**: reporta siempre centro **y** dispersión.

## 3. La forma de una distribución

Míralo con un **histograma** o un **boxplot** antes de calcular nada.

- **Simétrica:** media ≈ mediana.
- **Sesgada a la derecha** (cola larga hacia valores altos: ingresos, precios de viviendas): media > mediana.
- **Sesgada a la izquierda:** media < mediana.
- **Bimodal:** dos picos. Suele indicar que mezclas dos grupos distintos (por ejemplo, clientes minoristas y empresas): sepáralos.

## 4. La distribución normal

La famosa "campana". Muchas cosas se aproximan a ella (alturas, errores de medición, promedios de muestras grandes). La **regla 68-95-99,7**:

- ≈ 68 % de los datos está a menos de 1 desviación de la media,
- ≈ 95 % a menos de 2,
- ≈ 99,7 % a menos de 3.

**Ojo:** muchos datos de negocio **no** son normales (ventas, tiempos de espera, ingresos). No asumas normalidad sin mirar el histograma.

## 5. Puntuaciones z: comparar en una misma escala

`z = (valor − media) / desviación`. Dice a cuántas desviaciones está un dato de la media. Una z de 2,5 es un valor inusual.
Sirve para comparar variables en escalas distintas.

## 6. Valores atípicos (outliers)

Regla del IQR: es atípico lo que queda fuera de `[Q1 − 1,5·IQR, Q3 + 1,5·IQR]`. Un atípico puede ser un **error** (edad 250) o un **caso real
importante** (un cliente que compra 100 veces más). **Investiga antes de borrar.**

En Python: `statistics.mean`, `statistics.median`, `statistics.stdev` (muestral), `statistics.quantiles(datos, n=4)` (cuartiles); en pandas: `describe()`, `quantile()`.

## Cómo sabes que dominas este tema

- Eliges media o mediana con criterio y lo justificas.
- Describes la forma de una distribución mirando su histograma.
- Calculas puntuaciones z y detectas atípicos con el IQR.
""",
        "exercises": [
            py("est-media", "Media y mediana", "Estadística: descriptiva",
               "Escribe `media_mediana(valores)` que devuelva una tupla `(media, mediana)` de una lista de números "
               "(sin usar librerías externas; la mediana de una cantidad par de valores es el promedio de los dos centrales).",
               starter="""
def media_mediana(valores):
    # tu código aquí
    pass
""",
               solution="""
def media_mediana(valores):
    ordenados = sorted(valores)
    n = len(ordenados)
    media = sum(ordenados) / n
    medio = n // 2
    mediana = ordenados[medio] if n % 2 else (ordenados[medio - 1] + ordenados[medio]) / 2
    return media, mediana
""",
               tests="""
assert media_mediana([1, 2, 3]) == (2.0, 2), "Para [1, 2, 3] esperaba (2.0, 2)"
assert media_mediana([4, 1, 3, 2]) == (2.5, 2.5), "Para una cantidad par, la mediana es el promedio de los dos centrales"
media, mediana = media_mediana([1000, 1100, 1200, 1300, 50000])
assert mediana == 1200 and media == 10920
""",
               hint="Ordena la lista; si n es impar la mediana es ordenados[n // 2]."),
            py("est-std", "Desviación estándar muestral", "Estadística: descriptiva",
               "Escribe `desviacion_muestral(valores)` que calcule la desviación estándar **muestral** (divide entre `n - 1`).",
               starter="""
def desviacion_muestral(valores):
    # tu código aquí
    pass
""",
               solution="""
def desviacion_muestral(valores):
    n = len(valores)
    media = sum(valores) / n
    varianza = sum((v - media) ** 2 for v in valores) / (n - 1)
    return varianza ** 0.5
""",
               tests="""
res = desviacion_muestral([2, 4, 4, 4, 5, 5, 7, 9])
assert abs(res - 2.13809) < 1e-4, "Para [2,4,4,4,5,5,7,9] esperaba ~2.1381 (muestral) y obtuve %r" % res
assert abs(desviacion_muestral([1, 3]) - 1.41421) < 1e-4
""",
               hint="varianza = suma((x - media)^2) / (n - 1); desviación = raíz de la varianza."),
            py("est-z", "Puntuaciones z", "Estadística: descriptiva",
               "Escribe `puntuaciones_z(valores)` que devuelva una lista con la puntuación z de cada valor: `(valor - media) / desviacion_muestral`. "
               "Puedes usar `statistics.mean` y `statistics.stdev`.",
               starter="""
import statistics

def puntuaciones_z(valores):
    # tu código aquí
    pass
""",
               solution="""
import statistics

def puntuaciones_z(valores):
    media = statistics.mean(valores)
    desviacion = statistics.stdev(valores)
    return [(v - media) / desviacion for v in valores]
""",
               tests="""
res = puntuaciones_z([2, 4, 6])
assert [round(z, 6) for z in res] == [-1.0, 0.0, 1.0], "Media 4 y desviacion 2 -> [-1, 0, 1]; obtuve %r" % (res,)
res = puntuaciones_z([10, 10, 10, 30])
assert abs(res[-1] - 1.5) < 1e-9, "El 30 esta a 1.5 desviaciones de la media"
"""),
            py("est-atipicos", "Atípicos con el IQR", "Estadística: descriptiva",
               "Escribe `atipicos_iqr(valores)` que devuelva, ordenados, los valores fuera de `[Q1 - 1.5*IQR, Q3 + 1.5*IQR]`. "
               "Calcula los cuartiles con `statistics.quantiles(valores, n=4)`, que devuelve `[Q1, Q2, Q3]`.",
               starter="""
import statistics

def atipicos_iqr(valores):
    # tu código aquí
    pass
""",
               solution="""
import statistics

def atipicos_iqr(valores):
    q1, _, q3 = statistics.quantiles(valores, n=4)
    iqr = q3 - q1
    inferior, superior = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    return sorted(v for v in valores if v < inferior or v > superior)
""",
               tests="""
assert atipicos_iqr([1, 2, 3, 4, 5, 6, 7, 8, 9, 100]) == [100], "Solo el 100 es atipico"
assert atipicos_iqr([10, 11, 12, 13, 14, 15]) == [], "Sin atipicos debe devolver []"
assert atipicos_iqr([-80, 10, 11, 12, 13, 14, 15, 90]) == [-80, 90], "Detecta extremos por ambos lados, ordenados"
"""),
            quiz("est-quiz-media", "Media o mediana", "Estadística: descriptiva",
                 "Analizas los salarios de una empresa donde el director gana 100 veces más que el resto. ¿Qué medida resume mejor el salario 'típico'?",
                 ["La media", "La mediana", "El máximo", "La suma"], 1,
                 "La mediana no se ve afectada por valores extremos; la media se arrastra hacia ellos."),
            quiz("est-quiz-normal", "Regla 68-95-99,7", "Estadística: descriptiva",
                 "Los tiempos de entrega siguen aproximadamente una normal con media 40 min y desviación 5 min. ¿Qué porcentaje de entregas tarda entre 30 y 50 minutos?",
                 ["≈ 68 %", "≈ 95 %", "≈ 99,7 %", "≈ 50 %"], 1,
                 "30 y 50 están a 2 desviaciones de la media (40 ± 2·5). En una normal, ≈ 95 % de los datos cae en ese rango."),
            quiz("est-quiz-sesgo", "Forma de la distribución", "Estadística: descriptiva",
                 "En un dataset de precios de viviendas la media es 180 000 y la mediana 120 000. ¿Qué indica?",
                 ["Distribución simétrica", "Sesgo a la derecha: unas pocas viviendas muy caras elevan la media", "Sesgo a la izquierda", "Que hay un error de cálculo"], 1,
                 "Cuando la media supera claramente a la mediana, hay una cola larga de valores altos (sesgo a la derecha)."),
        ],
    },
    {
        "slug": "est-probabilidad",
        "phase": "estadistica",
        "title": "Probabilidad para analistas",
        "summary": "Probabilidad condicional, independencia, el teorema de Bayes, valor esperado y simulación.",
        "hours": 8,
        "theory": r"""
# Probabilidad para analistas

No necesitas resolver problemas de urnas y bolas. Necesitas **razonar con incertidumbre** y no caer en los errores de intuición más comunes.

## 1. Lo básico

- Una probabilidad va de 0 (imposible) a 1 (seguro). En datos, casi siempre se **estima** con frecuencias: `casos favorables / casos totales`.
- **Complemento:** `P(no A) = 1 − P(A)`. "La probabilidad de que al menos uno falle" suele ser más fácil como `1 − P(ninguno falla)`.
- **A y B** (ambos): si son independientes, `P(A y B) = P(A) · P(B)`.
- **A o B** (al menos uno): `P(A o B) = P(A) + P(B) − P(A y B)`.

## 2. Probabilidad condicional: la más útil

`P(A | B)` se lee "probabilidad de A **dado** B": la probabilidad de A **solo entre los casos donde ocurre B**.

```
P(compra | llegó por la app) = compras desde la app / visitas desde la app
```

Casi toda métrica de negocio segmentada es una probabilidad condicional: la tasa de conversión **de** un canal, la tasa de cancelación **de** un plan...

**Cuidado:** `P(A | B)` no es lo mismo que `P(B | A)`. La probabilidad de que un fraude dispare una alerta no es la probabilidad de que una alerta sea fraude.

## 3. Independencia

A y B son independientes si saber B no cambia la probabilidad de A: `P(A | B) = P(A)`. Las monedas y los dados no tienen memoria:
tras 5 caras seguidas, la siguiente sigue siendo 50 % (creer lo contrario es la **falacia del jugador**).

## 4. Teorema de Bayes y la tasa base

```
P(A | B) = P(B | A) · P(A) / P(B)
```

Ejemplo clásico: una enfermedad afecta al 1 % de la población. Una prueba detecta al 99 % de los enfermos y da falso positivo en el 5 % de los sanos.
Si alguien da positivo, ¿qué probabilidad hay de que esté enfermo?

- Enfermos que dan positivo: 0,01 × 0,99 = 0,0099
- Sanos que dan positivo: 0,99 × 0,05 = 0,0495
- P(enfermo | positivo) = 0,0099 / (0,0099 + 0,0495) ≈ **17 %**

¡No 99 %! Cuando el evento es raro, **la mayoría de positivos son falsos**. Ignorar la tasa base es uno de los errores más caros en
modelos de fraude, alertas de seguridad o detección de anomalías.

## 5. Valor esperado

El promedio ponderado de los resultados posibles: `E = Σ valor × probabilidad`.
Una campaña que cuesta 10 USD por cliente y genera 200 USD con probabilidad 0,08 tiene un valor esperado de `0,08 × 200 − 10 = 6` USD por cliente: vale la pena.

## 6. Simular cuando la fórmula es difícil

Con Python puedes **simular** miles de veces un proceso aleatorio y contar (método de Monte Carlo). Usa una **semilla** (`random.Random(42)`)
para que el resultado sea reproducible.

## Cómo sabes que dominas este tema

- Traduces "tasa de X en el segmento Y" a una probabilidad condicional.
- Explicas por qué una prueba muy precisa puede dar mayoría de falsos positivos.
- Calculas un valor esperado para decidir si una acción conviene.
""",
        "exercises": [
            py("prob-condicional", "Conversión de un canal", "Estadística: probabilidad",
               "Escribe `prob_compra_dado_canal(visitas, canal)`. `visitas` es una lista de tuplas `(canal, compro)`, donde `compro` es `True` o `False`. "
               "Devuelve la probabilidad de compra **entre las visitas de ese canal**. Si no hay visitas del canal, devuelve `0.0`.",
               starter="""
def prob_compra_dado_canal(visitas, canal):
    # tu código aquí
    pass
""",
               solution="""
def prob_compra_dado_canal(visitas, canal):
    del_canal = [compro for c, compro in visitas if c == canal]
    if not del_canal:
        return 0.0
    return sum(del_canal) / len(del_canal)
""",
               tests="""
visitas = [("app", True), ("app", False), ("web", False), ("app", True), ("web", True), ("app", False)]
assert prob_compra_dado_canal(visitas, "app") == 0.5, "En la app compran 2 de 4 visitas"
assert prob_compra_dado_canal(visitas, "web") == 0.5
assert prob_compra_dado_canal(visitas, "tienda") == 0.0, "Sin visitas del canal debe devolver 0.0"
""",
               hint="Filtra primero las visitas del canal; luego cuenta cuántas compraron. sum() de booleanos cuenta los True."),
            py("prob-bayes", "Teorema de Bayes", "Estadística: probabilidad",
               "Escribe `prob_real_dado_positivo(prevalencia, sensibilidad, tasa_falsos_positivos)` que devuelva la probabilidad de que un caso sea realmente positivo "
               "dado que la prueba dio positivo: `sensibilidad·prevalencia / (sensibilidad·prevalencia + tasa_falsos_positivos·(1 − prevalencia))`.",
               starter="""
def prob_real_dado_positivo(prevalencia, sensibilidad, tasa_falsos_positivos):
    # tu código aquí
    pass
""",
               solution="""
def prob_real_dado_positivo(prevalencia, sensibilidad, tasa_falsos_positivos):
    verdaderos = sensibilidad * prevalencia
    falsos = tasa_falsos_positivos * (1 - prevalencia)
    return verdaderos / (verdaderos + falsos)
""",
               tests="""
res = prob_real_dado_positivo(0.01, 0.99, 0.05)
assert abs(res - 0.16667) < 1e-4, "Con 1%% de prevalencia deberia salir ~0.1667, obtuve %r" % res
assert abs(prob_real_dado_positivo(0.5, 0.9, 0.1) - 0.9) < 1e-9, "Con 50% de prevalencia el resultado es 0.9"
"""),
            py("prob-esperado", "Valor esperado", "Estadística: probabilidad",
               "Escribe `valor_esperado(resultados)`. `resultados` es una lista de tuplas `(valor, probabilidad)`. Devuelve la suma de `valor * probabilidad`. "
               "Si las probabilidades no suman 1 (con tolerancia de `1e-9`), lanza `ValueError`.",
               starter="""
def valor_esperado(resultados):
    # tu código aquí
    pass
""",
               solution="""
def valor_esperado(resultados):
    if abs(sum(p for _, p in resultados) - 1) > 1e-9:
        raise ValueError("Las probabilidades deben sumar 1")
    return sum(valor * p for valor, p in resultados)
""",
               tests="""
assert abs(valor_esperado([(190, 0.08), (-10, 0.92)]) - 6.0) < 1e-9, "0.08*190 + 0.92*(-10) = 6"
assert valor_esperado([(1, 0.5), (0, 0.5)]) == 0.5
try:
    valor_esperado([(1, 0.5), (0, 0.4)])
except ValueError:
    pass
else:
    raise AssertionError("Si las probabilidades no suman 1 debe lanzar ValueError")
"""),
            py("prob-simulacion", "Simular dos dados", "Estadística: probabilidad",
               "Escribe `simular_suma_siete(n, semilla=42)` que lance dos dados `n` veces con `random.Random(semilla)` (usa `rng.randint(1, 6)`) "
               "y devuelva la proporción de lanzamientos cuya suma es 7. Con muchas repeticiones debe acercarse a 1/6.",
               starter="""
import random

def simular_suma_siete(n, semilla=42):
    rng = random.Random(semilla)
    # tu código aquí
    pass
""",
               solution="""
import random

def simular_suma_siete(n, semilla=42):
    rng = random.Random(semilla)
    sietes = 0
    for _ in range(n):
        if rng.randint(1, 6) + rng.randint(1, 6) == 7:
            sietes += 1
    return sietes / n
""",
               tests="""
res = simular_suma_siete(60000)
assert abs(res - 1 / 6) < 0.01, "Con 60000 lanzamientos deberia acercarse a 0.1667, obtuve %r" % res
assert simular_suma_siete(1000, 7) == simular_suma_siete(1000, 7), "Con la misma semilla el resultado debe repetirse"
"""),
            quiz("prob-quiz-base", "La tasa base", "Estadística: probabilidad",
                 "Un modelo detecta el 95 % de los fraudes y marca por error al 2 % de las transacciones legítimas. Solo el 0,1 % de las transacciones son fraude. "
                 "Si una transacción es marcada, ¿qué es más probable?",
                 ["Que sea fraude, porque el modelo acierta el 95 %", "Que sea legítima: con un fraude tan raro, la mayoría de alertas son falsos positivos",
                  "Exactamente 50 % y 50 %", "No se puede razonar sin más datos"], 1,
                 "Con 0,1 % de fraude, por cada fraude detectado (0,00095) hay unas 0,02 alertas falsas. Más del 95 % de las alertas son legítimas."),
            quiz("prob-quiz-jugador", "Independencia", "Estadística: probabilidad",
                 "Una moneda justa salió cara 6 veces seguidas. ¿Qué probabilidad hay de que la siguiente sea cruz?",
                 ["Más del 50 %, porque 'le toca'", "Exactamente 50 %", "Menos del 50 %", "1 / 64"], 1,
                 "Los lanzamientos son independientes: la moneda no recuerda los resultados anteriores. Pensar que 'le toca' es la falacia del jugador."),
            quiz("prob-quiz-condicional", "Condicional al revés", "Estadística: probabilidad",
                 "El 90 % de los clientes que cancelaron se quejaron antes al soporte. ¿Significa que el 90 % de los que se quejan cancelan?",
                 ["Sí, es lo mismo", "No: P(queja | canceló) no es P(canceló | queja); hay que mirar cuántos de los que se quejan cancelan",
                  "Sí, si la muestra es grande", "Solo si las quejas son graves"], 1,
                 "Si se quejan muchísimos clientes y pocos cancelan, P(canceló | queja) puede ser pequeña aunque P(queja | canceló) sea 90 %."),
        ],
    },
    {
        "slug": "est-inferencia",
        "phase": "estadistica",
        "title": "Muestreo e intervalos de confianza",
        "summary": "Población y muestra, sesgos de muestreo, error estándar, teorema central del límite, intervalos de confianza y bootstrap.",
        "hours": 8,
        "theory": r"""
# Muestreo e intervalos de confianza

Casi nunca ves a toda la población: ves una **muestra**. La inferencia te dice **cuánto confiar** en lo que calculas con ella.

## 1. Población, muestra y sesgo

- **Población:** todos los casos que te interesan (todos tus clientes).
- **Muestra:** los que realmente observas (los que respondieron la encuesta).
- **Sesgo de muestreo:** la muestra no representa a la población. **Más datos no lo arreglan.**
  - *Sesgo de selección:* encuesta solo por la app → no representa a quien no usa la app.
  - *Sesgo de supervivencia:* analizar solo las empresas que siguen abiertas.
  - *Sesgo de no respuesta:* responden sobre todo los muy contentos o los muy enfadados.

Una muestra pequeña pero **aleatoria** suele ser mejor que una enorme pero sesgada.

## 2. El error estándar

Si repitieras el muestreo muchas veces, la media saldría un poco distinta cada vez. El **error estándar** mide esa variación:

```
EE de la media = desviación muestral / √n
EE de una proporción = √( p · (1 − p) / n )
```

Fíjate en la raíz: para **reducir el error a la mitad** necesitas **4 veces** más datos.

## 3. Teorema central del límite (TCL)

Aunque los datos originales no sean normales, **la media de muestras grandes se distribuye aproximadamente como una normal**. Por eso podemos
construir intervalos de confianza para medias y proporciones con la normal (en la práctica, con n ≥ 30 suele bastar; con datos muy sesgados hace falta más).

## 4. Intervalos de confianza (IC)

Un IC del 95 % para una media:

```
media ± 1,96 · EE
```

Para una proporción: `p ± 1,96 · √(p(1−p)/n)`.

**Cómo interpretarlo bien:** "si repitiéramos este muestreo muchas veces, el 95 % de los intervalos construidos así contendrían el valor real".
En la práctica, comunícalo como "la conversión está entre 4,2 % y 5,8 %" en vez de "la conversión es 5 %". Es **más honesto** y evita sobrerreaccionar a cambios pequeños.

Un intervalo **ancho** significa poca información: necesitas más datos antes de decidir.

## 5. Bootstrap: intervalos sin fórmulas

Cuando no hay una fórmula sencilla (la mediana, un percentil, una métrica rara), puedes **remuestrear con reemplazo** tus datos miles de veces,
calcular la métrica en cada remuestra y tomar los percentiles 2,5 y 97,5 de los resultados. Es simple y muy usado en la industria.

## 6. Errores frecuentes

- Comparar dos números sin mirar sus intervalos ("subió de 5,0 % a 5,3 %": ¿es real o es ruido?).
- Creer que una muestra enorme corrige un sesgo.
- Presentar decimales que no son significativos (una encuesta de 80 personas no da 47,25 %).

## Cómo sabes que dominas este tema

- Identificas el sesgo de muestreo en un caso descrito.
- Calculas e interpretas un IC del 95 % para una media y para una proporción.
- Sabes cuántos datos más necesitas para estrechar un intervalo a la mitad.
""",
        "exercises": [
            py("inf-ee", "Error estándar de la media", "Estadística: inferencia",
               "Escribe `error_estandar(valores)` que devuelva `desviacion_muestral / raiz(n)`. Puedes usar `statistics.stdev` y `math.sqrt`.",
               starter="""
import math
import statistics

def error_estandar(valores):
    # tu código aquí
    pass
""",
               solution="""
import math
import statistics

def error_estandar(valores):
    return statistics.stdev(valores) / math.sqrt(len(valores))
""",
               tests="""
res = error_estandar([2, 4, 4, 4, 5, 5, 7, 9])
assert abs(res - 0.75593) < 1e-4, "Esperaba ~0.7559 y obtuve %r" % res
assert abs(error_estandar([1, 3]) - 1.0) < 1e-9
"""),
            py("inf-ic-media", "IC del 95 % para una media", "Estadística: inferencia",
               "Escribe `ic_media(valores)` que devuelva una tupla `(inferior, superior)` con el intervalo de confianza del 95 %: `media ± 1.96 * error_estandar`.",
               starter="""
import math
import statistics

def ic_media(valores):
    # tu código aquí
    pass
""",
               solution="""
import math
import statistics

def ic_media(valores):
    media = statistics.mean(valores)
    ee = statistics.stdev(valores) / math.sqrt(len(valores))
    return media - 1.96 * ee, media + 1.96 * ee
""",
               tests="""
inf, sup = ic_media([10, 12, 14, 16, 18])
assert abs(inf - 11.2282) < 1e-3 and abs(sup - 16.7718) < 1e-3, "Esperaba ~(11.228, 16.772) y obtuve %r" % ((inf, sup),)
inf, sup = ic_media([5, 5, 5, 5])
assert inf == sup == 5, "Sin variacion el intervalo es un solo punto"
"""),
            py("inf-ic-prop", "IC del 95 % para una proporción", "Estadística: inferencia",
               "Escribe `ic_proporcion(exitos, n)` que devuelva `(inferior, superior)`: `p ± 1.96 * raiz(p * (1 - p) / n)`, con `p = exitos / n`.",
               starter="""
import math

def ic_proporcion(exitos, n):
    # tu código aquí
    pass
""",
               solution="""
import math

def ic_proporcion(exitos, n):
    p = exitos / n
    margen = 1.96 * math.sqrt(p * (1 - p) / n)
    return p - margen, p + margen
""",
               tests="""
inf, sup = ic_proporcion(50, 1000)
assert abs(inf - 0.03649) < 1e-4 and abs(sup - 0.06351) < 1e-4, "50 de 1000: esperaba ~(0.0365, 0.0635), obtuve %r" % ((inf, sup),)
inf4, sup4 = ic_proporcion(200, 4000)
assert abs((sup4 - inf4) - (sup - inf) / 2) < 1e-9, "Con 4 veces mas datos, el intervalo mide la mitad"
"""),
            py("inf-bootstrap", "Bootstrap de la media", "Estadística: inferencia",
               "Escribe `bootstrap_medias(valores, repeticiones, semilla=0)` que, con `rng = random.Random(semilla)`, genere `repeticiones` remuestras con reemplazo "
               "del mismo tamaño que `valores` (usa `rng.choices(valores, k=len(valores))`) y devuelva la lista de sus medias.",
               starter="""
import random

def bootstrap_medias(valores, repeticiones, semilla=0):
    rng = random.Random(semilla)
    # tu código aquí
    pass
""",
               solution="""
import random

def bootstrap_medias(valores, repeticiones, semilla=0):
    rng = random.Random(semilla)
    medias = []
    for _ in range(repeticiones):
        muestra = rng.choices(valores, k=len(valores))
        medias.append(sum(muestra) / len(muestra))
    return medias
""",
               tests="""
datos = [3, 7, 8, 10, 12, 15, 21, 22, 30, 40]
medias = bootstrap_medias(datos, 2000)
assert len(medias) == 2000, "Debe haber una media por repeticion"
promedio = sum(medias) / len(medias)
assert abs(promedio - sum(datos) / len(datos)) < 0.6, "El promedio de las medias bootstrap debe acercarse a la media original (16.8)"
assert bootstrap_medias(datos, 5, 3) == bootstrap_medias(datos, 5, 3), "Con la misma semilla debe ser reproducible"
assert min(medias) >= min(datos) and max(medias) <= max(datos)
"""),
            quiz("inf-quiz-sesgo", "Muestra grande pero sesgada", "Estadística: inferencia",
                 "Haces una encuesta de satisfacción solo a usuarios que abren la app a diario y obtienes 50 000 respuestas. ¿Qué problema tiene?",
                 ["Ninguno: con 50 000 respuestas es representativa", "Sesgo de selección: deja fuera a los usuarios menos activos, que pueden estar menos satisfechos",
                  "El error estándar es demasiado grande", "Hay que usar la mediana"], 1,
                 "El tamaño reduce el error aleatorio, pero no corrige un sesgo. La muestra no representa a toda la base de usuarios."),
            quiz("inf-quiz-n", "Estrechar un intervalo", "Estadística: inferencia",
                 "Tu IC del 95 % para la conversión tiene un margen de ± 2 puntos con 1000 usuarios. ¿Cuántos necesitas, aproximadamente, para un margen de ± 1 punto?",
                 ["2000", "4000", "1500", "10 000"], 1,
                 "El margen depende de 1/√n: para reducirlo a la mitad necesitas 4 veces más datos."),
            quiz("inf-quiz-ic", "Interpretar un intervalo", "Estadística: inferencia",
                 "El ticket promedio tiene un IC del 95 % de [41, 49] USD. ¿Cómo lo comunicarías a un directivo?",
                 ["El ticket promedio es exactamente 45 USD", "Con los datos actuales, el ticket promedio real está probablemente entre 41 y 49 USD",
                  "El 95 % de los clientes gasta entre 41 y 49 USD", "El ticket cambia entre 41 y 49 cada día"], 1,
                 "El intervalo es sobre la **media**, no sobre clientes individuales. Comunicar el rango evita una falsa precisión."),
        ],
    },
    {
        "slug": "est-ab-testing",
        "phase": "estadistica",
        "title": "Pruebas de hipótesis y A/B testing",
        "summary": "Hipótesis nula, valor p, errores tipo I y II, potencia, prueba z de dos proporciones, tamaño de muestra y errores comunes en experimentos.",
        "hours": 10,
        "theory": r"""
# Pruebas de hipótesis y A/B testing

Un **A/B test** es un experimento: muestras la versión A a un grupo aleatorio y la B a otro, y comparas una métrica. Es **la** herramienta para
saber si un cambio **causa** una mejora. Aparece en casi todas las entrevistas de analista de producto.

## 1. El razonamiento

1. **Hipótesis nula (H₀):** no hay diferencia entre A y B.
2. **Hipótesis alternativa (H₁):** sí la hay.
3. Calculas qué tan **sorprendentes** serían tus datos **si H₀ fuera cierta**. Eso es el **valor p**.
4. Si el valor p es menor que un umbral fijado **antes** (α, normalmente 0,05), rechazas H₀.

**El valor p NO es** la probabilidad de que B sea mejor, ni la probabilidad de que H₀ sea cierta, ni el tamaño del efecto.

## 2. Los dos errores

| | H₀ es cierta (no hay efecto) | H₀ es falsa (hay efecto) |
|---|---|---|
| Rechazas H₀ | **Error tipo I** (falso positivo), probabilidad α | Correcto |
| No rechazas H₀ | Correcto | **Error tipo II** (falso negativo), probabilidad β |

La **potencia** (1 − β, normalmente 80 %) es la probabilidad de detectar un efecto real. Con pocos datos, la potencia es baja y te pierdes mejoras reales.

## 3. Prueba z para dos proporciones (conversiones)

```
p_A = conv_A / n_A        p_B = conv_B / n_B
p   = (conv_A + conv_B) / (n_A + n_B)              # proporción combinada
EE  = √( p · (1 − p) · (1/n_A + 1/n_B) )
z   = (p_B − p_A) / EE
```

El valor p bilateral se obtiene de la normal: `p = 2 · (1 − Φ(|z|))`. En Python: `math.erfc(abs(z) / math.sqrt(2))`.
Con α = 0,05, `|z| > 1,96` es significativo. En el trabajo usarás `statsmodels` o `scipy`, pero entender el cálculo te permite explicarlo.

## 4. Antes de lanzar el experimento

- **Una métrica principal** definida de antemano (y métricas de "guarda", como cancelaciones, que no deben empeorar).
- **Tamaño de muestra** calculado según el efecto mínimo que te importa detectar. Para proporciones, por grupo:

```
n ≈ (z_α/2 + z_β)² · (p₁(1−p₁) + p₂(1−p₂)) / (p₂ − p₁)²      con z_α/2 = 1,96 y z_β = 0,84 (80 % de potencia)
```

  Detectar mejoras pequeñas requiere **muchísimos** usuarios.
- **Asignación aleatoria** y duración de semanas completas (los lunes no se parecen a los sábados).

## 5. Los errores que invalidan un test

- **Mirar los resultados cada día y parar cuando "sale significativo"** (*peeking*). Infla mucho los falsos positivos. Decide la duración antes.
- **Comparaciones múltiples:** si pruebas 20 métricas o 20 segmentos, por azar alguna saldrá "significativa".
- **Desbalance de muestra (SRM):** si asignaste 50/50 y tienes 52/48 con muchos usuarios, algo falla en la asignación: no confíes en el resultado.
- Confundir **significativo** con **importante:** con millones de usuarios, una mejora del 0,01 % puede ser significativa e irrelevante para el negocio.

## 6. Qué reportar

El efecto (absoluto y relativo), su **intervalo de confianza**, el valor p, el tamaño de muestra, la duración y una **recomendación**.

## Cómo sabes que dominas este tema

- Explicas qué es (y qué no es) un valor p.
- Calculas una prueba z de dos proporciones y el tamaño de muestra necesario.
- Detectas *peeking*, comparaciones múltiples y SRM en un caso descrito.
""",
        "exercises": [
            py("est-ab", "Mejora relativa en un A/B test", "Estadística: A/B testing",
               "Escribe `mejora_relativa(conv_a, total_a, conv_b, total_b)` que devuelva la mejora relativa de la tasa de conversión de B respecto a A: "
               "`(tasa_b - tasa_a) / tasa_a`. Por ejemplo, si A convierte 5 % y B 6 %, la mejora es `0.2` (20 %).",
               starter="""
def mejora_relativa(conv_a, total_a, conv_b, total_b):
    # tu código aquí
    pass
""",
               solution="""
def mejora_relativa(conv_a, total_a, conv_b, total_b):
    tasa_a = conv_a / total_a
    tasa_b = conv_b / total_b
    return (tasa_b - tasa_a) / tasa_a
""",
               tests="""
assert abs(mejora_relativa(50, 1000, 60, 1000) - 0.2) < 1e-9, "5% -> 6% es una mejora relativa de 0.2"
assert abs(mejora_relativa(100, 1000, 90, 1000) + 0.1) < 1e-9, "10% -> 9% es una caida relativa de -0.1"
"""),
            py("ab-z", "Prueba z de dos proporciones", "Estadística: A/B testing",
               "Escribe `z_dos_proporciones(conv_a, n_a, conv_b, n_b)` que devuelva el estadístico z usando la proporción combinada (ver la teoría).",
               starter="""
import math

def z_dos_proporciones(conv_a, n_a, conv_b, n_b):
    # tu código aquí
    pass
""",
               solution="""
import math

def z_dos_proporciones(conv_a, n_a, conv_b, n_b):
    p_a = conv_a / n_a
    p_b = conv_b / n_b
    p = (conv_a + conv_b) / (n_a + n_b)
    ee = math.sqrt(p * (1 - p) * (1 / n_a + 1 / n_b))
    return (p_b - p_a) / ee
""",
               tests="""
z = z_dos_proporciones(200, 2000, 250, 2000)
assert abs(z - 2.50196) < 1e-3, "10%% vs 12.5%% con 2000 por grupo: z ~ 2.502, obtuve %r" % z
assert abs(z_dos_proporciones(250, 2000, 200, 2000) + 2.50196) < 1e-3, "Si B es peor, z es negativo"
"""),
            py("ab-pvalor", "Valor p bilateral", "Estadística: A/B testing",
               "Escribe `p_valor_bilateral(z)` que devuelva el valor p bilateral de un estadístico z: `math.erfc(abs(z) / math.sqrt(2))`. "
               "Comprueba que con `z = 1.96` sale aproximadamente 0.05.",
               starter="""
import math

def p_valor_bilateral(z):
    # tu código aquí
    pass
""",
               solution="""
import math

def p_valor_bilateral(z):
    return math.erfc(abs(z) / math.sqrt(2))
""",
               tests="""
assert abs(p_valor_bilateral(1.96) - 0.05) < 1e-3, "z = 1.96 corresponde a p ~ 0.05"
assert abs(p_valor_bilateral(-1.96) - 0.05) < 1e-3, "Es bilateral: el signo no importa"
assert abs(p_valor_bilateral(0) - 1.0) < 1e-9, "z = 0 -> p = 1"
"""),
            py("ab-decision", "Decidir un A/B test", "Estadística: A/B testing",
               "Escribe `decidir(conv_a, n_a, conv_b, n_b, alpha=0.05)` que devuelva `'B gana'` si B es significativamente mejor, `'A gana'` si B es significativamente peor, "
               "y `'sin diferencia'` si el valor p no es menor que `alpha`. Las funciones auxiliares ya están escritas.",
               starter="""
import math

def z_dos_proporciones(conv_a, n_a, conv_b, n_b):
    p_a, p_b = conv_a / n_a, conv_b / n_b
    p = (conv_a + conv_b) / (n_a + n_b)
    return (p_b - p_a) / math.sqrt(p * (1 - p) * (1 / n_a + 1 / n_b))

def p_valor_bilateral(z):
    return math.erfc(abs(z) / math.sqrt(2))

def decidir(conv_a, n_a, conv_b, n_b, alpha=0.05):
    # tu código aquí
    pass
""",
               solution="""
import math

def z_dos_proporciones(conv_a, n_a, conv_b, n_b):
    p_a, p_b = conv_a / n_a, conv_b / n_b
    p = (conv_a + conv_b) / (n_a + n_b)
    return (p_b - p_a) / math.sqrt(p * (1 - p) * (1 / n_a + 1 / n_b))

def p_valor_bilateral(z):
    return math.erfc(abs(z) / math.sqrt(2))

def decidir(conv_a, n_a, conv_b, n_b, alpha=0.05):
    z = z_dos_proporciones(conv_a, n_a, conv_b, n_b)
    if p_valor_bilateral(z) >= alpha:
        return "sin diferencia"
    return "B gana" if z > 0 else "A gana"
""",
               tests="""
assert decidir(200, 2000, 250, 2000) == "B gana", "10% vs 12.5% con 2000 por grupo es significativo a favor de B"
assert decidir(250, 2000, 200, 2000) == "A gana"
assert decidir(100, 1000, 104, 1000) == "sin diferencia", "10.0% vs 10.4% con 1000 por grupo no es significativo"
assert decidir(200, 2000, 250, 2000, alpha=0.01) == "sin diferencia", "Con alpha = 0.01 (p ~ 0.012) ya no es significativo"
"""),
            py("ab-muestra", "Tamaño de muestra", "Estadística: A/B testing",
               "Escribe `tamano_muestra(p_base, mejora_relativa)` que devuelva cuántos usuarios necesitas **por grupo** (redondeando hacia arriba con `math.ceil`) "
               "para detectar que la conversión pasa de `p_base` a `p_base * (1 + mejora_relativa)`, con α = 0.05 y potencia del 80 %: "
               "`n = (1.96 + 0.84)**2 * (p1*(1-p1) + p2*(1-p2)) / (p2 - p1)**2`.",
               starter="""
import math

def tamano_muestra(p_base, mejora_relativa):
    # tu código aquí
    pass
""",
               solution="""
import math

def tamano_muestra(p_base, mejora_relativa):
    p1 = p_base
    p2 = p_base * (1 + mejora_relativa)
    n = (1.96 + 0.84) ** 2 * (p1 * (1 - p1) + p2 * (1 - p2)) / (p2 - p1) ** 2
    return math.ceil(n)
""",
               tests="""
assert tamano_muestra(0.05, 0.2) == 8146, "De 5%% a 6%%: ~8146 usuarios por grupo; obtuve %r" % (tamano_muestra(0.05, 0.2),)
assert tamano_muestra(0.05, 0.1) > 3 * tamano_muestra(0.05, 0.2), "Detectar una mejora a la mitad requiere unas 4 veces mas usuarios"
"""),
            quiz("est-quiz-p", "Qué es un valor p", "Estadística: A/B testing",
                 "En un A/B test obtienes p = 0,03. ¿Qué afirmación es correcta?",
                 ["Hay un 97 % de probabilidad de que B sea mejor que A",
                  "Si en realidad no hubiera diferencia, ver un resultado así de extremo (o más) ocurriría ~3 % de las veces",
                  "El efecto es grande e importante para el negocio", "Hay un 3 % de probabilidad de que el test esté mal hecho"], 1,
                 "El valor p mide qué tan sorprendente es el dato **si no hubiera efecto**. No te dice la probabilidad de que B sea mejor ni el tamaño del efecto."),
            quiz("ab-quiz-peeking", "Mirar antes de tiempo", "Estadística: A/B testing",
                 "Planeaste un test de 3 semanas, pero lo revisas cada mañana y lo detienes el día 4 porque el valor p bajó de 0,05. ¿Qué pasa?",
                 ["Está bien, ya es significativo", "Aumentaste mucho la probabilidad de un falso positivo: el valor p fluctúa y tarde o temprano cruza 0,05 por azar",
                  "Ahorraste tiempo sin ningún riesgo", "El resultado es más fiable porque es temprano"], 1,
                 "Revisar repetidamente y parar en cuanto sale 'bien' (peeking) invalida el α del 5 %. Respeta la duración planificada o usa métodos secuenciales diseñados para ello."),
            quiz("ab-quiz-practica", "Significativo no es importante", "Estadística: A/B testing",
                 "Con 10 millones de usuarios, un cambio sube la conversión de 4,00 % a 4,01 % con p = 0,001. Implementarlo cuesta dos meses de trabajo. ¿Qué concluyes?",
                 ["Hay que implementarlo: es muy significativo", "Es estadísticamente significativo, pero el efecto es tan pequeño que quizá no compense el costo",
                  "El test está mal hecho", "Hay que repetirlo con menos usuarios"], 1,
                 "Con muestras enormes, efectos diminutos salen significativos. La decisión depende del **tamaño** del efecto y su impacto en el negocio."),
            checklist("ab-check", "Diseña un A/B test", "Estadística: A/B testing",
                      "Escribe en tus Apuntes el diseño de un test para un cambio real (por ejemplo, un nuevo botón de compra) y comprueba cada punto.",
                      ["Definí la hipótesis y la métrica principal", "Definí al menos una métrica de guarda que no debe empeorar",
                       "Calculé el tamaño de muestra según el efecto mínimo que me importa", "Fijé la duración en semanas completas antes de empezar",
                       "Expliqué cómo se asignan los usuarios al azar", "Escribí qué decisión tomaré con cada resultado posible"]),
        ],
    },
    {
        "slug": "est-regresion",
        "phase": "estadistica",
        "title": "Correlación y regresión lineal",
        "summary": "Correlación, causalidad, variables de confusión, paradoja de Simpson, regresión lineal simple, R² y residuos.",
        "hours": 8,
        "theory": r"""
# Correlación y regresión lineal

Buena parte del análisis consiste en preguntar "¿cómo se relaciona X con Y?". Este tema te da las herramientas y, sobre todo, las **precauciones**.

## 1. Correlación

El coeficiente de **Pearson** `r` (de −1 a 1) mide la fuerza de una relación **lineal**:

- `r ≈ 1`: cuando X sube, Y sube casi en línea recta.
- `r ≈ −1`: cuando X sube, Y baja.
- `r ≈ 0`: no hay relación **lineal** (¡puede haber una curva!).

**Grafica siempre** un diagrama de dispersión: datos muy distintos pueden tener el mismo `r` (el famoso cuarteto de Anscombe).
Si hay valores extremos o la relación es monótona pero no lineal, usa la correlación de **Spearman** (sobre rangos).

## 2. Correlación no implica causalidad

Que dos variables se muevan juntas puede deberse a:

1. **Causalidad real** (X causa Y).
2. **Causalidad inversa** (Y causa X).
3. **Una variable de confusión** que causa ambas: las ventas de helado y los ahogamientos suben juntos por el calor.
4. **Azar**, sobre todo si buscaste entre muchas variables.

Para afirmar causalidad necesitas un **experimento** (A/B test) o diseños cuasi-experimentales cuidadosos. En informes, escribe "se asocia con".

## 3. Paradoja de Simpson

Una tendencia que aparece en **cada grupo** puede **invertirse** al juntar los grupos. Ejemplo: un tratamiento tiene mejor tasa de éxito
en casos leves **y** en casos graves, pero peor tasa global porque se aplicó sobre todo a casos graves. **Lección:** cuando una comparación
global te sorprenda, segmenta por las variables que pueden cambiar la composición de los grupos.

## 4. Regresión lineal simple

Busca la recta `y = a + b·x` que minimiza los errores al cuadrado (**mínimos cuadrados**):

```
b (pendiente)  = Σ(x − x̄)(y − ȳ) / Σ(x − x̄)²
a (intercepto) = ȳ − b · x̄
```

**Interpretar la pendiente** es lo que importa: "por cada 1 000 USD extra de publicidad, las ventas aumentan en promedio 3 200 USD" (asociación, no necesariamente causa).

## 5. ¿Qué tan bien ajusta? R² y residuos

- **R²** (de 0 a 1): proporción de la variación de Y que explica el modelo. `R² = 1 − SS_res / SS_tot`.
  Un R² bajo no siempre es malo (los comportamientos humanos son ruidosos) y uno alto no garantiza que el modelo sea útil.
- **Residuos** = real − predicho. Grafícalos: si muestran un patrón (curva, embudo), la relación no es lineal o la varianza no es constante.
- **No extrapoles:** la recta solo es razonable dentro del rango de datos observado.

## 6. En la práctica

Con varias variables usarás **regresión múltiple** (`statsmodels` para interpretar coeficientes y sus intervalos, `scikit-learn` para predecir).
La idea es la misma: cada coeficiente es el efecto asociado de esa variable **manteniendo las demás constantes**.

## Cómo sabes que dominas este tema

- Das tres explicaciones alternativas para una correlación observada.
- Calculas e interpretas la pendiente y el R² de una regresión simple.
- Reconoces cuándo segmentar para evitar la paradoja de Simpson.
""",
        "exercises": [
            py("est-corr", "Correlación de Pearson", "Estadística: correlación y regresión",
               "Escribe `correlacion(x, y)` que calcule el coeficiente de correlación de Pearson entre dos listas del mismo tamaño.",
               starter="""
def correlacion(x, y):
    # tu código aquí
    pass
""",
               solution="""
def correlacion(x, y):
    n = len(x)
    mx = sum(x) / n
    my = sum(y) / n
    covarianza = sum((a - mx) * (b - my) for a, b in zip(x, y))
    sx = sum((a - mx) ** 2 for a in x) ** 0.5
    sy = sum((b - my) ** 2 for b in y) ** 0.5
    return covarianza / (sx * sy)
""",
               tests="""
assert abs(correlacion([1, 2, 3, 4], [2, 4, 6, 8]) - 1.0) < 1e-9, "Relacion lineal perfecta positiva = 1"
assert abs(correlacion([1, 2, 3, 4], [8, 6, 4, 2]) + 1.0) < 1e-9, "Relacion lineal perfecta negativa = -1"
assert abs(correlacion([1, 2, 3, 4, 5], [2, 1, 4, 3, 5]) - 0.8) < 1e-9, "Para este caso r = 0.8"
"""),
            py("reg-recta", "Recta de mínimos cuadrados", "Estadística: correlación y regresión",
               "Escribe `regresion_simple(x, y)` que devuelva una tupla `(pendiente, intercepto)` con las fórmulas de mínimos cuadrados de la teoría.",
               starter="""
def regresion_simple(x, y):
    # tu código aquí
    pass
""",
               solution="""
def regresion_simple(x, y):
    n = len(x)
    mx = sum(x) / n
    my = sum(y) / n
    pendiente = sum((a - mx) * (b - my) for a, b in zip(x, y)) / sum((a - mx) ** 2 for a in x)
    intercepto = my - pendiente * mx
    return pendiente, intercepto
""",
               tests="""
b, a = regresion_simple([1, 2, 3, 4, 5], [2, 4, 5, 4, 5])
assert abs(b - 0.6) < 1e-9 and abs(a - 2.2) < 1e-9, "Esperaba pendiente 0.6 e intercepto 2.2, obtuve %r" % ((b, a),)
b, a = regresion_simple([0, 1, 2], [1, 3, 5])
assert abs(b - 2) < 1e-9 and abs(a - 1) < 1e-9, "y = 1 + 2x exactamente"
"""),
            py("reg-r2", "Coeficiente R²", "Estadística: correlación y regresión",
               "Escribe `r_cuadrado(y_real, y_pred)` que devuelva `1 - SS_res / SS_tot`, donde `SS_res = Σ(real - pred)²` y `SS_tot = Σ(real - media_real)²`.",
               starter="""
def r_cuadrado(y_real, y_pred):
    # tu código aquí
    pass
""",
               solution="""
def r_cuadrado(y_real, y_pred):
    media = sum(y_real) / len(y_real)
    ss_res = sum((r - p) ** 2 for r, p in zip(y_real, y_pred))
    ss_tot = sum((r - media) ** 2 for r in y_real)
    return 1 - ss_res / ss_tot
""",
               tests="""
real = [2, 4, 5, 4, 5]
pred = [2.8, 3.4, 4.0, 4.6, 5.2]
assert abs(r_cuadrado(real, pred) - 0.6) < 1e-9, "SS_res = 2.4 y SS_tot = 6 -> R2 = 0.6"
assert r_cuadrado([1, 2, 3], [1, 2, 3]) == 1.0, "Prediccion perfecta -> R2 = 1"
"""),
            py("reg-simpson", "Detectar la paradoja de Simpson", "Estadística: correlación y regresión",
               "Escribe `tasas(registros)`. `registros` es una lista de tuplas `(grupo, tratamiento, exito)` con `tratamiento` en `'A'`/`'B'` y `exito` booleano. "
               "Devuelve un diccionario `{'global': {'A': tasa, 'B': tasa}, grupo1: {...}, grupo2: {...}}` con la tasa de éxito de cada tratamiento en total y dentro de cada grupo.",
               starter="""
def tasas(registros):
    # tu código aquí
    pass
""",
               solution="""
def tasas(registros):
    conteos = {}
    for grupo, tratamiento, exito in registros:
        for clave in ("global", grupo):
            exitos, total = conteos.get((clave, tratamiento), (0, 0))
            conteos[(clave, tratamiento)] = (exitos + int(exito), total + 1)
    resultado = {}
    for (clave, tratamiento), (exitos, total) in conteos.items():
        resultado.setdefault(clave, {})[tratamiento] = exitos / total
    return resultado
""",
               tests="""
registros = (
    [("leve", "A", True)] * 81 + [("leve", "A", False)] * 6 +
    [("leve", "B", True)] * 234 + [("leve", "B", False)] * 36 +
    [("grave", "A", True)] * 192 + [("grave", "A", False)] * 71 +
    [("grave", "B", True)] * 55 + [("grave", "B", False)] * 25
)
t = tasas(registros)
assert t["leve"]["A"] > t["leve"]["B"] and t["grave"]["A"] > t["grave"]["B"], "A es mejor dentro de cada grupo"
assert t["global"]["A"] < t["global"]["B"], "...pero peor en el total: eso es la paradoja de Simpson"
assert abs(t["global"]["A"] - 273 / 350) < 1e-9 and abs(t["global"]["B"] - 289 / 350) < 1e-9
""",
               hint="Acumula (éxitos, total) por (clave, tratamiento), donde la clave es 'global' y también el grupo de cada registro."),
            quiz("reg-quiz-confusion", "Variable de confusión", "Estadística: correlación y regresión",
                 "Los clientes que usan el chat de soporte gastan más. Un directivo propone obligar a todos a usar el chat. ¿Cuál es la objeción principal?",
                 ["El chat es caro", "Puede haber una variable de confusión: los clientes más comprometidos usan el chat y también gastan más",
                  "La correlación es demasiado alta", "Hay que usar Spearman"], 1,
                 "La asociación no prueba que el chat cause el gasto. Un experimento (A/B) sería la forma de comprobarlo."),
            quiz("reg-quiz-r0", "Correlación cero", "Estadística: correlación y regresión",
                 "Calculas r = 0,02 entre la temperatura y las ventas de una bebida. ¿Qué puedes concluir con seguridad?",
                 ["No hay ninguna relación", "No hay relación lineal fuerte, pero podría haber una no lineal: hay que graficar los datos",
                  "Hay causalidad negativa", "Los datos están mal"], 1,
                 "Pearson solo mide relaciones lineales. Una relación en forma de U (ventas bajas con frío y calor extremos) puede dar r ≈ 0."),
            quiz("reg-quiz-extrapolar", "Extrapolar", "Estadística: correlación y regresión",
                 "Ajustaste una regresión de ventas sobre inversión publicitaria con inversiones entre 1 000 y 10 000 USD. ¿Es fiable predecir las ventas con 100 000 USD?",
                 ["Sí, la recta sigue igual", "No: es extrapolar muy lejos del rango observado; la relación puede cambiar (saturación)",
                  "Sí, si el R² es alto", "Solo si la pendiente es positiva"], 1,
                 "Fuera del rango de datos no sabes si la relación se mantiene. En publicidad suele haber rendimientos decrecientes."),
        ],
    },
    {
        "slug": "proyecto-eda",
        "phase": "estadistica",
        "title": "Proyecto 1: análisis exploratorio completo",
        "summary": "Tu primera pieza de portafolio: un EDA con preguntas de negocio, limpieza, gráficos y conclusiones.",
        "hours": 16,
        "theory": r"""
# Proyecto 1: análisis exploratorio completo (EDA)

Hasta aquí aprendiste herramientas. Ahora las **combinas** en algo que puedes enseñar a un reclutador. Lo que busca un
entrevistador no es un notebook con 40 gráficos: es ver que sabes **hacer preguntas, validar datos y comunicar conclusiones**.

## 1. Elige un dataset con historia

Busca datos reales que te interesen y que tengan fechas, categorías y números. Ideas de fuentes: Kaggle, datos abiertos
de tu país o de tu ciudad, Our World in Data, Inside Airbnb, estadísticas de deportes, tu propia información
(gastos, estudio). **Mejor un tema que te apasione que uno "famoso" que todos usan** (el Titanic no te diferencia).

## 2. Estructura recomendada del proyecto

1. **Contexto y preguntas** (3-5 preguntas de negocio concretas).
2. **Carga y revisión inicial:** tamaño, tipos, nulos, duplicados.
3. **Limpieza documentada:** cada decisión con su justificación.
4. **Análisis:** responde cada pregunta con tablas y gráficos claros.
5. **Conclusiones y recomendaciones:** qué haría el negocio con esto, qué limitaciones tiene el análisis.
6. **Cómo reproducirlo:** `README.md` con instrucciones, versiones y dónde descargar los datos.

## 3. Qué lo hace destacar

- Preguntas que un negocio **sí** haría ("¿qué zonas tienen mayor oferta pero menor precio?").
- **Datos extraídos con SQL:** carga el dataset en PostgreSQL y haz la parte pesada con consultas.
- Gráficos limpios con título-conclusión y un solo color de énfasis.
- Una sección honesta de **limitaciones** (muestra sesgada, datos faltantes).
- **Incertidumbre:** acompaña tus cifras clave con intervalos de confianza y, si comparas grupos, indica si la diferencia es estadísticamente significativa (lo viste en la fase de estadística).
- Código en un repositorio de GitHub con carpetas ordenadas (`data/`, `notebooks/`, `src/`).

## 4. Plan de trabajo sugerido (≈ 16 horas)

| Horas | Tarea |
|---|---|
| 2 | Elegir dataset, definir preguntas, leer el diccionario de datos |
| 3 | Carga, revisión y limpieza |
| 5 | Análisis y gráficos |
| 3 | Conclusiones, redacción y README |
| 3 | Revisión, publicar en GitHub y escribir un post en LinkedIn |

## 5. Errores comunes

- No definir preguntas y "explorar sin rumbo".
- Gráficos sin conclusión.
- No mencionar qué hiciste con los nulos.
- Notebook que solo funciona en tu computador (rutas absolutas).
- Subir datos privados o con licencia que no permite redistribución.

> Pide a alguien (o a mí, en este chat) que **revise tu proyecto** con ojo crítico antes de publicarlo.
""",
        "exercises": [
            quiz("eda-quiz-orden", "Orden de un EDA", "Proyecto: análisis exploratorio",
                 "¿Cuál es el orden más sensato para empezar un análisis exploratorio?",
                 ["Graficar todo y luego pensar qué preguntas hacer",
                  "Definir preguntas, revisar calidad de datos, limpiar, analizar y concluir",
                  "Entrenar un modelo y después limpiar", "Limpiar sin mirar los datos para ahorrar tiempo"], 1,
                 "Las preguntas guían qué mirar; revisar la calidad evita conclusiones falsas; y solo entonces tiene sentido analizar."),
            checklist("eda-entregables", "Entregables del proyecto", "Proyecto: análisis exploratorio",
                      "Marca cada punto cuando esté listo en tu repositorio.",
                      ["Elegí un dataset real y definí 3-5 preguntas de negocio", "Revisé tipos, nulos y duplicados y los documenté",
                       "Documenté cada decisión de limpieza", "Cada pregunta tiene una tabla o gráfico con título-conclusión",
                       "Escribí conclusiones, recomendaciones y limitaciones", "El README explica cómo reproducir el análisis",
                       "Publiqué el proyecto en GitHub"]),
            checklist("eda-revision", "Revisión final de calidad", "Proyecto: análisis exploratorio",
                      "Antes de publicar, repasa estos puntos.",
                      ["Corrí el notebook completo desde cero sin errores", "No hay rutas absolutas ni credenciales en el código",
                       "Los gráficos son legibles y tienen etiquetas", "Alguien ajeno entendió el objetivo en 1 minuto",
                       "Verifiqué la licencia de los datos"]),
        ],
    },
]
