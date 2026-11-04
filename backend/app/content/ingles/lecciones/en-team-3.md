# Pull requests and code review

La revisión de código es **comunicación escrita entre colegas**, y en un equipo internacional ocurre en inglés y muchas veces cada día.
Un comentario técnicamente correcto pero brusco genera fricción y ralentiza al equipo; uno claro y amable lo acelera. Además, cómo
escribes las descripciones y los comentarios en GitHub es una de las primeras cosas que ve quien revisa tu portafolio.

> Lectura de la pronunciación: la **tilde** marca la sílaba fuerte, **j** es la h inglesa, **y** es la j inglesa de *job*, **ii/uu**
> son vocales largas, **z** es la th con la lengua entre los dientes, **er** es una vocal relajada con r suave.

---

## 1. La descripción de un pull request

Un **pull request** (*pul rikuést*, PR) es una solicitud para fusionar tus cambios. Su descripción debe permitir que alguien lo revise
**sin preguntarte nada**. La estructura más usada:

```
## What
Adds rate limiting to the /chat endpoint.

## Why
Some users were sending hundreds of requests per minute, which increased our LLM costs.

## How
Uses a token bucket per user (20 requests/minute). Returns 429 when the limit is exceeded.

## Testing
Added unit tests for the limiter and tested manually on staging.
```

| Sección | Qué contiene | Se pronuncia |
|---|---|---|
| What | Qué cambia, en una frase | uat |
| Why | El motivo: el problema que resuelve | uai |
| How | Cómo lo resuelve, las decisiones importantes | jau |
| Testing | Cómo lo comprobaste | tésting |

### El estilo del título y de los commits

El título de un PR y los mensajes de commit se escriben en **imperativo**, cortos y sin punto final:

| Bien | Mal |
|---|---|
| Add rate limiting to the chat endpoint | added rate limiting |
| Fix crash when the cart is empty | fixed bug |
| Update README with setup steps | changes |
| Remove unused imports | cleanup stuff |

Verbos más usados: *add* (añadir), *fix* (corregir), *update* (actualizar), *remove* (quitar), *refactor* (reestructurar), *rename*
(renombrar), *improve* (mejorar), *handle* (gestionar).

En la **descripción**, en cambio, se suele usar la tercera persona: *Adds rate limiting...* (añade), *Fixes the crash...* (corrige).

---

## 2. Comentar con tacto

La diferencia entre un buen revisor y uno que genera conflictos está en la forma:

| Brusco | Con tacto |
|---|---|
| This is wrong. | **I think** this might fail when the list is empty. **What do you think?** |
| Change this. | **Could we** move this logic to the service layer? |
| Why did you do this? | **I'm curious** about this approach. Could you explain the reasoning? |
| Bad name. | **Nit:** maybe `user_count` would be clearer than `n`. |
| You forgot the tests. | **Could you add** a test for the empty case? |
| This is slow. | **This might be** slow with large lists. **Have you considered** using a set? |

Las técnicas:

- **Habla del código, no de la persona:** *This function...* en vez de *You...*
- **Pregunta en vez de ordenar:** *Could we...?*, *What do you think about...?*, *Have you considered...?*
- **Muestra duda cuando no estés seguro:** *I think...*, *It might...*, *Maybe...*
- **Explica el porqué:** un comentario sin motivo parece un capricho.
- **Reconoce lo bueno:** *Nice approach!*, *This is much cleaner.* Un comentario positivo de vez en cuando cambia el tono de toda la
  revisión.

Pronunciación:

- *I think this might fail when the list is empty* → ai zink dis mait feil uen de list is émpti
- *Could we move this logic to the service layer?* → kud ui muuv dis lóyik tu de sérvis léier?
- *I'm curious about this approach* → aim kiúrios abáut dis apróuch
- *Have you considered using a set?* → jav iu konsíderd iúsing a set?

---

## 3. Las etiquetas de los comentarios

Muchos equipos marcan cada comentario para indicar **qué tan importante es**:

| Etiqueta | Se pronuncia | Significado |
|---|---|---|
| **Nit:** | nit | Detalle menor (estilo, nombres). No bloquea la aprobación |
| **Suggestion:** / **Optional:** | sayéschon / ópshonal | Propuesta que el autor puede ignorar |
| **Question:** | kuéschon | Pregunta para entender, no una petición de cambio |
| **Blocking:** | blóking | Hay que resolverlo antes de aprobar |
| **Praise:** | preis | Elogio |

***Nit*** viene de *nitpicking* (*nítpiking*), «buscarle tres pies al gato». Marcar algo como *nit* le dice al autor: «es un detalle, no
te preocupes demasiado».

---

## 4. Recibir comentarios

Cuando revisan **tu** código:

| Inglés | Se pronuncia | Cuándo |
|---|---|---|
| Good catch, thanks! Fixed in the latest commit. | gud kach, zanks! fikst in de léitest komít | Tenían razón y ya lo corregiste |
| Done. | dan | Cambio hecho (respuesta corta, muy común) |
| I see what you mean. | ai sii uat iu miin | Entiendes el punto |
| I went with this approach because..., but I'm open to changing it. | ai uent uid dis apróuch bikós..., bat aim óupen tu chéinying it | Explicas tu decisión sin cerrarte |
| Good point. I'll update it. | gud point. ail apdéit it | Aceptas el cambio |
| Let's discuss it in a quick call; it might be faster. | lets diskás it in a kuik kol; it mait bi fáster | Cuando el hilo se alarga |
| I'll address this in a follow-up PR. | ail adrés dis in a fólou-ap pii-ár | Lo harás en otro PR para no bloquear este |

***Good catch*** (buena observación, literalmente «buena atrapada») es la respuesta más habitual cuando alguien encuentra un error en tu
código. Es amable y reconoce el trabajo del revisor.

***I went with*** = elegí, opté por. Muy natural para explicar decisiones: *I went with PostgreSQL because...*

**Actitud:** los comentarios son sobre el código, no sobre ti. Un junior que recibe comentarios con buena actitud y aprende de ellos es
exactamente lo que buscan los equipos.

---

## 5. Aprobar o pedir cambios

| Inglés | Se pronuncia | Significado |
|---|---|---|
| LGTM | — | *Looks good to me*: aprobado |
| Approved | aprúuvd | Aprobado |
| Request changes | rikuést chéinyis | Pedir cambios antes de aprobar |
| Approved with minor comments | aprúuvd uid máinor kóments | Aprobado; los comentarios son menores |
| Ready for another look | rédi for anáder luk | Listo para otra revisión |
| PTAL | — | *Please take a look*: échale un vistazo |

---

## 6. Vocabulario de revisión

| Inglés | Se pronuncia | Español |
|---|---|---|
| to merge | tu merch | fusionar |
| to approve | tu aprúuv | aprobar |
| a merge conflict | a merch kónflikt | un conflicto al fusionar |
| to rebase | tu riibéis | rebasar (reaplicar cambios sobre otra rama) |
| a branch | a branch | una rama |
| a commit | a komít | un commit, una confirmación de cambios |
| a regression | a rigréshon | algo que funcionaba y dejó de funcionar |
| an edge case | an ech keis | un caso borde |
| backwards compatible | bákuerds kompátibel | compatible con versiones anteriores |
| readable | ríidabel | legible |
| maintainable | meintéinabel | fácil de mantener |
| a breaking change | a bréiking cheinch | un cambio que rompe la compatibilidad |
| to refactor | tu rifáktor | reestructurar el código |
| unused | aniúusd | sin usar |

---

## 7. Errores típicos de hispanohablantes

| Incorrecto | Correcto | Por qué |
|---|---|---|
| Added the tests. (título) | **Add** tests for the limiter | Títulos en imperativo |
| This is wrong, change it. | I think this might fail when... Could we...? | Brusco |
| I did this because is easier. | ...because **it's** easier. | Falta el sujeto |
| I'm agree. | I agree. / Good point. | *agree* es verbo |
| Please, check it. | Could you take a look? | Más natural |
| I will fix it in other PR. | I'll fix it in **another** PR / a follow-up PR. | *another* = otro |
| Thank you for your review, I appreciate a lot. | Thanks for the review, I really appreciate it. | Falta *it* |

---

## 8. Consejos para esta unidad

- **Escribe todos tus commits y PR en inglés**, incluso en tus proyectos personales. Es práctica diaria y queda visible en tu GitHub.
- **Lee revisiones de proyectos de código abierto** que uses (FastAPI, React): verás cientos de comentarios reales con el tono adecuado.
- **Guarda tus frases favoritas** en tus Apuntes y reutilízalas. En la revisión de código, las mismas 20 frases cubren casi todo.

---

## Comprueba que entendiste

1. ¿Qué cuatro secciones tiene la descripción de un PR?
2. ¿En qué forma verbal se escribe el título de un commit?
3. Suaviza: *Rename this variable.*
4. ¿Qué significa *Nit:* al principio de un comentario?
5. ¿Qué respondes cuando alguien encuentra un error en tu código?
6. ¿Qué es una *regression*?

**Respuestas:** 1) *What, Why, How, Testing*. 2) En imperativo: *Add...*, *Fix...* 3) Por ejemplo: *Nit: maybe `total_price` would be a
clearer name?* 4) Es un detalle menor que no bloquea la aprobación. 5) *Good catch, thanks! Fixed in the latest commit.* 6) Algo que
funcionaba y dejó de funcionar tras un cambio.
