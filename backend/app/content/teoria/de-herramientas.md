# Linux, Git y Docker

Saber programar no basta para trabajar en un equipo ni para entregar un proyecto a un cliente. Hay tres herramientas que se dan por
supuestas en cualquier oferta de empleo y en cualquier proyecto freelance:

- **La terminal**: manejar el ordenador escribiendo comandos. Los servidores donde se ejecutan las aplicaciones no tienen ratón ni
  ventanas.
- **Git** (y GitHub): guardar el historial de tu código, trabajar en paralelo con otras personas y mostrar tu trabajo.
- **Docker**: empaquetar tu aplicación con todo lo que necesita para que funcione igual en tu ordenador, en el de un compañero y en el
  servidor.

Las tres se aprenden **usándolas**. Lee cada sección y luego repite los comandos en tu propio ordenador: este mismo proyecto (DataPath)
usa Git y Docker, así que tienes dónde practicar.

---

## 1. La terminal

### Qué es

La **terminal** (o consola) es un programa donde escribes órdenes en texto. El programa que las interpreta se llama **shell**. Los más
comunes:

- **bash** (o zsh): el estándar en Linux y macOS, y en casi todos los servidores.
- **PowerShell**: el de Windows. Muchos comandos tienen nombres distintos, aunque PowerShell acepta alias de los de Linux (`ls`, `cd`,
  `cat`).
- **WSL2** (Windows Subsystem for Linux): un Linux real dentro de Windows. Muy recomendable si vas a trabajar con servidores.

Cuando abres la terminal ves el **prompt**, que te dice en qué carpeta estás y espera tu comando:

```
PS C:\Users\Talle\Documents>          (PowerShell)
talle@pc:~/proyectos$                 (bash; ~ es tu carpeta personal)
```

### Rutas

- **Ruta absoluta**: desde la raíz del disco. `C:\Users\Talle\Documents\notas.txt` o `/home/talle/notas.txt`.
- **Ruta relativa**: desde la carpeta en la que estás. Si estás en `Documents`, la ruta relativa es simplemente `notas.txt`.
- `.` es la carpeta actual; `..` es la carpeta de arriba; `~` es tu carpeta personal.

### Comandos esenciales

| Para... | bash (Linux, macOS, WSL, Git Bash) | PowerShell (Windows) |
|---|---|---|
| Ver dónde estoy | `pwd` | `pwd` o `Get-Location` |
| Listar archivos | `ls`, `ls -la` (con ocultos y detalles) | `ls` o `Get-ChildItem`, `-Force` para ocultos |
| Entrar en una carpeta | `cd proyectos` | `cd proyectos` |
| Subir un nivel | `cd ..` | `cd ..` |
| Crear una carpeta | `mkdir datos` | `mkdir datos` |
| Crear un archivo vacío | `touch notas.txt` | `New-Item notas.txt` |
| Ver un archivo | `cat notas.txt` | `cat notas.txt` o `Get-Content` |
| Primeras / últimas líneas | `head -n 20 datos.csv`, `tail -n 20` | `Get-Content datos.csv -TotalCount 20`, `-Tail 20` |
| Seguir un log en vivo | `tail -f app.log` | `Get-Content app.log -Wait` |
| Buscar texto en archivos | `grep "ERROR" app.log` | `Select-String "ERROR" app.log` |
| Contar líneas | `wc -l datos.csv` | `(Get-Content datos.csv).Count` |
| Copiar / mover / borrar | `cp`, `mv`, `rm` | `cp`, `mv`, `rm` |
| Limpiar la pantalla | `clear` | `cls` |

`rm` borra **sin papelera**. Antes de borrar, comprueba con `ls` qué vas a borrar.

### Opciones (flags) y ayuda

Los comandos aceptan **opciones** que cambian su comportamiento, normalmente con guiones: `ls -l` (formato largo), `ls -a` (incluir
ocultos), y se pueden combinar: `ls -la`. Para ver la ayuda de un comando: `comando --help` o `man comando` en Linux, y
`Get-Help comando` en PowerShell.

### Encadenar comandos: tuberías y redirección

La **tubería** `|` pasa la salida de un comando como entrada del siguiente. Es la idea más poderosa de la terminal:

```bash
grep "ERROR" app.log | wc -l          # ¿cuántas líneas de error hay?
cat ventas.csv | head -n 5            # ver las 5 primeras filas
```

La **redirección** guarda la salida en un archivo:

```bash
python informe.py > resultado.txt     # > crea o SOBRESCRIBE el archivo
python informe.py >> historial.txt    # >> añade al final
```

### Variables de entorno en la terminal

```bash
echo $HOME                      # bash: mostrar una variable
export MODO=desarrollo          # bash: definirla en esta sesión
```

```powershell
echo $env:USERPROFILE           # PowerShell: mostrar
$env:MODO = "desarrollo"        # PowerShell: definir en esta sesión
```

Las variables definidas así duran mientras la terminal esté abierta. Volveremos a ellas en la sección 6.

### Consumir una API desde la terminal

`curl` hace peticiones HTTP. Es la forma más rápida de probar una API:

```bash
curl http://localhost:8080/api/health
curl -X POST http://localhost:8000/items -H "Content-Type: application/json" -d '{"nombre": "café"}'
```

### Comprueba que entendiste

**Pregunta:** estás en `C:\Users\Talle\Documents\proyecto\backend`. ¿Qué hace `cd ..\frontend`?

**Respuesta:** sube a `proyecto` y entra en `frontend`, es decir, te lleva a `C:\Users\Talle\Documents\proyecto\frontend`.

---

## 2. Git: los conceptos

**Git** es un sistema de **control de versiones**: guarda la historia completa de tu proyecto como una serie de "fotos". Con él puedes
volver a cualquier versión anterior, ver qué cambió y quién lo cambió, y trabajar varias personas en paralelo sin pisarse.

**GitHub** (o GitLab, Bitbucket) es un servicio en internet que **aloja** repositorios Git y añade colaboración: Pull Requests,
revisiones e issues. Git funciona sin GitHub; GitHub es donde compartes.

### Las piezas

- **Repositorio (repo):** la carpeta del proyecto junto con su historial (guardado en una carpeta oculta `.git`).
- **Commit:** una foto del proyecto en un momento dado, con un mensaje que explica qué cambió y por qué. Cada commit tiene un
  identificador único (un *hash*, como `5a0b9c2`).
- **Las tres zonas**, la idea que más cuesta al principio:

```
  Directorio de trabajo  --git add-->  Área de preparación (staging)  --git commit-->  Historial
  (tus archivos tal cual)              (lo que irá en el próximo commit)               (los commits)
```

Modificar un archivo **no** lo guarda en el historial. Primero eliges qué cambios van en el próximo commit (`git add`) y después creas
la foto (`git commit`). Así puedes hacer commits pequeños y ordenados aunque hayas cambiado muchas cosas.

- **Rama (branch):** una línea de desarrollo independiente. La principal suele llamarse `main`. Creas una rama para cada cambio
  (`feature/login`), trabajas en ella sin afectar a `main` y, cuando está lista, la **fusionas** (*merge*).
- **Remoto:** la copia del repositorio en GitHub, normalmente llamada `origin`. `push` envía tus commits al remoto; `pull` trae los
  commits nuevos del remoto.

---

## 3. Git en el día a día

### Configurar una vez

```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu@correo.com"
```

### Empezar

```bash
git init                                  # convertir la carpeta actual en un repositorio
git clone https://github.com/usuario/repo.git   # o copiar uno existente
```

### El ciclo que repetirás cientos de veces

```bash
git status                     # 1. ¿qué ha cambiado?
git diff                       # 2. ¿qué cambié exactamente? (línea a línea)
git add archivo.py             # 3. preparar un archivo (o: git add . para todo)
git commit -m "Valida el email al registrar usuarios"   # 4. crear el commit
git log --oneline              # 5. ver el historial
```

`git status` es tu mejor amigo: dice en qué rama estás, qué archivos cambiaron, cuáles están preparados y qué hacer a continuación.
Úsalo antes y después de cada comando hasta que te salga solo.

`git add -p` te muestra cada cambio por separado y te pregunta si lo incluyes. Es la mejor forma de **revisar** lo que vas a subir y
evitar commits con cosas que no querías (un `print` de depuración, una contraseña).

### Mensajes de commit

Un buen mensaje explica **qué** cambia y, si no es obvio, **por qué**. Se escribe en imperativo, como una orden:

| Malo | Bueno |
|---|---|
| `cambios` | `Corrige el cálculo del IVA en pedidos con descuento` |
| `fix` | `Evita división entre cero cuando el carrito está vacío` |
| `asdf` | `Añade la página de vocabulario de inglés` |

En el futuro (tuyo o de quien revise tu portafolio), `git log` debería contar la historia del proyecto.

### Comprueba que entendiste

**Pregunta:** modificaste `app.py` y ejecutaste `git commit -m "..."` sin hacer `git add`. ¿Qué pasa?

**Respuesta:** Git dice que no hay nada preparado para el commit (*nothing added to commit*). Los cambios siguen en tu directorio de
trabajo; primero hay que hacer `git add app.py`.

---

## 4. Ramas, fusiones y conflictos

### Trabajar en una rama

```bash
git switch -c feature/exportar-csv      # crear la rama y cambiarte a ella
# ... editas, haces add y commit las veces que haga falta ...
git switch main                         # volver a main
git merge feature/exportar-csv          # traer los cambios de la rama a main
git branch -d feature/exportar-csv      # borrar la rama ya fusionada
```

(`git switch` es la forma moderna; verás también `git checkout -b nombre` en tutoriales antiguos, que hace lo mismo.)

### Conflictos: no te asustes

Un **conflicto** aparece cuando dos ramas cambiaron **las mismas líneas** de un archivo y Git no puede decidir cuál vale. Git marca el
archivo así:

```
<<<<<<< HEAD
TASA_IVA = 0.16
=======
TASA_IVA = 0.15
>>>>>>> feature/nueva-tasa
```

- Entre `<<<<<<< HEAD` y `=======`: lo que hay en tu rama actual.
- Entre `=======` y `>>>>>>>`: lo que viene de la otra rama.

Para resolverlo:

1. Edita el archivo y deja la versión correcta (una, la otra o una combinación). **Borra las tres líneas de marcas.**
2. `git add archivo.py` para marcarlo como resuelto.
3. `git commit` para completar la fusión.

Los conflictos son normales cuando varias personas trabajan en paralelo. Se evitan en gran parte con ramas cortas que se fusionan
pronto.

---

## 5. GitHub y los Pull Requests

### Subir tu trabajo

```bash
git remote add origin https://github.com/usuario/repo.git   # una vez, si el repo empezó en local
git push -u origin feature/exportar-csv                      # la primera vez que subes una rama
git push                                                     # las siguientes
git pull                                                     # traer los cambios de otros
```

### El flujo de trabajo en equipo

1. Actualizas `main` (`git switch main` y `git pull`).
2. Creas una rama para tu tarea.
3. Haces commits pequeños.
4. Subes la rama (`git push -u origin rama`).
5. En GitHub abres un **Pull Request** (PR): una petición para fusionar tu rama en `main`, con una descripción de qué cambia y cómo se
   probó.
6. Alguien **revisa** el código y comenta. Tú corriges con más commits en la misma rama.
7. Cuando está aprobado, se fusiona.

**No trabajes directamente en `main`** en proyectos de equipo: `main` debe estar siempre en un estado que funcione, porque es lo que se
despliega.

### GitHub como portafolio

Para un perfil junior, GitHub es tu escaparate. Un reclutador mirará tus repositorios **fijados**: que tengan un README claro, commits
con mensajes que se entienden y nada de secretos ni datos de clientes.

---

## 6. Secretos, `.gitignore` y variables de entorno

### `.gitignore`

Un archivo llamado `.gitignore` en la raíz del repositorio lista lo que Git **no** debe seguir:

```
# Secretos
.env

# Entornos y dependencias
.venv/
node_modules/

# Archivos generados
__pycache__/
dist/
*.log
```

Ponlo **al crear el proyecto**: si un archivo ya fue añadido a un commit, añadirlo después al `.gitignore` no lo borra del historial.

### Si subiste un secreto por error

Imagina que subiste una API key a GitHub. Borrarla en un nuevo commit **no sirve**: sigue en el historial, y hay bots que rastrean GitHub
buscando claves en cuestión de minutos. Lo correcto, en este orden:

1. **Revoca la clave inmediatamente** en el servicio que la emitió y genera una nueva. Es lo único que realmente te protege.
2. Pon la nueva clave en una variable de entorno, nunca en el código.
3. Opcionalmente, limpia el historial (con herramientas como `git filter-repo`), sabiendo que puede haber copias.

### Variables de entorno: la configuración fuera del código

La configuración que cambia entre entornos (la URL de la base de datos, el modo de depuración) y, sobre todo, **los secretos**
(contraseñas, API keys), no se escriben en el código: se leen de **variables de entorno**.

```python
import os

url = os.environ["DATABASE_URL"]               # error (KeyError) si no existe: útil si es obligatoria
modo = os.getenv("MODO", "desarrollo")         # con valor por defecto si no existe
```

### El archivo `.env`

Escribir todas las variables a mano cada vez sería incómodo, así que en desarrollo se guardan en un archivo `.env` (que **nunca** se
sube a Git), y una librería como `python-dotenv` lo carga al arrancar. Su formato es sencillo:

```
# Configuración local
DATABASE_URL=postgresql://usuario:clave@localhost:5432/tienda
MODO=desarrollo
SALUDO="Hola, mundo"
FIRMA='Equipo DataPath'
```

Reglas del formato:

- Una variable por línea, como `NOMBRE=valor`. El nombre es lo que hay **antes del primer `=`**.
- El valor es todo lo que hay después de ese primer `=`, **aunque contenga más signos `=`** (pasa mucho en URLs y en claves en
  base64).
- Las líneas vacías y las que empiezan por `#` se ignoran.
- Los espacios alrededor suelen ignorarse, y si el valor está entre comillas simples o dobles, las comillas no forman parte del valor.

Y el patrón profesional: el `.env` real queda fuera de Git, pero subes un **`.env.example`** con los nombres de las variables y valores
de ejemplo, para que cualquiera sepa qué tiene que configurar.

---

## 7. Docker: los conceptos

### El problema que resuelve

"En mi máquina funciona". Tu aplicación depende de una versión concreta de Python, de unas librerías, de PostgreSQL, de variables de
entorno... Cuando otra persona (o el servidor) intenta ejecutarla, algo de eso es distinto y falla. Docker **empaqueta la aplicación con
todo lo que necesita** para que funcione igual en cualquier sitio.

### Las piezas

- **Imagen:** una plantilla de solo lectura con un sistema mínimo, tu código y sus dependencias. Se construye a partir de un
  **Dockerfile**.
- **Contenedor:** una imagen **en ejecución**. De una misma imagen puedes arrancar muchos contenedores. Si la imagen es la clase, el
  contenedor es el objeto.
- **Registro:** un almacén de imágenes. **Docker Hub** tiene imágenes oficiales listas para usar: `python`, `postgres`, `nginx`...
- **Volumen:** un espacio de almacenamiento que vive **fuera** del contenedor, para los datos que deben sobrevivir.

Un contenedor no es una máquina virtual completa: comparte el núcleo del sistema operativo del ordenador, por eso arranca en segundos y
pesa mucho menos.

---

## 8. El Dockerfile, línea a línea

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

| Instrucción | Qué hace |
|---|---|
| `FROM python:3.12-slim` | Parte de la imagen oficial de Python 3.12 en su versión ligera (`slim`) |
| `WORKDIR /app` | Crea la carpeta `/app` dentro de la imagen y trabaja desde ahí |
| `COPY requirements.txt .` | Copia el archivo de dependencias desde tu ordenador a la imagen |
| `RUN pip install ...` | Ejecuta un comando **al construir** la imagen (instalar las dependencias) |
| `COPY . .` | Copia el resto del código |
| `EXPOSE 8000` | Documenta en qué puerto escucha la aplicación |
| `CMD [...]` | El comando que se ejecuta **al arrancar** el contenedor |

### Por qué se copia primero `requirements.txt`

Docker construye la imagen por **capas**, una por instrucción, y guarda cada capa en caché. Si una capa no cambió, la reutiliza. Como
las dependencias cambian poco y el código cambia mucho, copiar primero `requirements.txt` e instalar consigue que, al cambiar tu código,
Docker **no reinstale todas las librerías**: solo rehace las capas desde `COPY . .`. La construcción pasa de minutos a segundos.

### `.dockerignore`

Igual que `.gitignore`, pero para lo que **no** debe copiarse a la imagen: `.venv`, `node_modules`, `.git`, `__pycache__` y, sobre todo,
`.env`. **Nunca metas secretos dentro de una imagen**: cualquiera que tenga la imagen puede leerlos.

### Comandos básicos

```bash
docker build -t mi-api .                         # construir una imagen y llamarla mi-api
docker run -p 8000:8000 mi-api                   # arrancar un contenedor
docker run -p 8000:8000 -e MODO=produccion mi-api   # con una variable de entorno
docker ps                                        # contenedores en marcha
docker logs <id>                                 # ver lo que imprimió
docker stop <id>                                 # detenerlo
```

`-p 8000:8000` conecta el puerto 8000 de tu ordenador con el 8000 del contenedor (`-p puerto_tuyo:puerto_del_contenedor`). Sin ese
mapeo, la aplicación funciona dentro del contenedor pero no puedes llegar a ella desde fuera.

---

## 9. docker compose: varios servicios a la vez

Una aplicación real tiene varias piezas: tu API, una base de datos, quizá un frontend. **docker compose** las describe todas en un
archivo `docker-compose.yml` y las levanta con un solo comando:

```yaml
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: tienda
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: tienda
    volumes:
      - datos_db:/var/lib/postgresql/data

  api:
    build: ./backend
    env_file: .env
    ports:
      - "8000:8000"
    depends_on:
      - db

volumes:
  datos_db:
```

Puntos clave:

- Cada servicio es un contenedor. `image` usa una imagen ya hecha; `build` construye una con tu Dockerfile.
- Dentro de compose, los servicios se encuentran **por su nombre**: la API se conecta a la base de datos con el host `db` (no
  `localhost`), por ejemplo `postgresql://tienda:clave@db:5432/tienda`.
- `${DB_PASSWORD}` y `env_file: .env` leen los valores de tu `.env`, así el secreto no queda escrito en el YAML.
- `depends_on` arranca `db` antes que `api` (aunque no garantiza que la base esté lista para aceptar conexiones: la aplicación debe
  reintentar, como hace el backend de DataPath).

```bash
docker compose up -d --build      # construir y arrancar todo en segundo plano
docker compose ps                 # estado de los servicios
docker compose logs -f api        # seguir los logs de un servicio
docker compose exec db psql -U tienda   # ejecutar un comando dentro de un contenedor
docker compose down               # detener y borrar los contenedores
```

---

## 10. Volúmenes: dónde viven los datos

Un contenedor es **desechable**: cuando lo borras (por ejemplo, con `docker compose down` o al reconstruirlo), todo lo que se escribió
dentro de él **desaparece**. Para una base de datos eso sería un desastre.

Un **volumen** guarda los datos fuera del contenedor. En el ejemplo de arriba, `datos_db:/var/lib/postgresql/data` dice: "la carpeta
donde PostgreSQL guarda sus datos dentro del contenedor (`/var/lib/postgresql/data`) se guarda en el volumen `datos_db`". Puedes borrar
y recrear el contenedor tantas veces como quieras: los datos siguen en el volumen.

- `docker compose down` borra contenedores, **no** volúmenes.
- `docker compose down -v` borra también los volúmenes: **los datos se pierden**. Úsalo solo cuando quieras empezar de cero.

También existen los *bind mounts* (`./mi_carpeta:/app/datos`), que conectan una carpeta de tu ordenador con una del contenedor. Son
útiles en desarrollo para que el contenedor vea tus cambios de código al instante.

### Comprueba que entendiste

**Pregunta:** levantas PostgreSQL en un contenedor sin volumen, cargas datos, haces `docker compose down` y `up`. ¿Qué encuentras?

**Respuesta:** una base de datos vacía. Sin volumen, los datos vivían dentro del contenedor y se borraron con él.

---

## 11. Cuando algo falla en Docker

1. **`docker compose ps`**: ¿el servicio está en marcha (`running`) o se reinicia en bucle (`restarting`)?
2. **`docker compose logs nombre`**: el error casi siempre está ahí. Léelo de abajo arriba, como un traceback.
3. **`docker compose exec nombre sh`**: abre una terminal **dentro** del contenedor para mirar archivos o probar comandos.

| Problema | Causa habitual |
|---|---|
| `port is already allocated` | Otro programa (u otro contenedor) ya usa ese puerto en tu ordenador. Cambia el puerto de la izquierda |
| La API no conecta con la base | Usa `localhost` en lugar del nombre del servicio (`db`), o la base aún está arrancando |
| Los cambios de código no se ven | No reconstruiste la imagen: `docker compose up -d --build` |
| Los datos desaparecieron | Falta un volumen, o se usó `down -v` |
| La imagen pesa varios GB | Falta `.dockerignore` o se usó una imagen base completa en lugar de `slim`/`alpine` |
| `Bad Gateway` en nginx tras recrear el backend | nginx guardó la dirección antigua del backend; reinicia el servicio del frontend |

---

## Resumen del capítulo

| Herramienta | Lo esencial |
|---|---|
| Terminal | Rutas relativas y absolutas; `ls`, `cd`, `cat`, `grep`; tuberías `|` y redirección `>` |
| Git | Directorio de trabajo → `add` → staging → `commit` → historial; `status` siempre |
| Ramas | Una rama por tarea; `switch -c`, `merge`; conflictos: editar, quitar marcas, `add`, `commit` |
| GitHub | `push`/`pull`; Pull Requests con revisión; `main` siempre funciona |
| Secretos | `.gitignore` desde el principio; si se filtra una clave, **revocarla**; `.env.example` sí se sube |
| Variables de entorno | `os.getenv("X", defecto)`; `.env`: `NOMBRE=valor`, el valor puede contener `=` |
| Docker | Imagen (plantilla) → contenedor (en ejecución); Dockerfile con dependencias antes que el código |
| Compose | Varios servicios en un YAML; se conectan por nombre de servicio |
| Volúmenes | Los datos de una base de datos van en un volumen o se pierden |

## Autoevaluación final

1. ¿Qué hace `grep "ERROR" app.log | wc -l`?
2. ¿Qué diferencia hay entre `git add` y `git commit`?
3. ¿Por qué no se trabaja directamente en `main`?
4. Subiste una API key a GitHub y la borraste en el commit siguiente. ¿Qué tienes que hacer?
5. En un `.env`, ¿cuál es el valor de `URL=https://api.com/?token=abc=` ?
6. ¿Qué diferencia hay entre una imagen y un contenedor?
7. ¿Por qué en el Dockerfile se copia `requirements.txt` antes que el resto del código?
8. Dentro de docker compose, ¿con qué host se conecta tu API a un servicio llamado `db`?

**Respuestas:** 1) Cuenta cuántas líneas de `app.log` contienen "ERROR". 2) `add` prepara cambios para el próximo commit; `commit` crea
la foto con lo preparado. 3) Porque `main` debe funcionar siempre (es lo que se despliega); los cambios se hacen en ramas y entran por
Pull Request. 4) Revocar la clave y crear una nueva: sigue en el historial. 5) `https://api.com/?token=abc=`: todo lo que hay después
del primer `=`. 6) La imagen es la plantilla; el contenedor es una imagen en ejecución. 7) Para aprovechar la caché de capas y no
reinstalar las dependencias cada vez que cambia el código. 8) Con `db`, el nombre del servicio.

En la práctica vas a convertir el contenido de un `.env` en un diccionario respetando todas sus reglas, y a responder sobre volúmenes y
secretos filtrados. La lista de verificación final te pide dockerizar un proyecto tuyo: hazla de verdad, es una línea muy valiosa en tu
portafolio.
