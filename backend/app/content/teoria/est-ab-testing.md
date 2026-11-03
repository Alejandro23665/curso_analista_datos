# Pruebas de hipótesis y A/B testing

Cambias el texto del botón de compra y, al día siguiente, las ventas suben un 8 %. ¿Fue el botón? ¿O era viernes, hubo una promoción de
un competidor o simplemente azar? Sin un método, cada cambio se convierte en una discusión de opiniones.

Un **A/B test** responde a esa pregunta: muestras la versión actual (A) a un grupo de usuarios y la nueva (B) a otro grupo, elegidos **al
azar**, y comparas. La estadística te dice si la diferencia observada es **real** o puede explicarse por el azar. Es la herramienta con la
que las empresas de producto toman decisiones, la usarás para evaluar cambios en tu MVP y en los sistemas de IA (¿el nuevo prompt
convierte mejor?), y es una pregunta clásica de entrevista.

No necesitas una base matemática fuerte: necesitas entender **qué significa cada número** y **qué errores evitar**. Las fórmulas son
pocas y te las doy completas.

---

## 1. Por qué hace falta la estadística: el azar

Lanza una moneda 10 veces. Aunque sea perfectamente justa, es normal obtener 6 o 7 caras. Si alguien te dice "esta moneda está trucada,
salieron 7 caras de 10", no te convencería: **con pocas observaciones, el azar produce diferencias grandes**.

Con los usuarios pasa lo mismo. Si A convierte 4,0 % y B 4,6 % con 300 usuarios cada uno, la diferencia puede ser puro azar. Con 30 000
usuarios cada uno, la misma diferencia es casi seguro real. La estadística cuantifica esa intuición.

### ¿Por qué al azar?

Si eliges tú quién ve B (por ejemplo, los usuarios de móvil, o los que llegan esta semana), cualquier diferencia podría deberse a **esa**
elección y no al cambio. La asignación **aleatoria** hace que los dos grupos sean iguales en todo (en promedio) salvo en la versión que
ven. Es lo que permite hablar de **causa**, no solo de correlación.

## 2. La lógica de una prueba de hipótesis

Se razona "por reducción al absurdo":

1. **Hipótesis nula (H₀)**: no hay diferencia; A y B convierten igual. Cualquier diferencia observada es azar.
2. **Hipótesis alternativa (H₁)**: sí hay diferencia.
3. Se calcula **qué tan raro sería** observar una diferencia como la que viste (o mayor) **si H₀ fuera cierta**. Ese número es el **valor
   p**.
4. Si es muy raro (el valor p es menor que un umbral fijado de antemano, **α**, normalmente 0,05), se **rechaza H₀**: la diferencia es
   **estadísticamente significativa**.

### Qué es (y qué no es) el valor p

Obtienes **p = 0,03**. La interpretación correcta:

> Si en realidad no hubiera ninguna diferencia entre A y B, observar una diferencia tan grande como esta (o mayor) ocurriría por azar
> aproximadamente el 3 % de las veces.

Lo que **no** significa (errores muy frecuentes, también en entrevistas):

- ❌ "Hay un 97 % de probabilidad de que B sea mejor." El valor p supone que H₀ es cierta; no da la probabilidad de las hipótesis.
- ❌ "El efecto es grande o importante." Un efecto minúsculo puede tener un valor p muy pequeño con muchos usuarios (sección 7).
- ❌ "Hay un 3 % de probabilidad de que el test esté mal hecho."

## 3. Errores tipo I y tipo II

Como decides con datos sujetos al azar, puedes equivocarte de dos formas:

| | En realidad NO hay diferencia | En realidad SÍ hay diferencia |
|---|---|---|
| **Concluyes que hay diferencia** | **Error tipo I** (falso positivo): probabilidad α | Acierto: **potencia** (1 − β) |
| **Concluyes que no hay diferencia** | Acierto | **Error tipo II** (falso negativo): probabilidad β |

- **α = 0,05**: aceptas que, cuando no hay diferencia, 1 de cada 20 tests te dirá que sí la hay.
- **Potencia del 80 %** (β = 0,20): si la diferencia existe y es del tamaño que buscas, la detectarás 8 de cada 10 veces.

Un falso positivo te hace implementar un cambio que no sirve; un falso negativo te hace descartar uno que sí servía.

## 4. Las métricas del test

Cada grupo tiene un número de usuarios (**n**) y de conversiones. La **tasa de conversión** es conversiones / n.

Ejemplo que usaremos en todo el capítulo:

| Grupo | Usuarios (n) | Conversiones | Tasa |
|---|---|---|---|
| A (actual) | 5 000 | 200 | 200 / 5 000 = **0,040** (4,0 %) |
| B (nuevo) | 5 000 | 250 | 250 / 5 000 = **0,050** (5,0 %) |

### Diferencia absoluta y mejora relativa

- **Diferencia absoluta**: 0,050 − 0,040 = 0,010, es decir, **1 punto porcentual**.
- **Mejora relativa**: cuánto mejora B **respecto a A**: (tasa_B − tasa_A) / tasa_A = 0,010 / 0,040 = **0,25**, un **25 %**.

Las dos son correctas, pero dicen cosas distintas: "subimos la conversión un 25 %" suena mucho más que "1 punto". Especifica siempre cuál
usas. (Si la tasa de A fuera 0, la mejora relativa no estaría definida.)

## 5. La prueba z de dos proporciones

Es la prueba estándar para comparar dos tasas de conversión con muestras grandes. Mide **cuántos errores estándar** separan las dos tasas.

### Paso 1: la proporción combinada

Bajo H₀ (no hay diferencia), la mejor estimación de la tasa común junta los dos grupos:

```
p = (conversiones_A + conversiones_B) / (n_A + n_B)
```

En el ejemplo: p = (200 + 250) / (5 000 + 5 000) = 450 / 10 000 = **0,045**.

### Paso 2: el error estándar

Mide cuánto variaría la diferencia entre las dos tasas solo por azar:

```
EE = √( p × (1 − p) × (1/n_A + 1/n_B) )
```

En el ejemplo: EE = √(0,045 × 0,955 × (1/5 000 + 1/5 000)) = √(0,042975 × 0,0004) ≈ **0,004146**.

### Paso 3: el estadístico z

```
z = (tasa_B − tasa_A) / EE
```

En el ejemplo: z = 0,010 / 0,004146 ≈ **2,41**. La diferencia observada es unas 2,4 veces lo que se esperaría por azar.

### Paso 4: el valor p

Para un test **bilateral** (te interesa detectar diferencias en cualquier dirección: B mejor **o peor**), el valor p es la probabilidad de
un z tan extremo como el observado, en cualquiera de los dos extremos de la distribución normal. En Python, con la librería estándar:

```python
import math
p_valor = math.erfc(abs(z) / math.sqrt(2))
```

`math.erfc` es la "función de error complementaria"; no necesitas saber cómo funciona por dentro, solo que esta fórmula convierte un z en
su valor p bilateral. Valores de referencia:

| z | valor p bilateral |
|---|---|
| 1,00 | 0,317 |
| 1,96 | **0,050** |
| 2,41 | 0,016 |
| 2,58 | 0,010 |

En el ejemplo, p ≈ **0,016** < 0,05: la diferencia es **estadísticamente significativa**. Fíjate en el número mágico: **|z| > 1,96**
equivale a p < 0,05.

### Paso 5: decidir

Con α fijado de antemano:

- Si p < α y B > A → **B gana**.
- Si p < α y B < A → **A gana** (el cambio empeora las cosas: también es un resultado útil).
- Si p ≥ α → **no hay diferencia significativa**. Ojo: eso **no** demuestra que sean iguales; solo que, con estos datos, no se puede
  distinguir la diferencia del azar.

Organizar el cálculo en funciones pequeñas (la tasa, el z, el valor p, la decisión) y reutilizarlas hace el código fácil de leer y de
probar; los tests de cada pieza pueden comprobar los valores de referencia de la tabla.

## 6. Tamaño de muestra: cuántos usuarios necesitas

La pregunta que hay que hacer **antes** de empezar: ¿cuántos usuarios necesito para detectar la mejora que me importa?

Depende de tres cosas:

- **La tasa base** (p₁): la conversión actual.
- **El efecto mínimo que te importa detectar** (MDE, *Minimum Detectable Effect*): por ejemplo, una mejora relativa del 10 %. Cuanto más
  pequeño el efecto, más usuarios necesitas.
- **α y la potencia**: con α = 0,05 y potencia del 80 %, los valores z son 1,96 y 0,84.

La fórmula aproximada por grupo:

```
n = (1,96 + 0,84)² × (p₁(1 − p₁) + p₂(1 − p₂)) / (p₂ − p₁)²
```

donde p₂ = p₁ × (1 + mejora relativa) es la tasa que esperas con B.

Ejemplo: conversión actual del 10 % y quieres detectar una mejora relativa del 20 % (p₂ = 12 %):

```
n = 2,8² × (0,10 × 0,90 + 0,12 × 0,88) / (0,02)²
  = 7,84 × (0,09 + 0,1056) / 0,0004
  = 7,84 × 0,1956 / 0,0004
  ≈ 3 833,8  →  3 834 usuarios por grupo
```

El número de usuarios es entero y no puedes quedarte corto, así que se redondea **hacia arriba** (`math.ceil`).

Si en vez del 20 % quisieras detectar una mejora del **10 %** (p₂ = 11 %), necesitarías **≈ 14 732 por grupo**: casi cuatro veces más. La
diferencia está al cuadrado en el denominador, así que **reducir el efecto a la mitad multiplica la muestra por cuatro**. Con poco
tráfico, solo puedes detectar efectos grandes; tenlo en cuenta en tu MVP.

## 7. Significativo no es importante

Con 10 millones de usuarios, un cambio sube la conversión de 4,00 % a 4,01 % con p = 0,001. Es **estadísticamente significativo**: la
diferencia es real. Pero es **minúscula**. Si implementarlo cuesta dos meses de trabajo, probablemente no compensa.

Distingue siempre:

- **Significancia estadística**: ¿la diferencia es real o azar?
- **Relevancia práctica**: ¿la diferencia es lo bastante grande para que importe al negocio?

Por eso se informa el **tamaño del efecto** (la diferencia y la mejora relativa) junto al valor p, idealmente con un **intervalo de
confianza** ("la mejora está entre +0,2 y +1,8 puntos").

## 8. Errores comunes en experimentos

### Mirar antes de tiempo (*peeking*)

Planeas un test de 3 semanas, pero lo miras cada mañana y lo detienes el día 4 porque el valor p bajó de 0,05. Problema: el valor p
**fluctúa** mientras llegan datos, y si lo miras muchas veces, tarde o temprano cruzará 0,05 **por azar**, aunque no haya diferencia. La
probabilidad real de falso positivo puede pasar del 5 % a más del 20 %.

Solución: **fija el tamaño de muestra o la duración antes de empezar** y decide solo al final. (Existen métodos "secuenciales" diseñados
para mirar durante el test, pero son otros cálculos.)

### Otros

| Error | Por qué es un problema | Qué hacer |
|---|---|---|
| Duración de días sueltos | El comportamiento cambia entre días laborables y fines de semana | **Semanas completas** (mínimo 1-2) |
| Muchas métricas a la vez | Con 20 métricas, alguna sale "significativa" por azar (1 de cada 20 con α = 0,05) | Una **métrica principal** decidida antes |
| Muchas variantes (A/B/C/D...) | Mismo problema de comparaciones múltiples | Pocas variantes, o corregir α |
| Asignación por sesión | El mismo usuario ve A y B | Asignar por **usuario** de forma estable |
| Grupos desequilibrados | Si pediste 50/50 y salió 52/48 con mucho tráfico, algo falla en la asignación | Comprobar el reparto (*sample ratio mismatch*) |
| Efecto novedad | Los usuarios prueban lo nuevo por curiosidad y luego vuelven a lo de siempre | Duración suficiente; mirar la tendencia |
| Cambiar el test a mitad | Mezcla dos experimentos | Reiniciar |

### Métricas de guarda

Además de la métrica principal, define **métricas de guarda** (*guardrails*) que **no deben empeorar**: un botón más agresivo puede subir
la conversión y también las devoluciones o las quejas. Si una métrica de guarda empeora de forma significativa, no se implementa el
cambio aunque la principal mejore.

## 9. Diseñar un test: la plantilla

Antes de lanzar cualquier experimento, escribe:

```
Hipótesis:        Mostrar el costo de envío en la página del producto (y no solo al pagar)
                  aumentará la conversión, porque reduce la sorpresa en el último paso.
Métrica principal: Conversión de visita de producto a compra.
Métricas de guarda: Ticket promedio, tasa de devoluciones.
Efecto mínimo:     Mejora relativa del 10 %.
Muestra:           N usuarios por grupo (calculado con la fórmula) → duración: 3 semanas completas.
Asignación:        50/50, al azar por id de usuario, estable.
Decisión:          Si B gana → implementar. Si A gana → descartar y documentar.
                   Si no hay diferencia → mantener A (más simple) y documentar el aprendizaje.
```

Escribir la decisión **antes** de ver los resultados evita la tentación de reinterpretar los datos a tu favor.

### Cuando no puedes hacer un A/B test

Con muy poco tráfico (un MVP con 50 usuarios), un A/B test no detectará nada salvo efectos enormes. En esa etapa, aprende más hablando con
los usuarios, viendo cómo usan el producto y midiendo la retención. Los A/B tests llegan cuando hay volumen.

---

## Resumen del capítulo

| Concepto | Lo esencial |
|---|---|
| Asignación aleatoria | Hace comparables los grupos y permite hablar de causa |
| H₀ y valor p | Probabilidad de un resultado tan extremo **si no hubiera diferencia** |
| Errores | Tipo I (falso positivo, α); tipo II (falso negativo, β); potencia = 1 − β |
| Mejora relativa | (tasa_B − tasa_A) / tasa_A |
| Prueba z | p combinada → EE = √(p(1−p)(1/n_A + 1/n_B)) → z = (tasa_B − tasa_A) / EE |
| Valor p bilateral | `math.erfc(abs(z) / math.sqrt(2))`; \|z\| > 1,96 ↔ p < 0,05 |
| Tamaño de muestra | n = (1,96 + 0,84)² × (p₁(1−p₁) + p₂(1−p₂)) / (p₂ − p₁)², hacia arriba |
| Relevancia | Significativo ≠ importante; informar el tamaño del efecto |
| Errores comunes | Mirar antes de tiempo, días sueltos, muchas métricas, asignación por sesión |
| Diseño | Hipótesis, métrica principal, guardas, efecto mínimo, muestra, duración, decisión |

## Autoevaluación final

1. ¿Por qué hay que asignar los usuarios a A o B al azar?
2. Interpreta correctamente un valor p de 0,04.
3. A convierte 8 % y B 10 %. ¿Cuál es la diferencia absoluta y la mejora relativa?
4. A: 300 conversiones de 6 000; B: 360 de 6 000. Calcula la proporción combinada.
5. Obtienes z = 1,5. ¿Es significativo con α = 0,05?
6. ¿Qué pasa con el tamaño de muestra si quieres detectar un efecto la mitad de grande?
7. Detienes un test el día 3 porque el valor p bajó de 0,05. ¿Qué problema hay?
8. Un cambio es significativo pero sube la conversión de 3,00 % a 3,02 %. ¿Lo implementas?
9. ¿Qué es una métrica de guarda? Da un ejemplo.

**Respuestas:** 1) Para que los grupos sean iguales en todo salvo en la versión, y la diferencia pueda atribuirse al cambio. 2) Si no
hubiera diferencia, un resultado tan extremo o más ocurriría por azar alrededor del 4 % de las veces. 3) 2 puntos porcentuales; mejora
relativa de 0,02 / 0,08 = 25 %. 4) (300 + 360) / 12 000 = 0,055. 5) No: |z| < 1,96 (p ≈ 0,13). 6) Se multiplica aproximadamente por
cuatro. 7) Mirar repetidamente y detenerse cuando cruza 0,05 infla mucho la probabilidad de falso positivo; hay que fijar la duración
antes. 8) Depende del costo: el efecto es real pero diminuto; si implementarlo es caro, probablemente no compensa. 9) Una métrica que no
debe empeorar aunque la principal mejore; por ejemplo, la tasa de devoluciones o de quejas.
