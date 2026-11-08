# Regresión múltiple y regresión logística

En el tema de regresión simple ajustaste una recta con una sola variable. El mundo casi nunca es así: las ventas dependen del precio,
de la temporada, de la publicidad y del día de la semana a la vez. La **regresión múltiple** permite estudiar todas juntas y, sobre todo,
**separar** el efecto asociado a cada una. Es probablemente la herramienta estadística más usada en análisis de datos.

## 1. El modelo

```
y = b₀ + b₁·x₁ + b₂·x₂ + ... + bₖ·xₖ + error
```

Se ajusta igual que la recta simple: buscando los coeficientes que minimizan la suma de los errores al cuadrado. Ya no se hace a mano;
se usa `statsmodels` (para interpretar) o `scikit-learn` (para predecir).

## 2. Interpretar coeficientes: "manteniendo lo demás constante"

Cada coeficiente `bᵢ` es **la diferencia media en y asociada a una unidad más de xᵢ, comparando casos con los mismos valores en las demás
variables del modelo**. Esa última parte es la que da su poder a la regresión múltiple.

Ejemplo. Analizas las ventas diarias de una tienda. Con regresión simple, la publicidad parece tener un efecto enorme: cada 100 USD de
publicidad se asocian a 40 ventas más. Pero la tienda invierte más en publicidad en diciembre, cuando de todas formas vende más. Al
añadir la temporada al modelo:

```
ventas = 120 + 0,15·publicidad + 85·es_diciembre
```

El efecto de la publicidad baja a 15 ventas por cada 100 USD: parte de lo que parecía publicidad era temporada. El coeficiente de
`es_diciembre` (85) es la diferencia entre diciembre y el resto de meses **con la misma inversión en publicidad**.

Dos cuidados:

- **"Controlar" solo funciona con lo que está en el modelo.** Si falta un confusor importante, los coeficientes siguen sesgados.
- **Asociación no es causa**, aunque el modelo tenga muchas variables. Y añadir la variable equivocada (un mediador o un colisionador,
  que verás en el tema de causalidad) puede empeorar las cosas.

## 3. Variables categóricas: dummies

Una regresión necesita números. Una variable categórica como "tipo de publicación" (foto, carrusel, vídeo) se convierte en
**variables ficticias** (*dummies*): una columna 0/1 por categoría, **excepto una**, que queda como **referencia**.

| tipo | es_carrusel | es_video |
|---|---|---|
| foto | 0 | 0 |
| carrusel | 1 | 0 |
| vídeo | 0 | 1 |

Cada coeficiente se interpreta **respecto a la referencia**: si el de `es_video` es 0,8, los vídeos tienen de media 0,8 puntos más de
interacción que las fotos, con lo demás constante.

¿Por qué se quita una? Si incluyes las tres, sus columnas siempre suman 1 y son redundantes con el intercepto (es la "trampa de las
dummies"): el modelo no puede separar los efectos. Elige como referencia la categoría más natural o la más frecuente. En pandas:
`pd.get_dummies(df["tipo"], drop_first=True)`; en la fórmula de `statsmodels`, `C(tipo)` lo hace solo.

## 4. Interacciones: cuando un efecto depende de otro

A veces el efecto de una variable **cambia** según otra: los subtítulos ayudan mucho en vídeos largos y poco en cortos. Eso se modela
con un término de **interacción**, el producto de las dos variables:

```
retención = b₀ + b₁·subtítulos + b₂·duración + b₃·(subtítulos × duración)
```

Ahora el efecto de los subtítulos es `b₁ + b₃·duración`: depende de la duración. Las interacciones son fáciles de añadir y difíciles
de interpretar; inclúyelas cuando tengas una razón para esperarlas, no por probar todas.

## 5. Transformaciones: logaritmos y escalas

- **Logaritmo de y** (cuando y es positiva y asimétrica, como ventas o precios): un coeficiente `b` significa que una unidad más de x
  se asocia a un cambio de aproximadamente `100·b %` en y (exactamente `100·(e^b − 1) %`).
- **Logaritmo de x y de y:** el coeficiente es una **elasticidad**: un 1 % más de x se asocia a un `b %` más de y. Típico en precio y
  demanda.
- **Estandarizar** las variables (restar la media y dividir entre la desviación) permite comparar coeficientes de variables con
  unidades distintas: "una desviación más de X se asocia a...".
- **Relaciones curvas:** añade `x²` si el efecto crece y luego se estanca (por ejemplo, frecuencia de publicación y alcance).

## 6. Leer la salida de un modelo

Así se ve (resumida) la tabla de `statsmodels`:

```
                 coef    std err      t      P>|t|     [0.025    0.975]
Intercept      120.40      8.10    14.86    0.000     104.5     136.3
publicidad       0.15      0.04     3.75    0.000       0.07      0.23
es_diciembre    85.20     12.30     6.93    0.000      61.0     109.4
dia_finde       -4.10      6.20    -0.66    0.510     -16.3       8.1

R-squared: 0.62     Adj. R-squared: 0.61     No. Observations: 365
```

- **coef:** el efecto estimado, en unidades de y.
- **std err:** su incertidumbre. **t** = coef / std err.
- **P>|t|:** el valor p de la hipótesis "este coeficiente es 0". El fin de semana no tiene un efecto distinguible del azar (p = 0,51).
- **[0.025, 0.975]:** el intervalo de confianza del 95 %. Es lo más útil para comunicar: "cada 100 USD de publicidad se asocian a
  entre 7 y 23 ventas más".

## 7. Supuestos y diagnóstico

Los resultados de la tabla (errores estándar, valores p, intervalos) dependen de unos supuestos. Una forma de recordarlos es **LINE**:

- **L**inealidad: la relación entre cada x e y es aproximadamente lineal (o la has transformado para que lo sea).
- **I**ndependencia de los errores: falla con datos de series de tiempo o con varias filas de la misma persona.
- **N**ormalidad de los errores: importa poco con muestras grandes.
- **E**qual variance (varianza constante): la dispersión de los errores no cambia con el valor predicho.

Se comprueban **mirando los residuos** (real − predicho):

- Gráfico de residuos frente a valores predichos: debería ser una nube sin forma. Una **curva** indica que falta un término (x², una
  interacción); un **embudo** indica que la varianza crece (prueba con logaritmos o errores estándar robustos).
- Residuos en el orden del tiempo: si muestran rachas, hay autocorrelación (lo verás en series de tiempo).
- Puntos con residuos enormes o mucha influencia (en `statsmodels`, la distancia de Cook): revisa si son errores.

### Multicolinealidad

Si dos variables explicativas están muy correlacionadas (gasto en publicidad y número de anuncios), el modelo no sabe a cuál atribuir
el efecto: los coeficientes se vuelven inestables y sus intervalos enormes, aunque el modelo prediga bien. Se mide con el **VIF**
(factor de inflación de la varianza; valores por encima de 5 o 10 son una alerta). Soluciones: quedarte con una de las dos, combinarlas
en un índice o aceptar que no puedes separar sus efectos.

## 8. Sobreajuste: cuando el modelo memoriza

El R² **nunca baja** al añadir variables, aunque sean puro ruido. Con suficientes variables puedes "explicar" casi todo en tus datos y
fallar estrepitosamente con datos nuevos: es el **sobreajuste**.

- **R² ajustado:** penaliza cada variable añadida: `1 − (1 − R²)·(n − 1)/(n − k − 1)`. Si añadir una variable lo hace bajar, la variable
  no aporta lo suficiente.
- **Validación:** la prueba de verdad. Separa una parte de los datos que el modelo no ve al ajustarse y mide el error en ella
  (entrenamiento y prueba, o validación cruzada).
- **Regla práctica:** necesitas bastantes observaciones por variable (una referencia habitual son al menos 10 a 20). Con 30 filas y 15
  variables, el modelo casi seguro está sobreajustado.

## 9. Explicar o predecir: dos objetivos distintos

- **Explicar** (¿qué se asocia con qué y cuánto?): importan los coeficientes, sus intervalos y que el modelo tenga sentido. Modelos
  sencillos, variables elegidas con criterio, `statsmodels`.
- **Predecir** (¿cuánto venderemos?): importa el error con datos nuevos. Se puede usar cualquier modelo que prediga mejor, aunque no se
  pueda interpretar. `scikit-learn`, validación cruzada.

Confundirlos es habitual: un modelo que predice muy bien no te dice qué palanca mover, y un modelo con coeficientes muy claros puede
predecir mal.

## 10. Regresión logística: cuando y es sí o no

Si la variable a explicar es binaria (compra o no, se da de baja o no, el vídeo supera las 10 000 vistas o no), una recta no sirve: puede
predecir probabilidades negativas o mayores que 1. La **regresión logística** pasa la combinación lineal por una curva en forma de S, la
**función logística (sigmoide)**, que siempre da un valor entre 0 y 1:

```
z = b₀ + b₁·x₁ + ... + bₖ·xₖ
probabilidad = 1 / (1 + e^(−z))
```

### Odds y odds ratios

Los coeficientes de la logística actúan sobre las **odds** (las "probabilidades a favor"):

```
odds = p / (1 − p)          p = 0,5 → odds 1        p = 0,8 → odds 4        p = 0,2 → odds 0,25
```

Más exactamente, sobre su logaritmo: `log(odds) = z`. Por eso:

- **`e^b` es el odds ratio**: el factor por el que se multiplican las odds cuando x sube una unidad, con lo demás constante.
- `b = 0,69` → `e^0,69 ≈ 2`: las odds se duplican. `b = −0,69` → se reducen a la mitad.

Cuidado al comunicarlo: duplicar las odds **no** es duplicar la probabilidad. De 0,10 (odds 0,11) a odds 0,22 la probabilidad pasa a
0,18, casi el doble; pero de 0,50 (odds 1) a odds 2 la probabilidad pasa a 0,67. Para un público no técnico, traduce a probabilidades
en casos concretos: "un cliente típico que ve la demo pasa de un 10 % a un 18 % de probabilidad de compra".

### Evaluar un modelo logístico

No hay R² clásico. Se usan:

- **Precisión, sensibilidad y la matriz de confusión**, eligiendo un umbral (no tiene por qué ser 0,5: depende de qué error cuesta más).
- **AUC (área bajo la curva ROC):** la probabilidad de que el modelo dé más puntuación a un caso positivo que a uno negativo, elegidos
  al azar. 0,5 es azar; 1 es perfecto.
- **Calibración:** entre los casos a los que el modelo da un 30 %, ¿ocurre de verdad en torno al 30 %?

## 11. En Python

```python
import statsmodels.formula.api as smf

modelo = smf.ols("ventas ~ publicidad + C(mes) + dia_finde", data=df).fit()
print(modelo.summary())          # coeficientes, intervalos, R²
modelo.conf_int()                # intervalos de confianza

logit = smf.logit("compra ~ vio_demo + np.log(visitas) + C(canal)", data=df).fit()
np.exp(logit.params)             # odds ratios
```

## Resumen

- Cada coeficiente es el efecto asociado **con las demás variables del modelo constantes**.
- Categóricas como dummies con una referencia; interacciones cuando un efecto depende de otro.
- Logaritmos para variables positivas y asimétricas: los coeficientes pasan a ser porcentajes.
- Mira los residuos; vigila la multicolinealidad y el sobreajuste (R² ajustado y validación).
- Logística para resultados sí/no: los coeficientes son log-odds y `e^b` es el odds ratio.
- Una regresión no prueba causas: eso depende del diseño y de qué variables incluyes.
