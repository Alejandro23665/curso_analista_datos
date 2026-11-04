# Trade-offs and incidents

Lo que distingue a un buen ingeniero en una entrevista o en una reunión no es conocer muchas tecnologías, sino **explicar decisiones**:
qué opciones había, qué ganas y qué pierdes con cada una, y por qué elegiste una. Y cuando algo falla en producción, **contarlo con
claridad, sin culpas** y con lo que se hizo para que no vuelva a pasar.

Esta unidad te da el lenguaje para las dos cosas: comparar opciones y contar un incidente. Es inglés de nivel B2, pero se apoya en
estructuras que ya conoces.

> Lectura de la pronunciación: la **tilde** marca la sílaba fuerte, **j** es la h inglesa, **y** es la j inglesa de *job*, **ii/uu**
> son vocales largas, **z** es la th con la lengua entre los dientes, **er** es una vocal relajada con r suave.

---

## 1. Qué es un trade-off

Un ***trade-off*** (*tréid-of*) es un **intercambio**: ganas algo a cambio de perder otra cosa. En ingeniería casi todas las decisiones lo
son: un modelo más grande es más preciso, pero más lento y caro; una caché acelera las lecturas, pero los datos pueden estar
desactualizados.

En una entrevista, una buena respuesta técnica casi siempre suena así: «**depende** de..., **por un lado**..., **por otro lado**..., **en
este caso** elegiría... **porque**...».

---

## 2. El lenguaje para comparar opciones

### Las frases clave

| Inglés | Se pronuncia | Español |
|---|---|---|
| Option A is faster, but it's more expensive. | ópshon ei is fáster, bat its mor ekspénsiv | La opción A es más rápida, pero más cara. |
| On the one hand, ... On the other hand, ... | on de uan jand... on di áder jand | Por un lado... Por otro lado... |
| It depends on... | it dipénds on | Depende de... |
| The main advantage is... | de mein advántich is | La principal ventaja es... |
| The downside is... | de dáunsaid is | La desventaja es... |
| It's a trade-off between X and Y. | its a tréid-of bituíin | Es un equilibrio entre X e Y. |
| I'd go with X because... | aid gou uid | Yo elegiría X porque... |
| even though... | íiven dóu | aunque... |
| In this case, ... | in dis keis | En este caso... |
| For a small project, ... | for a smol próyekt | Para un proyecto pequeño... |

***It depends on*** siempre lleva ***on***: ~~It depends of the volume~~ es un error muy común de los hispanohablantes.

***I'd go with*** (*aid gou uid*, yo elegiría) es la forma más natural de recomendar una opción. *I'd* = *I would*.

### Un ejemplo completo

> *"It depends on the volume of requests. On the one hand, a bigger model is more accurate. On the other hand, it's slower and more
> expensive. For a support chatbot with a few hundred questions a day, I'd go with a smaller model, because the questions are simple and
> response time matters more. Even though it's a bit less accurate, we can compensate with good retrieval and an evaluation set. If the
> evaluation showed too many errors, I'd switch to the bigger model only for the difficult questions."*

Pronunciación de las partes difíciles:

- *It depends on the volume of requests* → it dipénds on de vólium ov rikuésts
- *a bigger model is more accurate* → a bíguer módel is mor ákiurat
- *it's slower and more expensive* → its slóuer and mor ekspénsiv
- *response time matters more* → rispóns taim máters mor
- *Even though it's a bit less accurate* → íiven dóu its a bit les ákiurat
- *I'd switch to the bigger model* → aid suich tu de bíguer módel

---

## 3. Gramática: los comparativos

| Tipo de adjetivo | Comparativo | Superlativo |
|---|---|---|
| Corto (1 sílaba) | fast → **faster** | the **fastest** |
| | cheap → **cheaper** | the **cheapest** |
| | slow → **slower** | the **slowest** |
| Termina en *-y* | easy → **easier** | the **easiest** |
| Largo (2+ sílabas) | expensive → **more** expensive | the **most** expensive |
| | reliable → **more** reliable | the **most** reliable |
| | accurate → **more** accurate | the **most** accurate |
| Irregulares | good → **better** | the **best** |
| | bad → **worse** | the **worst** |
| | far → **further** | the **furthest** |

- Para comparar dos cosas se usa ***than*** (*dan*): *PostgreSQL is **more reliable than** SQLite for this.*
- **Nunca** combines las dos formas: ~~more faster~~, ~~more easier~~, ~~more better~~.
- Para decir que algo es menos: ***less*** + adjetivo largo: *less expensive*, *less accurate*. Con cortos, mejor el contrario: *slower*
  en vez de ~~less fast~~.
- Para matizar la diferencia: *a bit faster* (un poco), *much faster* / *a lot faster* (mucho), *twice as fast* (el doble de rápido).

**Pronunciación:** el *-er* se dice con la vocal relajada: *fáster*, *chíiper*, *slóuer*. Y *worse* suena *uers* (no «uors»).

---

## 4. Contar un incidente: el postmortem

Un ***postmortem*** (*poustmórtem*) o ***incident report*** es el informe de un fallo en producción: qué pasó, por qué, qué se hizo y qué
se cambiará. En la cultura de los buenos equipos son ***blameless*** (*bléimles*, sin culpables): se busca qué falló en el **proceso**,
no a quién castigar.

### La estructura

| Parte | Qué cuentas | Ejemplo |
|---|---|---|
| **What happened** | Qué vieron los usuarios y cuándo | *On Tuesday at 10 a.m., users started getting errors when they uploaded files.* |
| **Impact** | A cuántos afectó y cuánto tiempo | *About 200 users were affected for 15 minutes.* |
| **Root cause** | La causa de fondo | *The root cause was a missing environment variable after a deployment.* |
| **Resolution** | Qué se hizo para arreglarlo | *We rolled back within ten minutes.* |
| **Prevention** | Qué cambia para que no vuelva a pasar | *Since then, we've added a check to the pipeline so that it can't happen again.* |

### Un ejemplo completo

> *"On Tuesday at 10 a.m., users started getting errors when they uploaded files. About 200 users were affected. The root cause was a
> missing environment variable after a deployment: the new version couldn't connect to the storage service. We noticed it through our
> error alerts, and we rolled back within ten minutes, so the impact was limited. Since then, we've added a check to the pipeline that
> verifies all the required variables before deploying, so that it can't happen again."*

Pronunciación:

- *users started getting errors* → iúsers stártid guéting érers
- *The root cause was a missing environment variable* → de ruut kos uos a mísing inváironment vériabel
- *We noticed it through our error alerts* → ui nóutist it zruu áuer érer alérts
- *we rolled back within ten minutes* → ui rould bak uidín ten mínits
- *Since then, we've added a check to the pipeline* → sins den, uiv ádid a chek tu de páiplain
- *so that it can't happen again* → sou dat it kant jápen aguén

### La gramática del incidente

- **Pasado simple** para la secuencia de hechos: *started, rolled back, noticed*.
- **Present perfect** para los cambios que siguen vigentes hoy: *Since then, **we've added**...* (Desde entonces hemos añadido...).
- ***so that*** + *can / can't* para la finalidad: *so that it can't happen again* (para que no vuelva a pasar).
- ***within*** (*uidín*) = en menos de, dentro de: *within ten minutes* (en menos de diez minutos).

---

## 5. Vocabulario de incidentes

| Inglés | Se pronuncia | Español |
|---|---|---|
| an incident | an ínsident | un incidente |
| an outage | an áutich | una caída del servicio |
| downtime | dáuntaim | tiempo sin servicio |
| the root cause | de ruut kos | la causa raíz |
| to roll back | tu roul bak | revertir (un despliegue) |
| to mitigate | tu mítigueit | mitigar, reducir el impacto |
| to restore (the service) | tu ristór | restablecer |
| to be down | tu bi daun | estar caído |
| to be back up | tu bi bak ap | volver a funcionar |
| an alert | an alért | una alerta |
| to be on call | tu bi on kol | estar de guardia |
| to escalate | tu éskaleit | escalar (a alguien con más responsabilidad) |
| blameless | bléimles | sin culpables |
| a hotfix | a jótfiks | una corrección urgente |
| a follow-up action | a fólou-ap ákshon | una acción de seguimiento |

---

## 6. Admitir un error propio con profesionalidad

Si el incidente lo causaste tú, la forma de contarlo dice mucho de ti:

| Inglés | Se pronuncia | Español |
|---|---|---|
| That was my mistake. | dat uos mai mistéik | Fue error mío. |
| I take responsibility for that. | ai teik rispónsibiliti for dat | Asumo la responsabilidad. |
| Here's what happened and what I've changed. | jíers uat jápend and uat aiv cheinyd | Esto es lo que pasó y lo que he cambiado. |
| It won't happen again because... | it uount jápen aguén bikós | No volverá a pasar porque... |

Lo que se valora: **reconocerlo pronto**, **explicar con hechos** (sin excusas) y **proponer un cambio concreto** en el proceso.

---

## 7. Errores típicos de hispanohablantes

| Incorrecto | Correcto | Por qué |
|---|---|---|
| It depends of the volume. | It depends **on** the volume. | Preposición fija |
| It's more faster. | It's **faster**. | Comparativo corto sin *more* |
| It's more cheap than... | It's **cheaper** than... | Adjetivo corto |
| The more reliable option is... (= la más fiable) | The **most** reliable option is... | Superlativo |
| We did a rollback in ten minutes. | We **rolled back** within ten minutes. | Más natural como verbo |
| Since then, we added a check. | Since then, **we've added** a check. | Con *since then*, present perfect |
| The problem was caused for a variable. | ...caused **by** a variable. | Pasiva con *by* |

***roll back*** (dos palabras) es el **verbo**: *We rolled back.* ***rollback*** (una palabra) es el **sustantivo**: *The rollback took
ten minutes.* Lo mismo con *set up* / *setup*, *log in* / *login*, *back up* / *backup*.

---

## 8. Consejos para esta unidad

- **Prepara dos o tres decisiones técnicas de tu demo** con el formato de trade-off: *I chose X over Y because..., even though...*
  Te preguntarán por ellas en las entrevistas.
- **Escribe un postmortem de un error real tuyo**, aunque sea de un proyecto personal (una tarde perdida por una variable mal
  configurada cuenta). Es una práctica excelente y puede ir al README.
- **Usa *It depends* con cuidado:** no te quedes ahí. Di siempre **de qué** depende y **qué elegirías** en el caso concreto.

---

## Comprueba que entendiste

1. ¿Qué es un *trade-off*?
2. Corrige: *It depends of how many users we have.*
3. Forma el comparativo: *reliable*, *cheap*, *good*.
4. ¿Cuáles son las cinco partes de un postmortem?
5. ¿Por qué se dice *Since then, we've added...* y no *we added*?
6. ¿Qué diferencia hay entre *roll back* y *rollback*?

**Respuestas:** 1) Un intercambio: ganas algo a cambio de perder otra cosa. 2) *It depends on how many users we have.* 3) *more
reliable*, *cheaper*, *better*. 4) Qué pasó, el impacto, la causa raíz, la resolución y la prevención. 5) Porque *since then* conecta el
pasado con el presente: el cambio sigue vigente. 6) *roll back* es el verbo; *rollback*, el sustantivo.
