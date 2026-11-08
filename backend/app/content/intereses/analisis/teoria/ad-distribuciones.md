# Distribuciones de probabilidad: los patrones del azar

Una **distribución de probabilidad** describe qué valores puede tomar algo aleatorio y con qué frecuencia. Saber distribuciones sirve
para tres cosas muy prácticas:

1. **Reconocer qué tipo de datos tienes** y, por tanto, qué resumen y qué prueba usar (la media sirve para unos datos y engaña en otros).
2. **Calcular probabilidades** sin tener que simular: "¿qué probabilidad hay de recibir más de 10 mensajes en una hora?".
3. **Detectar lo raro:** si sabes cómo se comporta el azar, sabes cuándo algo se sale de lo esperable.

No hace falta memorizar fórmulas. Lo importante de cada distribución es **qué proceso la genera**: si reconoces el proceso, sabes la
distribución.

## 1. Vocabulario mínimo

- **Variable aleatoria:** un número que sale de un proceso con azar (el número de ventas de mañana, la duración de una visita).
- **Discreta:** toma valores contables (0, 1, 2...). Se describe con la probabilidad de cada valor: `P(X = 3)`.
- **Continua:** toma cualquier valor en un intervalo (1,73 minutos). La probabilidad de un valor exacto es 0; se habla de
  probabilidad de un **rango**: `P(1 < X < 2)`. La curva que lo describe se llama **densidad**.
- **Función de distribución acumulada (CDF):** `P(X ≤ x)`. Sirve para todas: "probabilidad de que el pedido tarde menos de 40 minutos".
- **Esperanza (media)** y **varianza:** el centro y la dispersión teóricos de la distribución.
- **Parámetros:** los números que fijan una distribución concreta (por ejemplo, la media y la desviación de una normal).

## 2. Bernoulli y binomial: éxitos en intentos

**Bernoulli:** un único intento con dos resultados, éxito (probabilidad `p`) o fracaso. Un visitante compra o no compra.

**Binomial:** el número de éxitos en `n` intentos **independientes** con la **misma** probabilidad `p`.

```
P(X = k) = C(n, k) · p^k · (1 − p)^(n − k)        media = n·p        varianza = n·p·(1 − p)
```

`C(n, k)` (combinaciones) cuenta de cuántas formas pueden repartirse los `k` éxitos entre los `n` intentos.

Ejemplo: si el 5 % de los visitantes compra, de 200 visitantes esperas `200 · 0,05 = 10` compras, con una desviación de
`√(200 · 0,05 · 0,95) ≈ 3,1`. Ver 6 o 14 compras un día es normal; ver 25 ya es muy raro y merece una explicación.

**Cuándo falla:** si los intentos no son independientes (un mismo usuario cuenta varias veces) o la probabilidad cambia entre intentos
(usuarios de distintos canales con conversiones muy distintas), la variación real es **mayor** que la binomial. Es un fallo común en
los A/B tests que cuentan sesiones en vez de usuarios.

## 3. Geométrica: cuántos intentos hasta el primer éxito

El número de intentos hasta el primer éxito, con probabilidad `p` en cada uno. Media: `1 / p`.

Si cada mensaje en frío a un posible cliente tiene un 4 % de probabilidad de respuesta, esperas enviar en promedio `1 / 0,04 = 25`
mensajes hasta la primera respuesta. Pero la distribución es muy asimétrica: con bastante frecuencia necesitarás más de 50.
Saberlo evita abandonar una estrategia por mala suerte al principio.

## 4. Poisson: conteos de sucesos en un intervalo

El número de sucesos en un intervalo (de tiempo, de espacio) cuando ocurren **independientemente** y a un **ritmo medio constante** `λ`:
mensajes por hora a un chatbot, errores por cada 1 000 líneas, pedidos por minuto.

```
P(X = k) = e^(−λ) · λ^k / k!          media = λ          varianza = λ
```

Ejemplo: si llegan de media 2 mensajes por hora, la probabilidad de una hora sin ninguno es `e^(−2) ≈ 13,5 %`.

La propiedad que hay que recordar: **en una Poisson, la varianza es igual a la media**. Si en tus datos la varianza es mucho mayor
(**sobredispersión**), el ritmo no es constante (hay horas punta, campañas, días especiales) y la Poisson se queda corta: se usa la
**binomial negativa**. Es muy frecuente en datos reales.

Un uso práctico: con λ = 2, ver 9 mensajes en una hora tiene una probabilidad de aproximadamente 0,02 %. Eso no es azar: algo pasó
(un enlace compartido, un ataque de spam). Así funcionan muchas alertas automáticas.

## 5. Uniforme: todos los valores igual de probables

En un intervalo `[a, b]`, todos los valores tienen la misma probabilidad. Aparece sobre todo **de forma artificial**: los números
aleatorios de un ordenador, el reparto al azar en un experimento. En datos reales es rara; si la ves, desconfía (puede que un campo se
haya rellenado con valores inventados).

## 6. Normal: la campana

La distribución en forma de campana, simétrica, definida por su media `μ` y su desviación `σ`. Ya conoces la regla 68-95-99,7. La
probabilidad acumulada no tiene una fórmula simple, pero se calcula con la función de error:

```
P(X < x) = 0,5 · (1 + erf((x − μ) / (σ · √2)))
```

**Por qué aparece tanto:** por el **teorema central del límite**. Cuando una cantidad es la **suma** (o el promedio) de muchos efectos
pequeños e independientes, tiende a la normal, sea cual sea la distribución de cada efecto. Por eso son aproximadamente normales los
errores de medición, la altura de las personas y, sobre todo, **los promedios de muestras grandes**, que es lo que hace funcionar los
intervalos de confianza y las pruebas t.

**Cuándo no aparece:** cuando los efectos se **multiplican** en vez de sumarse, o cuando hay un límite (no puede haber tiempos
negativos) y los datos están cerca de él. En datos de negocio y de redes es la excepción, no la regla.

## 7. Exponencial: tiempos de espera

El tiempo **entre** sucesos de un proceso de Poisson: el tiempo hasta el siguiente mensaje, hasta el siguiente pedido. Si hay `λ`
sucesos por unidad de tiempo, el tiempo medio de espera es `1 / λ`, y:

```
P(espera > t) = e^(−λ·t)
```

Tiene una propiedad curiosa, la **falta de memoria**: si llevas 10 minutos esperando, la probabilidad de esperar 5 más es la misma que
al principio. Encaja con llegadas al azar, pero no con cosas que se desgastan (una máquina vieja sí tiene más probabilidad de fallar).

## 8. Log-normal: cuando los efectos se multiplican

Una variable es **log-normal** si su logaritmo es normal. Surge cuando el valor final es el **producto** de muchos factores:
el precio de una vivienda (tamaño × zona × calidad...), los ingresos, el tiempo en una página, el tamaño de una empresa.

Se reconoce porque:

- Es **asimétrica a la derecha**: muchos valores pequeños y una cola de valores grandes.
- La **media es claramente mayor que la mediana**.
- Si dibujas el histograma del **logaritmo** de los datos, parece una campana.

Consecuencia práctica: con estos datos, trabajar en **escala logarítmica** (gráficos con eje log, modelos sobre `log(precio)`) hace que
casi todo funcione mejor. Y un cambio en logaritmos se interpreta como un cambio **porcentual**.

## 9. Colas largas y leyes de potencias: el mundo de lo viral

Algunas distribuciones tienen colas **mucho más pesadas** que la log-normal: unos pocos casos acumulan casi todo. Es el terreno de
las **leyes de potencias** (distribución de Pareto):

- Las vistas de los vídeos: la mayoría tiene pocas y un puñado tiene millones.
- Los seguidores de las cuentas, las ventas por producto en una tienda en línea, las palabras de un idioma, el tamaño de las ciudades.

El famoso **principio 80/20** viene de aquí: el 20 % de los elementos acumula aproximadamente el 80 % del total (la proporción exacta
varía en cada caso).

Las colas largas surgen de procesos de **ventaja acumulada**: lo que ya tiene vistas recibe más vistas porque el algoritmo lo muestra
más y la gente lo comparte. El éxito alimenta el éxito.

Consecuencias que importan mucho para analizar redes:

1. **La media no describe nada.** Un solo vídeo viral cambia por completo la media de vistas de una cuenta. Usa la **mediana** y los
   percentiles, y analiza los éxitos por separado.
2. **La media es inestable:** cada nuevo éxito extremo la mueve mucho, y con muestras pequeñas casi nunca ves la cola real.
3. **Los promedios de grupos engañan:** "los vídeos de humor tienen más vistas de media" puede deberse a un único vídeo.
4. **La varianza es enorme**, así que comparar dos estrategias de contenido requiere muchos más vídeos de lo que parece, o comparar
   medianas o tasas en vez de vistas totales.

Una forma sencilla de medir lo concentrada que está una distribución es calcular **qué parte del total se llevan los de arriba**
(el 10 % o el 20 % superior). Lo practicarás en los ejercicios.

## 10. Cómo saber qué distribución tienen tus datos

| Si tus datos son... | Piensa en... |
|---|---|
| Sí/no por intento | Bernoulli, binomial para el total |
| Intentos hasta un éxito | Geométrica |
| Conteos por intervalo a ritmo estable | Poisson (binomial negativa si varianza ≫ media) |
| Tiempos entre sucesos al azar | Exponencial |
| Sumas o promedios de muchos efectos | Normal |
| Positivos, asimétricos, producto de factores | Log-normal |
| Unos pocos casos acumulan casi todo | Cola larga / ley de potencias |

Y para comprobarlo:

1. **Histograma**, primero en escala normal y luego en escala logarítmica.
2. **Compara la media con la mediana** y la varianza con la media (en conteos).
3. **Gráfico Q-Q:** ordena tus datos y enfréntalos a los cuantiles de la distribución teórica. Si los puntos forman una línea recta,
   encajan; si se curvan en los extremos, las colas son distintas. En Python: `scipy.stats.probplot`.
4. **Simula:** genera datos con la distribución candidata y los mismos parámetros, y compara los gráficos.

Ninguna distribución teórica encaja perfectamente con datos reales. La pregunta útil no es "¿son exactamente normales?" sino "¿se
parecen lo bastante para que las conclusiones no cambien?".

## 11. En Python

```python
import math, random
from scipy import stats   # en tu ordenador o en Colab

stats.binom.pmf(3, n=10, p=0.5)      # P(X = 3) binomial
stats.poisson.pmf(0, mu=2)           # P(X = 0) Poisson
stats.norm.cdf(50, loc=40, scale=5)  # P(X < 50) normal
stats.expon.sf(5, scale=1/2)         # P(espera > 5) con λ = 2

rng = random.Random(42)              # simular sin scipy
rng.gauss(40, 5); rng.expovariate(2); rng.lognormvariate(0, 1); rng.paretovariate(1.5)
```

En los ejercicios de la plataforma programarás tú las fórmulas con `math`, para que veas que no hay magia detrás.

## Resumen

- Reconoce el **proceso**: intentos (binomial), conteos (Poisson), esperas (exponencial), sumas (normal), productos (log-normal),
  ventaja acumulada (cola larga).
- La normal aparece en los **promedios**, no en la mayoría de los datos de negocio.
- En colas largas, la media engaña: usa mediana, percentiles y escala logarítmica.
- Comprueba con histogramas, gráficos Q-Q y simulaciones antes de suponer una distribución.
