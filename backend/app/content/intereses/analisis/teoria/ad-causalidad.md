# Causalidad y sesgos: cuándo un dato prueba algo

Casi todas las preguntas importantes son causales: ¿**funciona** este gancho?, ¿la publicidad **aumenta** las ventas?, ¿el curso gratuito
**trae** clientes? Y casi todos los datos que tenemos son **observacionales**: registran lo que pasó, no lo que habría pasado si
hubiéramos actuado distinto. Este capítulo trata de cómo cruzar ese puente sin engañarte, y de los sesgos que hacen que los datos
"demuestren" cosas falsas.

## 1. Qué significa "causa": el contrafactual

Decir que publicar con subtítulos **causa** más retención significa comparar dos mundos:

- El vídeo **con** subtítulos y su retención.
- **El mismo** vídeo, en el mismo momento, **sin** subtítulos y su retención.

El segundo mundo es el **contrafactual**, y nunca lo observas: cada vídeo se publicó de una sola forma. Este es el problema fundamental
de la inferencia causal. Todo método causal es una forma de **estimar el contrafactual** con algo que sí se puede observar.

Como no podemos ver el efecto en cada caso, se estima el **efecto medio**: la diferencia promedio entre los dos mundos en un grupo.

## 2. Por qué los experimentos funcionan

En un experimento (A/B test) repartes **al azar** quién recibe el tratamiento. El azar hace que los dos grupos sean, en promedio,
iguales en todo: en lo que mides y en lo que no. Así el grupo de control es una buena estimación del contrafactual del grupo tratado, y
la diferencia entre ambos es el efecto.

Es el estándar de oro. Cuando puedes hacer un experimento, hazlo. Este capítulo trata sobre todo de lo que hacer cuando no puedes: no
puedes asignar al azar la ciudad en la que vive un cliente, o el experimento sería demasiado caro, lento o poco ético.

## 3. Tres estructuras que lo explican casi todo

Ayuda dibujar las relaciones como flechas de causa a efecto (estos dibujos se llaman **DAG**, grafos acíclicos dirigidos). Con tres
variables, X (la supuesta causa), Y (el efecto) y Z (otra variable), hay tres estructuras básicas:

### Confusor (bifurcación): Z causa X y causa Y

```
       Z (interés previo en la tienda)
      ↙ ↘
     X     Y
(activa       (compra)
notificaciones)
```

Los usuarios con más interés activan las notificaciones **y** compran más. Aunque las notificaciones no hicieran nada, X e Y estarían
correlacionadas. **Hay que controlar por Z** (comparar usuarios con el mismo interés) o, mejor, experimentar.

### Mediador (cadena): X causa Z y Z causa Y

```
X (curso gratuito) → Z (confianza en la marca) → Y (ventas)
```

Z es **parte del camino** del efecto. Si quieres el efecto **total** del curso, **no** debes controlar por la confianza: al comparar
personas con la misma confianza, borras justo el mecanismo por el que actúa el curso y concluirías que "el curso no hace nada".

### Colisionador: X causa Z e Y causa Z

```
X (calidad del vídeo) → Z (se hace viral) ← Y (gancho llamativo)
```

Z es una **consecuencia común**. En el total de vídeos, calidad y gancho no tienen relación. Pero si **solo miras los virales** (es
decir, si condicionas por Z), aparece una correlación **negativa** falsa: entre los virales, los que tienen poca calidad necesariamente
tuvieron un gran gancho, y al revés. Concluirías que "la calidad y el gancho se excluyen", y es un espejismo creado por la selección.
Lo comprobarás con una simulación en los ejercicios.

**La regla:** controla por los **confusores**; **no** controles por los mediadores (si quieres el efecto total) ni por los
**colisionadores**. "Meter todas las variables en la regresión" no es una estrategia neutral: puede crear sesgos que no existían.

## 4. Los sesgos más frecuentes

### Sesgo de supervivencia

Analizar solo lo que "sobrevivió" a un filtro. El ejemplo clásico: en la Segunda Guerra Mundial se estudiaron los impactos de bala en los
aviones que **volvían** para decidir dónde reforzarlos. El estadístico Abraham Wald señaló que había que reforzar justo donde **no** había
impactos: los aviones alcanzados ahí no volvían.

En tu terreno:

- "Los vídeos virales usan música en tendencia" → ¿y los que no se hicieron virales? Quizá la usan igual.
- "Todas las startups exitosas tenían un fundador que dejó la universidad" → muchísimas fracasadas también.
- "Los creadores que publican a diario crecen" → solo ves a los que siguieron publicando; los que se agotaron no salen en la muestra.

Antídoto: pregunta siempre **qué casos faltan** en tus datos y cómo se decidió quién entraba.

### Sesgo de selección

Cuando quién entra en los datos depende de la variable que estudias. Una encuesta de satisfacción enviada solo a quienes siguen siendo
clientes no ve a los insatisfechos que se fueron. El sesgo de supervivencia es un caso particular; el colisionador es su mecanismo.

### Regresión a la media

Cuando eliges casos **por ser extremos**, en la siguiente medición tienden a acercarse a la media, aunque no hagas nada, porque parte
de su resultado extremo era azar (buena o mala suerte que no se repite).

- Los 10 vídeos con peor retención de este mes "mejoran" el siguiente tras cambiarles la miniatura.
- Las tiendas que peor vendieron el trimestre pasado mejoran tras el curso del gerente.
- El jugador que tuvo una temporada récord rinde menos la siguiente.

Es una de las fuentes más comunes de "intervenciones milagrosas". El antídoto es un **grupo de control**: otros casos igual de extremos
a los que no aplicas la intervención.

### Causalidad inversa

X e Y están relacionadas, pero es Y la que causa X. "Las cuentas que publican más tienen más seguidores": quizá tener más seguidores
(y más respuesta) es lo que motiva a publicar más.

### Confusión por el tiempo

Dos cosas que cambian a la vez en el tiempo parecen relacionadas. Si cambiaste tu estilo de vídeo en noviembre y en diciembre creció
tu cuenta, ¿fue el estilo o la temporada? Comparar "antes y después" sin un grupo de control casi nunca basta.

## 5. Métodos para estimar causas sin experimento

Todos se basan en la misma idea: encontrar un grupo de comparación que sea un buen sustituto del contrafactual. Cada uno se apoya en
un supuesto que hay que defender.

### Diferencias en diferencias

Compara el **cambio** del grupo tratado con el **cambio** de un grupo de control en el mismo periodo.

| | Antes | Después | Cambio |
|---|---|---|---|
| Ciudad con la campaña | 100 | 130 | +30 |
| Ciudad sin la campaña | 100 | 115 | +15 |
| **Efecto estimado** | | | **+15** |

El "antes y después" diría +30. Pero la ciudad sin campaña también creció 15 (la temporada, la economía), así que el efecto atribuible
a la campaña es 30 − 15 = 15.

**Supuesto clave (tendencias paralelas):** sin la campaña, las dos ciudades habrían evolucionado igual. Se vuelve creíble si, en los
meses anteriores, las dos series se movían en paralelo. Si no, el método falla.

### Discontinuidad de regresión

Cuando un tratamiento se asigna por un **umbral** (los clientes que gastan más de 500 USD reciben el estatus VIP), los que quedan justo
por encima y justo por debajo son casi idénticos. Compararlos estima el efecto del tratamiento **cerca del umbral**, como si fuera un
experimento.

### Emparejamiento (*matching*)

Para cada caso tratado se busca uno no tratado con características parecidas (edad, gasto previo, antigüedad) y se comparan las parejas.
Solo corrige los confusores que **mides**: si el confusor importante no está en tus datos, el sesgo sigue ahí.

### Variables instrumentales

Una variable que afecta al tratamiento pero no afecta al resultado por ningún otro camino (por ejemplo, un fallo técnico que dejó a
algunos usuarios sin ver un anuncio al azar). Es potente, pero encontrar un buen instrumento es difícil y su supuesto no se puede
comprobar del todo con los datos.

### Experimentos naturales

A veces el mundo hace el experimento por ti: un cambio de algoritmo que llega a unos países antes que a otros, una caída del servicio en
un día concreto. Estate atento a ellos.

## 6. ¿Y si solo tengo correlaciones? Cómo argumentar

A falta de experimento, la evidencia causal se acumula. Señales que la refuerzan (inspiradas en los criterios de Bradford Hill, usados
en epidemiología):

- **Orden temporal:** la causa precede al efecto.
- **Fuerza:** asociaciones grandes son más difíciles de explicar solo con confusores.
- **Dosis-respuesta:** más causa, más efecto (más días con subtítulos, más retención).
- **Consistencia:** aparece en distintos periodos, segmentos y datasets.
- **Mecanismo plausible:** hay una explicación de cómo X produce Y.
- **Se descartaron las alternativas:** los confusores obvios, la selección, la regresión a la media.

Y en el informe, el lenguaje importa: "se asocia con" para correlaciones; "causa" o "aumenta" solo cuando el diseño lo respalda.

## 7. Aplicado a tus redes

Quieres saber si los ganchos con pregunta funcionan. Lo que **no** sirve: comparar tus vídeos virales con los demás, mirar solo el
mes en que empezaste a usarlos, o copiar lo que hacen las cuentas grandes (sesgo de supervivencia).

Lo que **sí** sirve, de mejor a peor:

1. **Experimentar:** durante un mes, decide al azar (con una moneda o con `random`) qué vídeos llevan gancho con pregunta, y compara
   la retención a los 3 segundos. Las plataformas también permiten probar varias portadas o versiones en algunos formatos.
2. **Comparar dentro de lo comparable:** vídeos del mismo tema, duración y franja horaria, con y sin el gancho.
3. **Diferencias en diferencias** si cambias de estilo en una cuenta y no en otra que gestionas.

## Resumen

- Causa = diferencia con el **contrafactual**, que nunca se observa: hay que estimarlo.
- El experimento aleatorio es el mejor estimador; sin él, cada método depende de un supuesto.
- Controla por confusores; no por mediadores ni colisionadores.
- Sospecha siempre de: supervivencia, selección, regresión a la media, causalidad inversa y "antes y después" sin control.
- Diferencias en diferencias, discontinuidad, emparejamiento e instrumentos son las herramientas cuando no puedes experimentar.
