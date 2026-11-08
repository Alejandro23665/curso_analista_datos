# Series de tiempo y tendencias

Una **serie de tiempo** es una variable medida de forma ordenada en el tiempo: ventas diarias, seguidores por semana, interés de búsqueda
mensual. Tiene algo que la hace distinta de todo lo anterior: **las observaciones no son independientes**. Lo que pasó ayer influye en
hoy. Eso cambia cómo se resume, cómo se compara y cómo se predice.

## 1. Los componentes de una serie

Casi cualquier serie se puede pensar como la combinación de cuatro partes:

- **Tendencia:** la dirección a largo plazo (tu cuenta crece, un producto pierde interés).
- **Estacionalidad:** patrones que se repiten con un periodo **fijo**: más ventas los viernes, más búsquedas de "regalos" en diciembre,
  más uso de una app educativa en época de exámenes.
- **Ciclo:** subidas y bajadas **sin** periodo fijo (los ciclos económicos).
- **Ruido:** la variación aleatoria que queda.

Cuando las partes se suman (la estacionalidad añade siempre unas 200 ventas en diciembre) el modelo es **aditivo**; cuando se
multiplican (diciembre vende un 30 % más, sea cual sea el nivel) es **multiplicativo**. Las series de negocio que crecen suelen ser
multiplicativas: su estacionalidad crece con ellas. Trabajar con el logaritmo de la serie las vuelve aditivas.

La **descomposición** separa estas partes y es lo primero que hay que hacer con una serie nueva. En Python:
`statsmodels.tsa.seasonal.seasonal_decompose(serie, period=7)` o `STL` (más robusta).

## 2. Antes de analizar: el calendario

Muchas "señales" en una serie son en realidad efectos del calendario:

- **Día de la semana:** comparar un lunes con un domingo no tiene sentido si tu negocio depende del día.
- **Meses de distinta longitud:** febrero tiene un 10 % menos de días que marzo. Compara medias diarias, no totales mensuales.
- **Festivos y fechas especiales** que cambian de fecha (Semana Santa, Black Friday).
- **Cambios de definición:** si la plataforma cambió cómo cuenta las "vistas", la serie tiene un salto que no es real.
- **Granularidad:** los datos diarios son ruidosos; los mensuales esconden detalles. Agrega según la pregunta (en pandas, `resample("W")`).

## 3. Suavizar: medias móviles

Una **media móvil** reemplaza cada punto por el promedio de una ventana de puntos vecinos. Reduce el ruido y deja ver la tendencia.

- Una media móvil de **7 días** sobre datos diarios elimina por completo el efecto del día de la semana (cada ventana contiene un
  día de cada tipo). Por eso es tan común.
- **Ventana hacia atrás** (los últimos 7 días): usable en tiempo real, pero va con retraso respecto a los cambios.
- **Ventana centrada** (3 días antes, el día y 3 después): mejor para analizar el pasado, pero no existe para los últimos días.
- **Suavizado exponencial:** da más peso a lo reciente. Reacciona antes a los cambios. En pandas: `serie.ewm(span=7).mean()`.

En pandas: `serie.rolling(7).mean()` (hacia atrás) o `serie.rolling(7, center=True).mean()` (centrada).

## 4. Medir el cambio

- **Variación porcentual** respecto al periodo anterior: `(actual − anterior) / anterior`. Cuidado: las variaciones no se suman ni se
  compensan. Subir un 10 % y bajar un 10 % te deja en el 99 % del valor inicial.
- **Variación interanual** (*year over year*, YoY): compara con el **mismo periodo del año anterior**. Es la forma más simple de
  eliminar la estacionalidad: diciembre contra diciembre.
- **Tasa de crecimiento anual compuesta (CAGR):** la tasa constante que llevaría del valor inicial al final:

```
CAGR = (final / inicial)^(1 / periodos) − 1
```

Duplicar en 3 años no es crecer un 33 % anual, sino un 26 % (1,26 × 1,26 × 1,26 ≈ 2). Es la cifra honesta para resumir un crecimiento
con altibajos.

- **Índices de base 100:** dividir toda la serie entre un valor de referencia y multiplicar por 100. Permite comparar series de escalas
  muy distintas ("desde enero, la cuenta A creció hasta 180 y la B hasta 140").

## 5. Google Trends: saber leer un índice

Google Trends no da el número de búsquedas. Da un **índice relativo**:

- El valor 100 es el **máximo** de la serie en el periodo y la región elegidos; el resto se escala respecto a él.
- Es interés **relativo** al total de búsquedas de ese momento y lugar, no volumen absoluto.
- Si comparas varios términos a la vez, el 100 es el máximo del conjunto.

Consecuencias:

- **Un pico enorme aplasta todo lo demás:** si hubo un día viral, el resto de la serie aparece cerca de 0. Cambia el periodo para verla.
- **Cambiar el periodo cambia los números:** el 100 de los últimos 12 meses no es el 100 de los últimos 5 años.
- No puedes decir "se busca el doble que en Chile" comparando dos consultas separadas: cada una tiene su propio 100.
- Los valores bajos son ruidosos (se calculan con muestras) y los términos con poco volumen aparecen como 0.

Para detectar tendencias de contenido, lo útil es la **forma**: ¿crece de forma sostenida (tendencia), sube y baja cada año (estacional)
o tiene un pico y se apaga (moda pasajera)? Una moda pasajera es una oportunidad de contenido rápido; una tendencia sostenida, de
contenido de fondo o de negocio.

## 6. Autocorrelación: por qué las series rompen las pruebas habituales

La **autocorrelación** es la correlación de una serie consigo misma desplazada en el tiempo (*lag*). La de lag 1 mide cuánto se parece
cada día al anterior; la de lag 7 en datos diarios revela la estacionalidad semanal. En pandas: `serie.autocorr(lag=7)`; para verlas
todas, el gráfico ACF (`statsmodels.graphics.tsaplots.plot_acf`).

Por qué importa:

1. **Las pruebas t y los intervalos suponen independencia.** Con datos autocorrelacionados, 365 días no equivalen a 365 observaciones
   independientes: el error estándar real es mayor y los valores p salen engañosamente pequeños.
2. **Correlaciones espurias entre series:** dos series con tendencia correlacionan casi siempre, aunque no tengan nada que ver (tus
   seguidores y el precio del café). Antes de relacionar dos series, compara sus **cambios** (`serie.diff()`) y no sus niveles, y
   desconfía de cualquier correlación entre series con tendencia.

## 7. Detectar anomalías

Para saber si un día fue "raro" hay que compararlo con lo esperable **para ese día**, no con la media general:

1. Quita la tendencia y la estacionalidad (descomposición, o compara con la media móvil y el mismo día de semanas anteriores).
2. Mira el **residuo**: si está a más de 3 desviaciones (o fuera del rango del IQR) de lo habitual, es una anomalía candidata.
3. Investiga antes de concluir: un error de registro, una caída del servicio, una campaña, un vídeo que se hizo viral.

Es la base de las alertas automáticas de métricas.

## 8. Pronosticar, con humildad

### Empieza por los modelos ingenuos

Antes de cualquier modelo sofisticado, calcula el error de los pronósticos más simples. Sorprendentemente a menudo, son difíciles de
superar:

- **Ingenuo:** mañana será como hoy.
- **Ingenuo estacional:** el próximo lunes será como el último lunes (o este diciembre como el pasado).
- **Media móvil:** el próximo valor será la media de las últimas semanas.

Si tu modelo complejo no mejora claramente al ingenuo estacional, no aporta nada.

### Modelos habituales

- **Holt-Winters** (suavizado exponencial con tendencia y estacionalidad): sencillo y sólido. `statsmodels.tsa.holtwinters.ExponentialSmoothing`.
- **ARIMA / SARIMA:** modelan la autocorrelación de forma explícita. Potentes, pero más difíciles de ajustar bien.
- **Prophet** (de Meta): pensado para datos de negocio con festivos y varias estacionalidades; fácil de usar.
- **Modelos de machine learning** con variables de calendario y retardos: útiles con muchas series o muchas variables externas.

### Evaluar bien un pronóstico

- **Nunca mezcles el futuro con el pasado:** entrena con los datos hasta una fecha y evalúa en los posteriores. Separar al azar (como en
  otros problemas de ML) hace trampa, porque el modelo "ve" el futuro.
- **Métricas:** el **MAE** (error absoluto medio, en las unidades de la serie, fácil de explicar) y el **MAPE** (error porcentual medio,
  que falla cuando hay valores cercanos a 0).
- **Da un rango, no un número:** "entre 1 200 y 1 600 ventas en diciembre (intervalo del 80 %)". El futuro es incierto y cuanto más
  lejos, más.
- Los pronósticos fallan cuando cambia el mundo (una pandemia, un cambio de algoritmo). Ningún modelo histórico lo anticipa.

## 9. En pandas

```python
serie = df.set_index("fecha")["ventas"].asfreq("D")

serie.resample("W").sum()            # agregar por semana
serie.rolling(7).mean()              # media móvil de 7 días
serie.pct_change()                   # variación respecto al día anterior
serie.pct_change(periods=365)        # variación interanual (con datos diarios)
serie.shift(7)                       # el valor de hace 7 días (para el ingenuo estacional)
serie.diff()                         # cambios en lugar de niveles
serie.autocorr(lag=7)                # autocorrelación semanal
```

## Resumen

- Una serie = tendencia + estacionalidad + ciclo + ruido; descompón antes de interpretar.
- Cuidado con el calendario: día de la semana, longitud de los meses, festivos, cambios de definición.
- Media móvil de 7 días para datos diarios; interanual para quitar la estacionalidad; CAGR para resumir crecimientos.
- Google Trends es un índice relativo con el máximo en 100: compara formas, no números absolutos.
- La autocorrelación invalida las pruebas habituales y crea correlaciones espurias: compara cambios, no niveles.
- Pronostica empezando por los modelos ingenuos, evalúa en datos posteriores y da siempre un rango.
