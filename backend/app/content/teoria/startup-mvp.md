# Startup: del problema al MVP

La mayoría de las startups no fracasan porque su tecnología no funcione. Fracasan porque **construyen algo que nadie necesita lo
suficiente como para pagar**. Pasan meses programando una plataforma completa, la lanzan y descubren que el problema no era tan
importante, que los clientes ya lo resolvían de otra forma o que no estaban dispuestos a pagar.

Este capítulo te enseña el proceso para reducir ese riesgo **antes** de invertir meses: elegir un problema, entrevistar a clientes sin
engañarte, construir el experimento más pequeño posible, medir con las métricas honestas y cobrar pronto. Como desarrollador, tu
tentación será empezar por el código; el método consiste justamente en retrasarlo hasta saber qué construir.

---

## 1. Empieza por el problema, no por la idea

"Una app con IA para restaurantes" es una idea. "Los restaurantes pequeños pierden pedidos por WhatsApp en las horas punta porque nadie
puede responder a tiempo" es un **problema**. Las startups que funcionan se enamoran del problema, no de su primera solución.

### Un buen problema es...

| Criterio | Pregunta |
|---|---|
| **Frecuente** | ¿Ocurre a menudo (cada día, cada semana)? |
| **Doloroso** | ¿Cuesta dinero, tiempo o clientes? ¿Cuánto? |
| **Con presupuesto** | ¿Quien lo sufre puede pagar por resolverlo? (Los negocios suelen pagar más fácilmente que las personas.) |
| **Ya se intenta resolver** | ¿Usan hojas de cálculo, personal extra, herramientas a medias? Eso demuestra que les importa |
| **Lo puedes alcanzar** | ¿Puedes hablar con estas personas y venderles? |
| **Encaja contigo** | ¿Tienes alguna ventaja: conoces el sector, tienes contactos, sabes la tecnología? |

### De dónde salen los buenos problemas

- **De tu trabajo freelance**: si tres clínicas te piden el mismo bot de recordatorios, ese problema está validado por clientes que ya
  pagaron. Es la estrategia que tienes planteada, y es de las mejores: cada proyecto es investigación de mercado pagada.
- De tu experiencia o la de gente cercana en un sector.
- De tareas manuales y repetitivas que ves hacer a negocios (copiar datos entre sistemas, responder lo mismo cien veces).
- De herramientas caras o complicadas que un segmento (por ejemplo, pymes de Latinoamérica) no puede usar bien.

## 2. Entrevistas de descubrimiento: cómo no engañarte

Si le cuentas tu idea a alguien y le preguntas "¿la usarías?", casi siempre te dirá que sí. No por mentir, sino por amabilidad y porque
imaginar un uso futuro no cuesta nada. Las opiniones sobre el futuro son **poco fiables**; los **hechos del pasado** sí lo son.

### Las reglas

1. **Habla de su vida, no de tu idea.** No presentes tu solución al principio (o en absoluto en las primeras entrevistas).
2. **Pregunta por hechos concretos del pasado**, no por opiniones ni hipótesis.
3. **Escucha más de lo que hablas.**
4. **Busca el costo real**: tiempo, dinero, clientes perdidos.

| Pregunta mala | Por qué | Pregunta buena |
|---|---|---|
| ¿Te parece buena mi idea? | Te dirán que sí por educación | Cuéntame cómo gestionas hoy las citas |
| ¿Pagarías 10 USD al mes por esto? | Prometer un pago futuro es gratis | ¿Pagas hoy por algo para resolverlo? ¿Cuánto? |
| ¿Usarías una app que...? | Hipotético | ¿Cuándo fue la última vez que te pasó? ¿Qué hiciste? |
| ¿Qué funcionalidades querrías? | Diseñan por ti, sin criterio | ¿Qué es lo más molesto de cómo lo haces ahora? |

La pregunta más valiosa: **"Cuéntame la última vez que te ocurrió este problema: ¿qué hiciste y cuánto te costó?"**. Si no recuerdan la
última vez, el problema no es frecuente. Si no hicieron nada, no es doloroso.

### Señales

- **Señales fuertes**: ya pagan por una solución parcial; han construido su propia solución con hojas de cálculo; te piden que les avises
  cuando esté listo y te dan su contacto; aceptan un piloto; **pagan por adelantado**.
- **Señales débiles** (no te fíes): "qué interesante", "yo lo usaría", "mándame información".

Haz **al menos 15-20 entrevistas** antes de escribir código. Toma notas literales y busca patrones: ¿qué problemas se repiten? ¿quién
siente más dolor? ¿cómo lo resuelven hoy?

## 3. Hipótesis: qué tiene que ser cierto

Toda startup se apoya en suposiciones. Escríbelas y ordénalas por **riesgo**:

```
1. Las clínicas pequeñas pierden al menos un 15 % de citas por ausencias.          (problema)
2. Un recordatorio por WhatsApp el día anterior reduce esas ausencias.             (solución)
3. Las clínicas pagarían 30 USD al mes por el servicio.                             (disposición a pagar)
4. Podemos conseguir clientes a un costo menor que lo que pagan en un año.          (adquisición)
```

La **más arriesgada** (la que, si es falsa, hunde todo y de la que menos evidencia tienes) es la que pruebas primero, con el experimento
más barato posible.

## 4. El MVP: el experimento más pequeño

Un **MVP** (*Minimum Viable Product*) no es "la versión 1.0 con menos funciones". Es **el experimento más pequeño que te permite aprender
si tu hipótesis más arriesgada es cierta**. A veces ni siquiera tiene código.

| Tipo de MVP | Qué es | Ejemplo |
|---|---|---|
| **Conserje** (*concierge*) | Haces el servicio **a mano** para unos pocos clientes | Envías tú los recordatorios por WhatsApp a 3 clínicas durante un mes y mides las ausencias |
| **Mago de Oz** | El cliente ve un producto "automático", pero detrás lo haces tú | Un formulario que parece una IA, y respondes tú manualmente |
| **Página de aterrizaje** | Una página que describe el producto con un botón de registro o de pago | Mides cuántos visitantes dejan su correo o pagan una reserva |
| **Producto de una sola función** | La funcionalidad central y nada más | Solo el recordatorio automático, sin panel, sin estadísticas |

En el ejemplo de las clínicas, construir durante seis meses una plataforma con app móvil sería apostar todo a hipótesis sin probar. Enviar
tú los recordatorios a mano a tres clínicas durante un mes **prueba las hipótesis 1, 2 y (si te pagan) 3** en semanas, sin programar
nada. Si funciona, automatizas lo que hacías a mano, sabiendo exactamente qué construir.

### Reglas para un MVP

- **Una sola funcionalidad central**, la que resuelve el problema. Todo lo demás (pagos integrados, modo oscuro, app móvil, panel de
  administración) espera.
- **Menos de 6 semanas** desde el inicio hasta tener usuarios reales.
- **Usa herramientas que ya conoces** y servicios existentes (autenticación, pagos, correo): no es el momento de aprender un framework
  nuevo ni de construir infraestructura.
- **Lanza cuando te dé un poco de vergüenza.** Si no te da vergüenza la primera versión, lanzaste demasiado tarde.
- **Hazlo lo bastante bueno** para que la experiencia central funcione: un MVP que no resuelve el problema no te enseña nada.

## 5. Métricas honestas

### El embudo de un producto

```
Adquisición  →  Activación  →  Retención  →  Ingresos  →  Recomendación
(llegan)        (prueban el      (vuelven)      (pagan)       (lo cuentan)
                 valor central)
```

- **Activación**: el momento en que el usuario **experimenta el valor** por primera vez. Para el bot de recordatorios: "la clínica
  configuró su agenda y se envió el primer recordatorio". Define la tuya: es mucho más útil que "se registró".
- **Retención**: si los usuarios **vuelven** después de la primera experiencia. Es la métrica más importante en esta etapa.

### Por qué la retención es la métrica clave

Tu producto pasó de 100 a 1 000 registros este mes, pero solo el **3 %** sigue activo tras dos semanas. Los registros dicen que **la
adquisición funciona** (el mensaje atrae); la retención dice que **el producto no cumple** lo que promete. Invertir en publicidad sería
llenar un cubo agujereado. Lo correcto es entender **por qué abandonan** (hablando con ellos) y arreglarlo antes de crecer.

### Análisis de cohortes

Una **cohorte** es un grupo de usuarios que empezaron en el mismo periodo (la misma semana de registro). Para cada cohorte se mide qué
fracción sigue activa en cada semana posterior:

| Cohorte (semana de registro) | Usuarios | Semana 0 | Semana 1 | Semana 2 | Semana 3 | Semana 4 |
|---|---|---|---|---|---|---|
| 6 de octubre | 40 | 100 % | 45 % | 30 % | 25 % | 25 % |
| 13 de octubre | 55 | 100 % | 50 % | 36 % | 31 % | — |
| 20 de octubre | 48 | 100 % | 56 % | 42 % | — | — |

Cómo leerla:

- La **semana 0** es la del registro: siempre 100 % (todos estuvieron activos ese día).
- **Cada fila** muestra cómo cae una cohorte con el tiempo. Lo que buscas es que la curva **se aplane** (en la primera fila, se estabiliza
  en 25 %): significa que hay un grupo de usuarios que encontró valor y se queda. Si la curva cae hasta 0, el producto no retiene a nadie.
- **Cada columna** compara cohortes en la misma semana de vida: si las cohortes recientes retienen más (45 % → 50 % → 56 % en la semana
  1), tus mejoras están funcionando.

Para calcular la retención de una semana concreta se necesita, para cada usuario, el **conjunto de semanas** en que estuvo activo; la
retención de la semana *k* es la fracción de usuarios cuyo conjunto contiene *k*. Con Python, un diccionario `{usuario: set(semanas)}`
y el operador `in` sobre cada conjunto lo resuelven; y, como siempre, hay que decidir qué devolver si no hay usuarios.

### Ingresos: MRR

En un producto de suscripción, el **MRR** (*Monthly Recurring Revenue*, ingreso recurrente mensual) es la suma de lo que pagan cada mes
las suscripciones **activas**. Las anuales se **normalizan** a su equivalente mensual (precio / 12), para no inflar el mes en que se cobran.

Ejemplo:

| Cliente | Plan | Precio | Activa | Aporte al MRR |
|---|---|---|---|---|
| Clínica Sol | mensual | 30 | sí | 30,00 |
| Clínica Luna | anual | 300 | sí | 300 / 12 = 25,00 |
| Clínica Mar | mensual | 30 | no (canceló) | 0 |
| Clínica Río | anual | 240 | sí | 240 / 12 = 20,00 |
| **MRR** | | | | **75,00** |

El MRR y su crecimiento mes a mes son las métricas que mirará cualquier inversor. Se descompone en: MRR nuevo (clientes nuevos) +
expansión (clientes que suben de plan) − contracción (bajan de plan) − churn (cancelan).

### Product-market fit

El *product-market fit* es el momento en que el mercado "tira" del producto: los usuarios se quedan (la curva de retención se aplana),
lo recomiendan, y crecer se vuelve más fácil. Una pregunta usada para medirlo: *"¿cómo te sentirías si ya no pudieras usar este
producto?"*. Si más del 40 % responde "muy decepcionado", vas por buen camino.

## 6. Cobrar pronto

Cobrar es el **experimento de validación más fiable**: alguien que paga demuestra que el problema es real.

- **Cobra desde el principio**, aunque sea poco o con descuento para los primeros clientes. "Lo hago gratis para que lo prueben" atrae a
  usuarios que no tienen el problema lo bastante fuerte.
- **Compromisos reales** antes de construir: un pago por adelantado, un piloto pagado o, al menos, una carta de intención.
- **Precio por valor**: si el bot evita 10 citas perdidas al mes a 20 USD cada una, ahorra 200 USD; cobrar 30-50 USD es fácil de
  justificar.
- **B2B** (vender a negocios) suele ser más fácil para empezar que B2C (a personas): menos clientes necesarios, más disposición a pagar y
  conoces ese mundo por tu trabajo freelance.
- Desde Venezuela, piensa en mercados donde puedas cobrar con facilidad (clientes de toda Latinoamérica, España o EE. UU.) y en las
  plataformas de pago que funcionen para ti; resuélvelo antes de lanzar.

## 7. Errores frecuentes de fundadores técnicos

| Error | Alternativa |
|---|---|
| Construir durante meses antes de hablar con clientes | 15-20 entrevistas y un MVP en menos de 6 semanas |
| Enamorarse de la tecnología (IA, microservicios, Kubernetes) | La tecnología más simple que resuelve el problema |
| Medir registros y visitas | Activación y retención por cohortes |
| No cobrar "hasta que esté terminado" | Cobrar desde el primer piloto |
| Añadir funciones para atraer usuarios | Entender por qué abandonan los actuales |
| Querer resolverlo para todo el mundo | Un segmento muy concreto primero |
| Escuchar solo lo que confirma tu idea | Buscar activamente las razones por las que no funcionaría |

---

## Resumen del capítulo

| Concepto | Lo esencial |
|---|---|
| Problema | Frecuente, doloroso, con presupuesto, ya se intenta resolver, alcanzable |
| Entrevistas | Hechos del pasado, no opiniones; "la última vez que..."; 15-20 antes de programar |
| Hipótesis | Escritas y ordenadas por riesgo; probar primero la más arriesgada |
| MVP | El experimento más pequeño: conserje, mago de Oz, página, una función |
| Activación | El momento en que el usuario experimenta el valor |
| Retención | La métrica clave; cohortes; buscar que la curva se aplane |
| MRR | Suma de suscripciones activas; anuales / 12 |
| Cobrar | Desde el principio; el pago es la validación más fiable |

## Autoevaluación final

1. Convierte la idea "una app con IA para gimnasios" en una descripción de un problema.
2. ¿Por qué "¿pagarías 10 USD al mes por esto?" es una mala pregunta? ¿Cuál la sustituye?
3. Nombra tres señales fuertes y una débil en una entrevista.
4. Quieres reducir las ausencias en clínicas. Propón un MVP que no requiera programar.
5. ¿Qué es la activación? Defínela para un asistente que responde preguntas de clientes por WhatsApp.
6. 1 000 registros, 3 % activos a las dos semanas. ¿Qué haces?
7. En una tabla de cohortes, ¿qué indica que la curva se aplane?
8. Calcula el MRR: mensual 50 activa, anual 600 activa, mensual 50 cancelada.
9. ¿Por qué conviene cobrar desde el primer piloto?

**Respuestas:** 1) Por ejemplo: "los gimnasios pequeños pierden socios porque no detectan a tiempo a los que dejan de venir". 2) Prometer
un pago futuro es gratis; mejor "¿pagas hoy por algo para resolverlo? ¿cuánto?". 3) Fuertes: ya pagan por una solución parcial, aceptan
un piloto, pagan por adelantado (o han construido su propia solución); débil: "qué interesante, yo lo usaría". 4) Un MVP conserje:
enviar tú los recordatorios a mano a unas pocas clínicas durante un mes y medir las ausencias. 5) El momento en que el usuario
experimenta el valor; por ejemplo, "el asistente respondió correctamente su primera pregunta real de un cliente". 6) No invertir en
crecer: hablar con los que abandonan, entender por qué y mejorar la retención. 7) Que un grupo de usuarios encontró valor y se queda.
8) 50 + 600 / 12 = 100. 9) Porque el pago es la prueba más fiable de que el problema es real, y filtra a quienes no lo sufren de verdad.
