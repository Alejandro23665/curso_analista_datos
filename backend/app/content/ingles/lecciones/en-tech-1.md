# Reading documentation

Casi toda la documentación técnica está en inglés: la de FastAPI, React, PostgreSQL, la API de Claude, las librerías de Python, los
mensajes de error. Y casi todo lo nuevo en IA aparece primero (o solo) en inglés. La buena noticia es que la documentación usa un
**vocabulario pequeño y muy repetitivo**: con unas 150 palabras y unas pocas estructuras, puedes leer la mayoría sin traductor.

Leer documentación es la habilidad de inglés **más fácil de alcanzar**: puedes ir a tu ritmo, releer y buscar. Y es la que más vas a
usar.

> Lectura de la pronunciación: la **tilde** marca la sílaba fuerte, **j** es la h inglesa, **y** es la j inglesa de *job*, **ii/uu**
> son vocales largas, **z** es la th con la lengua entre los dientes, **er** es una vocal relajada con r suave.

---

## 1. El imperativo: instrucciones directas

La documentación da instrucciones con el **verbo en forma base y sin sujeto**:

- ***Install** the package.* (instól de pákich) — Instala el paquete.
- ***Run** the server.* (ran de sérver) — Ejecuta el servidor.
- ***Set** the environment variable.* (set di inváironment vériabel) — Configura la variable de entorno.
- ***Make sure** the port is free.* (meik shur de port is frii) — Asegúrate de que el puerto está libre.
- ***Don't** commit your API key.* (dount komít iur ei-pi-ái kii) — No subas tu clave de API.

No es descortés: es el estilo normal de las instrucciones técnicas. Y es fácil: si una frase empieza por un verbo, es una instrucción.

### Verbos de instrucción más frecuentes

| Inglés | Se pronuncia | Español |
|---|---|---|
| install | instól | instalar |
| run | ran | ejecutar |
| set up | set ap | configurar, preparar |
| configure | konfíguier | configurar |
| create | kriéit | crear |
| add | ad | añadir |
| remove | rimúuv | quitar, eliminar |
| replace | ripléis | reemplazar |
| import | impórt | importar |
| call | kol | llamar (a una función) |
| pass | pas | pasar (un argumento) |
| check | chek | comprobar |
| enable / disable | inéibel / diséibel | activar / desactivar |
| make sure | meik shur | asegurarse |
| note that | nout dat | ten en cuenta que |

---

## 2. Vocabulario esencial de la documentación

### Parámetros y valores

| Inglés | Se pronuncia | Español |
|---|---|---|
| required | rikuáird | obligatorio |
| optional | ópshonal | opcional |
| default (value) | difólt (váliu) | (valor) por defecto |
| argument / parameter | árguiument / parámeter | argumento / parámetro |
| type | taip | tipo |
| string | string | texto, cadena |
| integer | ínteyer | número entero |
| boolean | búulian | booleano (verdadero/falso) |
| array / list | aréi / list | arreglo / lista |
| object | óbyekt | objeto |
| null | nal | nulo |

### Lo que hace una función

| Inglés | Se pronuncia | Español |
|---|---|---|
| returns | ritérns | devuelve |
| raises / throws (an error) | réisis / zrous | lanza (un error) |
| accepts / takes | aksépts / teiks | acepta, recibe |
| supports | supórts | es compatible con |
| deprecated | déprikeitid | obsoleto (se eliminará) |
| will be removed | uil bi rimúuvd | se eliminará |

### Las APIs web

| Inglés | Se pronuncia | Español |
|---|---|---|
| request / response | rikuést / rispóns | petición / respuesta |
| endpoint | éndpoint | ruta de una API |
| header | jéder | cabecera |
| body / payload | bódi / péiloud | cuerpo / datos enviados |
| rate limit | reit límit | límite de peticiones |
| authentication | ozentikéishon | autenticación |
| token | tóuken | token, credencial |
| timeout | táimaut | tiempo máximo de espera |

### Los avisos

| Inglés | Significa |
|---|---|
| *Note* | Nota: información útil |
| *Tip* | Consejo |
| *Warning* (*uórning*) | Advertencia: puede causar problemas |
| *Caution* (*kóshon*) | Precaución |
| *Important* | Importante |
| *Prerequisites* (*priirékuisits*) | Requisitos previos |
| *Getting started* | Primeros pasos |
| *Quickstart* | Inicio rápido |
| *Troubleshooting* (*trábelshuuting*) | Solución de problemas |

---

## 3. Desmontar una frase típica

> *"`max_tokens` (integer, **required**): the maximum number of tokens to generate **before stopping**."*

| Fragmento | Significado |
|---|---|
| *integer, required* | número entero, obligatorio |
| *the maximum number of tokens* | el número máximo de tokens |
| *to generate* | que se generarán (literalmente, «para generar») |
| *before stopping* | antes de detenerse |

Fíjate en *before **stopping***: después de **preposiciones** (*before, after, without, by, for, about*), el verbo va en **-ing**:

- *Check the logs **before deploying**.* — Revisa los logs antes de desplegar.
- *You can authenticate **by passing** a token.* — Puedes autenticarte pasando un token.
- *The request fails **without setting** the header.* — La petición falla sin configurar la cabecera.

### Otra frase típica

> *"If the request exceeds the rate limit, the API **returns** a `429` error. **We recommend** retrying with exponential backoff."*

- *If the request exceeds...* → Si la petición supera...
- *the API returns a 429 error* → la API devuelve un error 429.
- *We recommend retrying* → Recomendamos reintentar (después de *recommend*, también **-ing**).
- *with exponential backoff* → con espera exponencial.

---

## 4. Las estructuras que más se repiten

| Estructura | Ejemplo | Significado |
|---|---|---|
| **can / may** | *You **can** pass a list.* | Puedes (es posible) |
| **must / need to** | *The key **must** be a string.* | Tiene que (obligatorio) |
| **should** | *You **should** use HTTPS.* | Deberías (recomendado) |
| **will** | *This **will** create a file.* | Esto creará (resultado) |
| **If..., ...** | *If the file doesn't exist, it is created.* | Si..., ... |
| **is used to / is used for** | *This flag **is used to** enable logging.* | Sirve para |
| **Pasiva** (*is + participio*) | *The token **is sent** in the header.* | El token se envía en la cabecera |

La **voz pasiva** es muy frecuente en la documentación: *is created, is sent, is returned, is stored*. Se traduce casi siempre con «se»:
*The data **is stored** in memory* = Los datos se guardan en memoria. La verás a fondo en *Explaining an AI system*.

---

## 5. Falsos amigos de la documentación

| Inglés | Significa | No significa |
|---|---|---|
| library (*láibreri*) | biblioteca (también de código) | librería (tienda) |
| actually (*ákchuali*) | en realidad, de hecho | actualmente (*currently*) |
| eventually (*ivénchuali*) | al final, con el tiempo | eventualmente (*possibly*) |
| to support (*supórt*) | ser compatible con, dar soporte | soportar, aguantar |
| to assume (*asúum*) | suponer | asumir (responsabilidad: *take on*) |
| argument (*árguiument*) | argumento de una función; también discusión | — |
| to realize (*ríalais*) | darse cuenta | realizar (*carry out*) |
| sensible (*sénsibel*) | sensato, razonable | sensible (*sensitive*) |

Ejemplo: *"This version **supports** Python 3.12"* = Esta versión es compatible con Python 3.12. Y *"sensible defaults"* = valores
por defecto razonables.

---

## 6. Leer mensajes de error

Los mensajes de error siguen patrones fijos. Aprender a leerlos acelera muchísimo la depuración:

| Mensaje | Qué significa |
|---|---|
| `ModuleNotFoundError: No module named 'fastapi'` | No está instalado el módulo `fastapi` |
| `KeyError: 'email'` | No existe la clave `email` en el diccionario |
| `TypeError: unsupported operand type(s)` | Operación con tipos incompatibles |
| `Connection refused` | Nada escucha en esa dirección y puerto |
| `Permission denied` | No tienes permisos |
| `No such file or directory` | El archivo o la carpeta no existe |
| `Unexpected token` | Hay un carácter que no se esperaba en ese lugar |
| `... is not defined` | Usas algo que no se ha creado |
| `... is deprecated` | Funciona, pero se eliminará en el futuro |
| `Timed out` | Se agotó el tiempo de espera |

---

## 7. Estrategia para leer documentación

1. **Lee el código de los ejemplos primero.** Muchas veces se entiende antes que el texto.
2. **Busca la idea de cada párrafo**, no traduzcas palabra por palabra.
3. **Usa el traductor para frases concretas**, no para la página entera. Si traduces todo siempre, nunca aprenderás.
4. **Apunta las palabras que se repiten** en tus Apuntes. Son pocas y vuelven una y otra vez.
5. **Cambia el idioma por defecto.** Si una documentación tiene versión en español, usa la inglesa: es la más actualizada y la que
   coincide con los mensajes de error y las búsquedas.

---

## 8. Consejos para esta unidad

- **Lee 15 minutos de documentación en inglés al día** sobre lo que estás estudiando. Por ejemplo, la página *Tutorial* de FastAPI. Es
  la exposición al inglés técnico más útil que existe.
- **Lee los mensajes de error en voz alta**, completos. Además de practicar, te obliga a leerlos de verdad en vez de copiarlos al buscador
  sin mirar.
- **Escribe tus commits y README en inglés**: es la forma más rápida de que este vocabulario pase de leerlo a usarlo.

---

## Comprueba que entendiste

1. ¿Qué significa *deprecated*?
2. Traduce: *This parameter is optional. The default value is 30.*
3. ¿Por qué se dice *before stopping* y no *before stop*?
4. *"This library supports async requests."* ¿Qué quiere decir?
5. ¿Qué diferencia hay entre *must* y *should* en una documentación?
6. ¿Cómo se pronuncia *required*?

**Respuestas:** 1) Obsoleto: todavía funciona, pero se eliminará en una versión futura. 2) Este parámetro es opcional. El valor por
defecto es 30. 3) Porque después de una preposición el verbo va en *-ing*. 4) Que la librería es compatible con peticiones asíncronas.
5) *must* = obligatorio; *should* = recomendado. 6) *rikuáird*.
