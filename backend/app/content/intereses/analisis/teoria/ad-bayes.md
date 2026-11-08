# Estadística bayesiana: actualizar creencias con datos

Hasta ahora has usado la estadística **frecuentista**: valores p e intervalos de confianza, que hablan de qué pasaría si repitieras el
muestreo muchas veces. La estadística **bayesiana** responde de forma más directa a lo que normalmente quieres saber: **dados mis datos,
¿qué tan probable es cada posibilidad?** Cada vez se usa más en A/B testing, en rankings, en sistemas de recomendación y en IA.

## 1. La idea: creer, observar, actualizar

El enfoque bayesiano trata lo desconocido (la tasa de conversión real, por ejemplo) como algo sobre lo que tienes **incertidumbre**, y
la describe con una distribución de probabilidad. El proceso tiene tres piezas:

1. **Prior (a priori):** lo que crees **antes** de ver los datos. "Las tasas de conversión de páginas como la mía suelen estar entre
   el 1 % y el 5 %."
2. **Verosimilitud:** qué tan probables son los datos observados bajo cada valor posible. "Si la conversión real fuera del 3 %, ¿qué
   tan probable sería ver 12 compras de 300 visitas?"
3. **Posterior (a posteriori):** lo que crees **después** de ver los datos. Combina las dos anteriores mediante el teorema de Bayes:

```
posterior ∝ verosimilitud × prior
```

(∝ significa "proporcional a": después se divide entre la suma para que todo sume 1.)

Y el posterior de hoy es el prior de mañana: cada nuevo dato actualiza la creencia.

## 2. Un ejemplo con pocas hipótesis

Sospechas que una herramienta de automatización que vendes tiene un error que hace fallar el 30 % de las ejecuciones; si no lo tiene,
falla un 5 %. Antes de mirar, crees que hay un 50 % de probabilidad de que tenga el error.

Observas una ejecución y **falla**:

| Hipótesis | Prior | Verosimilitud de un fallo | Prior × verosimilitud | Posterior |
|---|---|---|---|---|
| Tiene el error | 0,5 | 0,30 | 0,150 | 0,150 / 0,175 = **0,857** |
| No lo tiene | 0,5 | 0,05 | 0,025 | 0,025 / 0,175 = **0,143** |

Un solo fallo sube tu creencia del 50 % al 86 %. Si la siguiente ejecución funciona, vuelves a actualizar partiendo de 0,857. Es el
mismo cálculo que hiciste con la prueba médica en el tema de probabilidad, aplicado de forma repetida.

## 3. El modelo beta-binomial: tasas con incertidumbre

Para tasas (conversión, clics, tasa de interacción) hay una combinación especialmente cómoda.

- La **distribución beta** `Beta(a, b)` describe la incertidumbre sobre una proporción entre 0 y 1. Su media es `a / (a + b)` y cuanto
  mayores son `a` y `b`, más concentrada (más segura) está.
- `Beta(1, 1)` es plana: todas las tasas igual de probables (prior "no sé nada").
- Se puede leer `a` como "éxitos imaginarios" y `b` como "fracasos imaginarios" que aportas antes de empezar.

Y la gran ventaja: si el prior es `Beta(a, b)` y observas `éxitos` y `fracasos`, el posterior es simplemente:

```
Beta(a + éxitos, b + fracasos)
```

Sumas los éxitos y los fracasos. Ejemplo: con prior `Beta(1, 1)` y 8 compras de 10 visitas, el posterior es `Beta(9, 3)`, con media
9/12 = 75 %. Pero con un prior realista que espera en torno al 5 %, como `Beta(2, 38)`, 3 compras de 3 visitas dan `Beta(5, 38)`: una
media del 11,6 %, no del 100 %. El prior frena las conclusiones precipitadas con pocos datos.

## 4. Elegir el prior

Es la parte que más críticas recibe y la que más hay que cuidar:

- **Poco informativo** (`Beta(1, 1)`): deja hablar casi solo a los datos. Seguro cuando no sabes nada.
- **Informativo**, basado en datos históricos: "nuestras landing pages convierten entre el 2 % y el 6 %". Ayuda mucho con pocos datos.
  Una forma de construirlo: si la media histórica es `m` y quieres que pese como `k` observaciones, usa `a = m·k`, `b = (1 − m)·k`.
- **Nunca** elijas el prior después de ver los datos para obtener el resultado que querías.

La buena noticia: **con muchos datos, el prior apenas importa**. Con 500 éxitos y 4 500 fracasos, `Beta(1, 1)` y `Beta(2, 38)` dan
posteriores prácticamente iguales. El prior pesa cuando hay pocos datos, que es justo cuando más falta hace algo de sentido común.

## 5. Intervalos de credibilidad

Del posterior se obtiene un **intervalo de credibilidad**: el rango que contiene, por ejemplo, el 95 % de la probabilidad. Se lee
exactamente como a todo el mundo le gustaría leer un intervalo de confianza:

> "Dado el modelo y el prior, hay un 95 % de probabilidad de que la conversión real esté entre el 4,1 % y el 5,9 %."

El intervalo de confianza frecuentista **no** permite esa frase (su 95 % se refiere al procedimiento repetido, no a este intervalo).
En la práctica, con muchos datos y priors poco informativos, los dos intervalos salen casi iguales; la diferencia está en la
interpretación y en lo que pasa con pocos datos.

## 6. A/B testing bayesiano

En lugar de un valor p, el enfoque bayesiano responde directamente a las preguntas del negocio:

- **¿Qué probabilidad hay de que B sea mejor que A?**
- **¿Cuánto espero perder si elijo B y resulta ser peor?** (la *pérdida esperada*).

Se calcula fácilmente por **simulación**:

1. Posterior de cada variante: `Beta(1 + éxitos, 1 + fracasos)`.
2. Saca muchas muestras de cada posterior (por ejemplo, 20 000).
3. Cuenta en qué proporción de las simulaciones la tasa de B supera a la de A.

```python
import random
rng = random.Random(1)
gana_b = sum(rng.betavariate(1 + 80, 1 + 920) > rng.betavariate(1 + 50, 1 + 950) for _ in range(20000)) / 20000
```

Una regla de decisión típica: lanzar B si `P(B > A) > 95 %` y la pérdida esperada es menor que un umbral que no te importe asumir.

**Un mito frecuente:** "con el enfoque bayesiano puedes mirar los resultados cuando quieras". Mirar a menudo es **menos** problemático
que con valores p, pero si paras justo cuando el resultado te gusta, sigues sesgando las conclusiones. Define de antemano cuánto tiempo
o cuántos datos vas a recoger.

## 7. Medias suavizadas: rankings justos

Problema real: quieres ordenar tus vídeos (o productos, o restaurantes) por tasa de interacción. Un vídeo con 2 likes de 2 vistas
(100 %) ganaría a uno con 450 de 500 (90 %). Absurdo.

La solución bayesiana es la **media suavizada** (o *shrinkage*): usar la media del posterior con un prior basado en la media general.

```
media suavizada = (éxitos + media_prior × peso_prior) / (total + peso_prior)
```

Con una media general del 10 % y un peso de 20:

- 2 de 2 → (2 + 2) / 22 ≈ **18 %**: con tan pocos datos, se queda cerca de la media general.
- 450 de 500 → (450 + 2) / 520 ≈ **87 %**: con muchos datos, apenas se mueve.

Así ordenan muchos sitios las valoraciones con estrellas. El peso del prior dice "cuántas observaciones hacen falta para empezar a
fiarse": puedes elegirlo según el tamaño típico de tus muestras.

## 8. Bandidos multibrazo: experimentar y aprovechar a la vez

En un A/B test clásico, la mitad del tráfico va a la variante peor durante todo el experimento. Los **bandidos multibrazo** reparten el
tráfico de forma adaptativa. El método más conocido, el **muestreo de Thompson**, es puro Bayes:

1. Para cada visitante, saca una tasa aleatoria del posterior de cada variante.
2. Muéstrale la variante cuya tasa sacada sea mayor.
3. Actualiza el posterior con el resultado.

Las variantes que van mejor reciben cada vez más tráfico, pero las inciertas siguen recibiendo algo, por si acaso. Es ideal para
elegir titulares, portadas o mensajes cuando importa ganar mientras aprendes. Su contrapartida: es peor para **medir** con precisión
el tamaño del efecto.

## 9. ¿Cuándo usar cada enfoque?

| Situación | Enfoque recomendable |
|---|---|
| Pocos datos y conocimiento previo útil | Bayesiano |
| Necesitas comunicar "probabilidad de que B sea mejor" | Bayesiano |
| Rankings y tasas con tamaños muy distintos | Bayesiano (media suavizada) |
| Optimizar mientras experimentas | Bandidos (Thompson) |
| Muchos datos, prácticas establecidas, revisión externa | Frecuentista (o cualquiera: darán lo mismo) |
| No hay ningún prior defendible y hay que evitar críticas | Frecuentista o bayesiano con prior poco informativo |

No son religiones enfrentadas: son herramientas. Un buen analista entiende las dos y sabe traducir entre ellas.

## 10. Herramientas

- Para tasas, todo lo que viste se hace con `random.betavariate` o `scipy.stats.beta` (`beta.ppf` para los intervalos).
- Para modelos bayesianos completos (regresiones, modelos jerárquicos): **PyMC** o **Bambi** (que usa fórmulas como `statsmodels`).

## Resumen

- Posterior ∝ verosimilitud × prior; el posterior de hoy es el prior de mañana.
- Para tasas: prior `Beta(a, b)` + datos → `Beta(a + éxitos, b + fracasos)`.
- El prior pesa con pocos datos y se diluye con muchos; nunca se elige después de ver los resultados.
- El intervalo de credibilidad sí se interpreta como "95 % de probabilidad de que el valor esté aquí".
- A/B bayesiano: P(B > A) y pérdida esperada por simulación.
- Media suavizada para rankings justos; muestreo de Thompson para optimizar mientras aprendes.
