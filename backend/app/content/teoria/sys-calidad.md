# Pruebas, CI/CD y operación en producción

Que el código funcione en tu ordenador el día que lo escribes es el principio. Lo difícil es que **siga funcionando** cuando cambias otra
parte, cuando lo toca otra persona (o un agente de código), cuando lo usan cientos de clientes y cuando algo falla a las 3 de la mañana.

Este capítulo cubre el ciclo completo de la calidad: **pruebas** automáticas con pytest, **integración y despliegue continuos** (CI/CD)
con GitHub Actions, **despliegues seguros**, **observabilidad** (logs, métricas, errores), **copias de seguridad** y cómo actuar ante un
**incidente**. Son las prácticas que una empresa espera de un backend y las que hacen que un cliente confíe en tu trabajo.

---

## 1. Por qué pruebas automáticas

Cada cambio puede romper algo que funcionaba (una **regresión**). Sin pruebas, la única forma de saberlo es probar a mano todo cada vez,
y nadie lo hace. Con pruebas automáticas:

- **Cambias con confianza**: si rompes algo, lo sabes en segundos.
- **Documentan** cómo debe comportarse el código, con ejemplos que se ejecutan.
- **Son la red de seguridad para trabajar con agentes de código**: le dices al agente "haz que pasen las pruebas" y verificas su trabajo.
- **Encuentran los errores de los casos borde**, que son la mayoría de los errores reales.

## 2. La pirámide de pruebas

```
            /\
           /E2E\          pocas: lentas, frágiles, caras
          /------\
         /integra-\       algunas: API + base de datos real
        /  ción    \
       /------------\
      /  unitarias   \    muchas: rápidas, precisas, baratas
     /________________\
```

| Tipo | Qué prueba | Velocidad | Ejemplo |
|---|---|---|---|
| **Unitaria** | Una función o clase aislada | Milisegundos | `calcular_envio(peso, pais)` |
| **Integración** | Varias piezas juntas (API + base de datos) | Segundos | `POST /pedidos` guarda el pedido en la base |
| **E2E** (de extremo a extremo) | La aplicación completa en un navegador | Muchos segundos | Un usuario inicia sesión y compra |

La mayoría deben ser **unitarias de la lógica de negocio**: son rápidas, señalan exactamente qué falla y no se rompen por cambios de
diseño. Para que el código sea fácil de probar así, separa la lógica (funciones puras) de los efectos (HTTP, base de datos), como verás en
el capítulo de arquitectura.

## 3. pytest

```python
# app/envios.py
def costo_envio(peso_kg, pais):
    if peso_kg <= 0:
        raise ValueError("El peso debe ser positivo")
    base = 5 if pais == "Venezuela" else 15
    return base + 2 * max(0, peso_kg - 1)
```

```python
# tests/test_envios.py
import pytest
from app.envios import costo_envio

def test_envio_nacional_ligero():
    assert costo_envio(1, "Venezuela") == 5

def test_envio_internacional_con_peso_extra():
    assert costo_envio(3, "Chile") == 19          # 15 + 2 * 2

def test_peso_invalido_lanza_error():
    with pytest.raises(ValueError):
        costo_envio(0, "Venezuela")
```

Se ejecuta con `pytest` (o `pytest -v` para ver cada prueba). pytest encuentra los archivos `test_*.py` y las funciones `test_*`.

### Parametrizar: muchos casos, una prueba

```python
@pytest.mark.parametrize("peso, pais, esperado", [
    (1, "Venezuela", 5),
    (2, "Venezuela", 7),
    (1.5, "Venezuela", 6),
    (1, "Espana", 15),
])
def test_costo_envio(peso, pais, esperado):
    assert costo_envio(peso, pais) == esperado
```

### Fixtures: preparar datos compartidos

```python
@pytest.fixture
def carrito():
    return [{"producto": "Lámpara", "precio": 24.0, "cantidad": 2}]

def test_total_carrito(carrito):
    assert sum(i["precio"] * i["cantidad"] for i in carrito) == 48.0
```

### Dobles de prueba (*fakes* y *mocks*)

Para probar código que envía correos, llama a una API o a un LLM, sustituye la dependencia por una **falsa** que registra lo que recibe y
devuelve una respuesta fija. Así la prueba es rápida, gratis y determinista. Es mucho más fácil si la dependencia se **inyecta** (se pasa
como parámetro) en lugar de crearse dentro de la función: lo verás en *Arquitectura de software*.

### Qué casos probar

Para cada función, piensa en:

- **El caso normal** (el ejemplo típico).
- **Los límites**: cero, uno, el máximo, justo por encima y por debajo de un umbral (en el ejemplo, peso 1 y peso 1.5).
- **Vacíos y nulos**: lista vacía, texto vacío, `None`.
- **Entradas inválidas**: que lance el error esperado.
- **Invariantes**: propiedades que **siempre** deben cumplirse, sea cual sea la entrada. Por ejemplo, "al repartir una cantidad, las
  partes suman el total". Comprobar invariantes con muchas entradas encuentra errores que los ejemplos sueltos no ven.

### Un error clásico que solo encuentran las buenas pruebas: perder centavos

Repartir 100,00 entre 3 personas con decimales: 33,33 × 3 = 99,99. **Desapareció un centavo.** En un sistema de pagos, eso son
descuadres contables. Los dos remedios habituales:

- Trabajar con **enteros en centavos** (10 000 centavos), y repartir el **resto** de la división entera entre algunas de las partes, de
  forma que todas difieran como mucho en un centavo y la suma sea exacta.
- O, como en los hitos de pago del capítulo de freelance, calcular todas las partes menos una y que la última sea la diferencia.

En Python, la división entera `//` y el resto `%` (o `divmod`, que devuelve ambos) son las herramientas. Por ejemplo, convertir minutos
a horas y minutos:

```python
divmod(135, 60)    # (2, 15): 2 horas y 15 minutos
135 // 60, 135 % 60  # (2, 15)
```

Y la prueba de invariante correspondiente: "para muchos totales y números de partes, `sum(partes) == total` y
`max(partes) - min(partes) <= 1`".

### Cobertura

`pytest --cov` (con el plugin `pytest-cov`) mide qué líneas ejecutan las pruebas. Es útil para encontrar código **sin** probar, pero una
cobertura alta no garantiza buenas pruebas: se puede ejecutar una línea sin comprobar su resultado. Apunta a cubrir bien la lógica de
negocio, no a un número.

---

## 4. Integración continua (CI)

La **integración continua** ejecuta automáticamente las pruebas (y el *linter*) **en cada push y en cada pull request**. Así nadie fusiona
código que rompe algo, aunque se le olvide ejecutar las pruebas en local.

Con **GitHub Actions**, un archivo `.github/workflows/ci.yml`:

```yaml
name: CI
on: [push, pull_request]

jobs:
  pruebas:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -r requirements.txt
      - run: ruff check .
      - run: pytest
```

En GitHub verás una marca verde o una cruz roja en cada commit y en cada pull request. Configura la rama `main` para que **no se pueda
fusionar** un pull request con la CI en rojo.

Un repositorio con CI en verde y una insignia (*badge*) en el README es una señal inmediata de profesionalidad para quien revisa tu
portafolio.

## 5. Despliegue continuo (CD) y despliegues seguros

El **despliegue continuo** publica automáticamente cada cambio fusionado en `main` (Vercel, Railway y Render lo hacen al conectar el
repositorio). Para que sea seguro:

- **Entornos separados**: desarrollo (tu ordenador), *staging* o *preview* (una copia para probar) y producción. Vercel crea una URL de
  *preview* para cada pull request.
- **Configuración por variables de entorno**: el mismo código en todos los entornos; cambian las variables (la URL de la base, las
  claves).
- **Cambios pequeños y frecuentes**: un despliegue con un cambio es fácil de revisar y de revertir; uno con 50 cambios, no.
- **Poder volver atrás rápido** (*rollback*): saber cómo volver a la versión anterior en un clic o un comando, **antes** de necesitarlo.
- **Migraciones de base de datos compatibles** con la versión anterior del código, para que el rollback no rompa nada.
- **Comprobación de salud**: un endpoint `/health` que verifica que la app y la base responden; la plataforma lo usa para saber si el
  despliegue fue bien.

---

## 6. Observabilidad: saber qué pasa en producción

En producción no puedes poner un `print` y mirar la consola. Necesitas que la aplicación **cuente lo que hace**.

### Logs estructurados

Un log de texto libre es difícil de buscar y filtrar:

```
Usuario 42 creó el pedido 1001 por 59.90
```

Un **log estructurado** es una línea JSON con campos:

```json
{"ts": "2026-11-02T14:03:11Z", "nivel": "info", "mensaje": "pedido creado", "usuario_id": 42, "pedido_id": 1001, "total": 59.9}
```

Ahora puedes buscar "todos los errores del usuario 42" o "pedidos de más de 100" en tu herramienta de logs. En Python, `json.dumps(dict)`
convierte un diccionario en una línea JSON; y una función con `**campos` acepta cualquier número de campos con nombre:

```python
def evento(nombre, **campos):
    return {"evento": nombre, **campos}

evento("login", usuario_id=42, metodo="google")
# {'evento': 'login', 'usuario_id': 42, 'metodo': 'google'}
```

### Niveles

| Nivel | Para qué |
|---|---|
| `debug` | Detalle para desarrollar; desactivado en producción |
| `info` | Eventos normales importantes: un pedido creado, un despliegue |
| `warning` | Algo raro pero manejado: un reintento, un valor por defecto |
| `error` | Algo falló: una excepción, una petición que no se pudo completar |

### Nunca registres secretos ni datos sensibles

Los logs se copian, se envían a servicios externos y los leen muchas personas. **Nunca** deben contener contraseñas, tokens, claves de
API ni datos personales innecesarios. Como un desarrollador puede añadir un campo sensible sin pensarlo, conviene que la función de log
**redacte automáticamente** los campos peligrosos: si el **nombre** del campo contiene palabras como *password*, *token* o *secret* (sin
importar mayúsculas: `API_TOKEN`, `userPassword`), su valor se reemplaza por un marcador como `***`. Es defensa en profundidad aplicada a
los logs.

### Métricas, errores y alertas

- **Métricas**: números en el tiempo (peticiones por minuto, latencia, tasa de errores, costo de tokens por día). Dicen **cuánto** y
  **cuándo**.
- **Seguimiento de errores**: servicios como **Sentry** capturan cada excepción con su traza, el usuario y el contexto, y las agrupan.
  Saber de un error **antes** de que el cliente te escriba cambia por completo la relación.
- **Alertas**: avisos automáticos cuando algo supera un umbral ("más del 5 % de errores en 5 minutos"). Pocas y accionables: si suenan
  constantemente, se ignoran.

Las cuatro señales clásicas a vigilar: **latencia**, **tráfico**, **errores** y **saturación** (CPU, memoria, conexiones).

---

## 7. Copias de seguridad

Una copia de seguridad que **nunca has restaurado** es una esperanza, no una copia de seguridad. Muchos equipos descubren en el peor
momento que sus copias estaban vacías, incompletas o que restaurarlas tardaba un día entero.

- **Automáticas** y **fuera** del servidor de la base (si se pierde el servidor, se pierden también las copias guardadas en él).
- **Prueba periódicamente la restauración** en un entorno aparte, y **mide cuánto tarda**.
- Conoce dos números: cuántos datos puedes permitirte perder (**RPO**: si la copia es diaria, hasta un día) y cuánto tiempo puede estar
  caído el servicio (**RTO**: lo que tarda restaurar).
- Los proveedores gestionados (Neon, Supabase, RDS) ofrecen copias y restauración a un momento concreto: aprende a usarlas antes de
  necesitarlo.

---

## 8. Incidentes

Tras un despliegue, los pagos empiezan a fallar. ¿Qué haces?

1. **Mitigar primero**: restaurar el servicio es la prioridad. Lo más rápido suele ser **volver a la versión anterior** (*rollback*) o
   desactivar la funcionalidad nueva. Investigar la causa viene **después**.
2. **Comunicar**: avisar al equipo y, si afecta a los usuarios, a ellos o al cliente ("estamos al tanto y trabajando en ello").
3. **Investigar**: con los logs, las métricas y los errores, encontrar la causa. Reproducirla con una prueba.
4. **Corregir** con esa prueba incluida (para que no vuelva a pasar) y desplegar.
5. **Post-mortem sin culpables**: un documento breve con qué pasó, el impacto, la línea de tiempo, la causa raíz y las acciones para
   evitarlo. "Sin culpables" significa que se busca **qué falló en el proceso** (por qué las pruebas no lo detectaron, por qué la
   revisión no lo vio), no a quién castigar. Si la gente teme las consecuencias, esconde los errores.

---

## 9. Lista para tu proyecto

- [ ] Pruebas unitarias de la lógica principal, incluidos los casos borde.
- [ ] GitHub Actions ejecuta el linter y las pruebas en cada push.
- [ ] La configuración y los secretos vienen de variables de entorno.
- [ ] Logs estructurados sin datos sensibles.
- [ ] Seguimiento de errores (Sentry tiene un plan gratuito) y una alerta básica.
- [ ] Un endpoint `/health`.
- [ ] Sabes cómo hacer rollback.
- [ ] Probaste restaurar una copia de la base de datos.

---

## Resumen del capítulo

| Concepto | Lo esencial |
|---|---|
| Pirámide | Muchas unitarias, algunas de integración, pocas E2E |
| pytest | `assert`, `pytest.raises`, `parametrize`, fixtures |
| Casos | Normal, límites, vacíos, inválidos e invariantes |
| Dinero | Enteros en centavos; repartir el resto; probar que la suma cuadra |
| CI | Linter y pruebas en cada push/PR; no fusionar en rojo |
| CD | Entornos separados, cambios pequeños, rollback preparado, `/health` |
| Logs | Estructurados (JSON), con niveles y sin secretos (redacción automática) |
| Monitoreo | Métricas, seguimiento de errores, alertas accionables |
| Copias | Fuera del servidor y restauración probada (RPO/RTO) |
| Incidentes | Mitigar, comunicar, investigar, corregir con prueba, post-mortem sin culpables |

## Autoevaluación final

1. ¿Por qué la mayoría de las pruebas deben ser unitarias?
2. Escribe los casos que probarías para una función `descuento(total)` que da un 10 % a partir de 100.
3. ¿Qué es una invariante y por qué es útil probarla?
4. Repartes 10,00 entre 3 con decimales y redondeo. ¿Qué problema aparece y cómo se evita?
5. ¿Qué hace la integración continua y qué regla conviene activar en `main`?
6. ¿Qué ventaja tiene un log estructurado frente a uno de texto libre?
7. Un campo de log se llama `Api_Token`. ¿Qué debería hacer tu función de log?
8. Tu proveedor hace copias cada noche. ¿Qué te falta?
9. Tras un despliegue fallan los pagos. ¿Qué haces primero?

**Respuestas:** 1) Son rápidas, precisas (señalan qué falla) y baratas de mantener. 2) Por ejemplo: 50 (sin descuento), 99,99, 100 (el
límite exacto), 150, 0 y un valor negativo (error). 3) Una propiedad que siempre debe cumplirse sea cual sea la entrada; probándola con
muchas entradas se encuentran errores que los ejemplos no ven. 4) 3,33 × 3 = 9,99: se pierde un centavo; se evita con enteros en centavos
repartiendo el resto, o con la última parte como diferencia. 5) Ejecuta el linter y las pruebas en cada push y pull request; impedir
fusionar con la CI en rojo. 6) Se puede buscar y filtrar por campos. 7) Reemplazar su valor por un marcador como `***`, porque el nombre
contiene "token" (sin importar mayúsculas). 8) Probar que puedes restaurarlas y cuánto tardas. 9) Mitigar: rollback a la versión
anterior; investigar después.
