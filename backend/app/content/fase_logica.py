"""Lógica de programación: seguir código a mano, patrones que se repiten y cómo descomponer un problema."""
from ._helpers import checklist, parsons, predict, py, quiz

SKILL_TRAZAR = "Lógica: seguir código"
SKILL_PATRONES = "Lógica: patrones"
SKILL_PROBLEMAS = "Lógica: resolver problemas"

TOPICS = [
    # ------------------------------------------------------------------------------------------
    {
        "slug": "logica-trazar",
        "phase": "python",
        "title": "Lógica I: seguir el código a mano",
        "summary": "La tabla de variables: cómo ejecutar un programa en tu cabeza, línea a línea, para entender qué hace y por qué falla.",
        "hours": 4,
        "theory": "Ver el capítulo largo en teoria/logica-trazar.md. " * 30,
        "exercises": [
            predict(
                "lt-pred-acumula", "Un bucle que acumula", SKILL_TRAZAR,
                "Sigue el código con una tabla de variables (`i` y `total` en cada vuelta) y escribe lo que imprime.",
                """
total = 0
for i in range(1, 5):
    total = total + i
    print(i, total)
""",
                "1 1\n2 3\n3 6\n4 10",
                "`range(1, 5)` da 1, 2, 3 y 4 (el 5 no se incluye). En cada vuelta `total` suma el valor de `i`: 0+1=1, 1+2=3, 3+3=6, 6+4=10.",
                hint="Haz una tabla con columnas i y total. Recuerda que range(1, 5) no llega al 5.",
            ),
            predict(
                "lt-pred-if", "Condiciones dentro de un bucle", SKILL_TRAZAR,
                "¿Qué imprime este programa? Fíjate en el orden de las condiciones.",
                """
for n in [3, 10, 15, 7]:
    if n % 5 == 0 and n % 3 == 0:
        print("ambos")
    elif n % 5 == 0:
        print("cinco")
    elif n > 5:
        print("grande")
    else:
        print(n)
""",
                "3\ncinco\nambos\ngrande",
                "3: no es múltiplo de 5 y no es mayor que 5 → imprime 3. 10: múltiplo de 5 (no de 3) → cinco. 15: múltiplo de 5 y de 3 → ambos "
                "(se comprueba primero). 7: mayor que 5 → grande. En un if/elif solo se ejecuta la primera rama que se cumple.",
                hint="En una cadena if / elif / else solo entra en la primera condición verdadera.",
            ),
            predict(
                "lt-pred-while", "Un while con lista", SKILL_TRAZAR,
                "Sigue el bucle `while` vuelta a vuelta. ¿Qué se imprime?",
                """
numeros = [4, 8, 1, 9]
i = 0
while i < len(numeros) and numeros[i] != 1:
    numeros[i] = numeros[i] * 2
    i += 1
print(i)
print(numeros)
""",
                "2\n[8, 16, 1, 9]",
                "La condición se comprueba antes de cada vuelta. i=0: 4 != 1 → se duplica a 8. i=1: 8 != 1 → 16. i=2: numeros[2] es 1 → el bucle "
                "termina sin tocarlo. Se imprime i (2) y la lista modificada.",
                hint="El bucle se detiene en cuanto encuentra el 1. Anota la lista completa después de cada vuelta.",
            ),
            predict(
                "lt-pred-funcion", "Funciones y variables locales", SKILL_TRAZAR,
                "¿Qué imprime? Ojo con qué variable cambia dentro de la función y cuál fuera.",
                """
def duplicar(x):
    x = x * 2
    return x

a = 5
b = duplicar(a)
print(a, b)
print(duplicar(b) + a)
""",
                "5 10\n25",
                "La función recibe una copia del valor: cambiar `x` dentro no cambia `a`. `b` vale 10. En la última línea, duplicar(10) devuelve "
                "20, y 20 + 5 = 25.",
            ),
            parsons(
                "lt-ord-promedio", "Ordena: promedio de notas aprobadas", SKILL_TRAZAR,
                "Ordena las líneas para que el programa imprima el promedio de las notas **aprobadas** (5 o más). Debe imprimir `7.0`.",
                [
                    "notas = [4, 6, 9, 3, 6]",
                    "suma = 0",
                    "cuenta = 0",
                    "for nota in notas:",
                    "    if nota >= 5:",
                    "        suma = suma + nota",
                    "        cuenta = cuenta + 1",
                    "print(suma / cuenta)",
                ],
                "Primero se preparan los datos y las variables a cero (antes del bucle). Dentro del bucle, el `if` filtra y solo entonces se suma y "
                "se cuenta. El `print` va al final, fuera del bucle, cuando ya se recorrieron todas las notas: (6 + 9 + 6) / 3 = 7.0.",
                hint="Las variables que acumulan se crean antes del bucle, y el resultado se imprime después.",
            ),
            quiz(
                "lt-quiz-tabla", "Para qué sirve la tabla de variables", SKILL_TRAZAR,
                "Tu función devuelve un resultado incorrecto y no entiendes por qué. ¿Qué es lo más útil primero?",
                [
                    "Reescribir la función entera desde cero",
                    "Seguirla a mano con una tabla de variables (o con print) usando un ejemplo pequeño y comparar con lo que esperabas en cada paso",
                    "Pedirle a un asistente de IA que la arregle sin leerla",
                    "Probar con datos más grandes",
                ],
                1,
                "Con un ejemplo pequeño y una tabla de variables ves en qué línea exacta el valor real se separa del esperado: ahí está el error.",
            ),
        ],
    },
    # ------------------------------------------------------------------------------------------
    {
        "slug": "logica-patrones",
        "phase": "python",
        "title": "Lógica II: los patrones que se repiten",
        "summary": "Contador, acumulador, máximo, bandera y búsqueda: cinco recetas que resuelven la mayoría de los ejercicios con bucles.",
        "hours": 5,
        "theory": "Ver el capítulo largo en teoria/logica-patrones.md. " * 30,
        "exercises": [
            py(
                "lp-contar-largas", "Contador: palabras largas", SKILL_PATRONES,
                "Escribe `contar_largas(palabras, minimo)` que devuelva **cuántas** palabras tienen `minimo` letras o más. "
                "Usa el patrón **contador** (no uses `len` sobre una lista filtrada ni `sum`).",
                """
def contar_largas(palabras, minimo):
    # contador = 0 antes del bucle; dentro, suma 1 cuando se cumpla la condición
    pass
""",
                """
def contar_largas(palabras, minimo):
    contador = 0
    for palabra in palabras:
        if len(palabra) >= minimo:
            contador += 1
    return contador
""",
                """
assert contar_largas(["sol", "montaña", "río", "ciudad"], 5) == 2, "montaña y ciudad tienen 5 letras o más"
assert contar_largas(["hola"], 4) == 1, "4 letras cumple 'minimo 4' (>=)"
assert contar_largas([], 3) == 0, "con una lista vacía, el contador se queda en 0"
assert contar_largas(["a", "bb"], 10) == 0
""",
                hint="Cuidado con >= frente a >: 'minimo letras o más' incluye el propio mínimo.",
            ),
            py(
                "lp-mayor-gasto", "Máximo: el mayor gasto y su día", SKILL_PATRONES,
                "Escribe `mayor_gasto(gastos)` que reciba una lista de tuplas `(dia, importe)` y devuelva la tupla con el **mayor importe**. "
                "Si hay empate, la primera que aparece. Si la lista está vacía, devuelve `None`. Hazlo con el patrón **máximo** (sin `max` ni `sorted`).",
                """
def mayor_gasto(gastos):
    pass
""",
                """
def mayor_gasto(gastos):
    if not gastos:
        return None
    mejor = gastos[0]
    for gasto in gastos[1:]:
        if gasto[1] > mejor[1]:
            mejor = gasto
    return mejor
""",
                """
assert mayor_gasto([("lun", 20), ("mar", 55), ("mie", 30)]) == ("mar", 55)
assert mayor_gasto([("lun", 40), ("mar", 40)]) == ("lun", 40), "con empate gana la primera: usa > y no >="
assert mayor_gasto([]) is None, "lista vacía -> None"
assert mayor_gasto([("dom", -5), ("lun", -2)]) == ("lun", -2), "si empiezas con mejor = 0, los negativos fallan"
""",
                hint="Empieza con el primer elemento como 'mejor hasta ahora', no con 0: así funciona también con números negativos.",
            ),
            py(
                "lp-todos-validos", "Bandera: ¿todos los correos son válidos?", SKILL_PATRONES,
                "Escribe `todos_validos(correos)` que devuelva `True` si **todos** los textos contienen exactamente una `@` y al menos un `.` "
                "después de ella, y `False` si alguno no cumple. Una lista vacía devuelve `True`. Usa el patrón **bandera** o sal en cuanto "
                "encuentres uno inválido.",
                """
def todos_validos(correos):
    pass
""",
                """
def todos_validos(correos):
    for correo in correos:
        if correo.count("@") != 1:
            return False
        dominio = correo.split("@")[1]
        if "." not in dominio:
            return False
    return True
""",
                """
assert todos_validos(["ana@mail.com", "luis@empresa.org"]) is True
assert todos_validos(["ana@mail.com", "luis.empresa.org"]) is False, "falta la @"
assert todos_validos(["ana@@mail.com"]) is False, "dos @"
assert todos_validos(["ana.perez@mail"]) is False, "el punto tiene que estar después de la @"
assert todos_validos([]) is True, "si no hay ninguno, ninguno es inválido"
""",
                hint="Para «todos cumplen», busca uno que no cumpla: en cuanto aparezca, la respuesta ya es False.",
            ),
            py(
                "lp-primer-repetido", "Búsqueda: el primer pedido repetido", SKILL_PATRONES,
                "Escribe `primer_repetido(ids)` que devuelva el **primer id que aparece por segunda vez** al recorrer la lista, o `None` si no se "
                "repite ninguno. Ejemplo: `[7, 3, 9, 3, 7]` → `3` (el 3 se repite antes que el 7).",
                """
def primer_repetido(ids):
    pass
""",
                """
def primer_repetido(ids):
    vistos = set()
    for x in ids:
        if x in vistos:
            return x
        vistos.add(x)
    return None
""",
                """
assert primer_repetido([7, 3, 9, 3, 7]) == 3
assert primer_repetido([1, 2, 3]) is None
assert primer_repetido([5, 5]) == 5
assert primer_repetido([]) is None
""",
                hint="Guarda en un conjunto lo que ya viste. Comprueba si el actual ya estaba ANTES de añadirlo.",
            ),
            predict(
                "lp-pred-bandera", "¿Qué imprime? Una bandera mal colocada", SKILL_PATRONES,
                "Este código quiere saber si hay algún número negativo, pero tiene un error clásico. ¿Qué imprime?",
                """
numeros = [3, -1, 4, 5]
hay_negativo = False
for n in numeros:
    if n < 0:
        hay_negativo = True
    else:
        hay_negativo = False
print(hay_negativo)
""",
                "False",
                "La bandera se vuelve a poner en False en cada número positivo: el -1 la pone a True, pero el 4 la devuelve a False. Una bandera "
                "solo se cambia en un sentido (de False a True) dentro del bucle; el valor inicial va antes del bucle y no hay `else`.",
            ),
            parsons(
                "lp-ord-agrupar", "Ordena: agrupar por categoría", SKILL_PATRONES,
                "Ordena las líneas para contar cuántos productos hay de cada categoría. Debe imprimir `{'libro': 2, 'hogar': 1}`.",
                [
                    "productos = [('novela', 'libro'), ('lampara', 'hogar'), ('atlas', 'libro')]",
                    "conteo = {}",
                    "for nombre, categoria in productos:",
                    "    if categoria not in conteo:",
                    "        conteo[categoria] = 0",
                    "    conteo[categoria] += 1",
                    "print(conteo)",
                ],
                "Es el patrón contador, pero con un contador por categoría en un diccionario: antes de sumar hay que crear la clave si no existe.",
            ),
        ],
    },
    # ------------------------------------------------------------------------------------------
    {
        "slug": "logica-descomponer",
        "phase": "python",
        "title": "Lógica III: cómo resolver un problema que no sabes resolver",
        "summary": "Entender el enunciado, hacer ejemplos a mano, descomponer en pasos, escribir pseudocódigo y probar con casos borde.",
        "hours": 5,
        "theory": "Ver el capítulo largo en teoria/logica-descomponer.md. " * 30,
        "exercises": [
            py(
                "ld-validar-clave", "Descomponer: validar una contraseña", SKILL_PROBLEMAS,
                "Escribe `errores_clave(clave)` que devuelva una **lista con los problemas** de una contraseña, en este orden:\n\n"
                "1. `'corta'` si tiene menos de 8 caracteres.\n"
                "2. `'sin numero'` si no tiene ningún dígito.\n"
                "3. `'sin mayuscula'` si no tiene ninguna letra mayúscula.\n\n"
                "Si es válida, devuelve una lista vacía. Descompón: cada regla es un paso independiente.",
                """
def errores_clave(clave):
    errores = []
    # paso 1: longitud
    # paso 2: ¿hay algún dígito?  (pista: c.isdigit())
    # paso 3: ¿hay alguna mayúscula? (pista: c.isupper())
    return errores
""",
                """
def errores_clave(clave):
    errores = []
    if len(clave) < 8:
        errores.append("corta")
    if not any(c.isdigit() for c in clave):
        errores.append("sin numero")
    if not any(c.isupper() for c in clave):
        errores.append("sin mayuscula")
    return errores
""",
                """
assert errores_clave("Segura2026") == []
assert errores_clave("abc") == ["corta", "sin numero", "sin mayuscula"]
assert errores_clave("abcdefgh1") == ["sin mayuscula"]
assert errores_clave("Abcdefgh") == ["sin numero"]
assert errores_clave("Ab1") == ["corta"], "son tres comprobaciones independientes: usa if, no elif"
""",
                hint="Usa tres if separados (no elif): una contraseña puede tener varios problemas a la vez.",
            ),
            py(
                "ld-resumen-notas", "Descomponer: el resumen de un curso", SKILL_PROBLEMAS,
                "Escribe `resumen(notas)` que reciba un diccionario `{alumno: nota}` y devuelva un diccionario con:\n\n"
                "- `'promedio'`: la media de las notas redondeada a 1 decimal (0.0 si no hay notas),\n"
                "- `'aprobados'`: la lista de alumnos con nota >= 5, **ordenada alfabéticamente**,\n"
                "- `'mejor'`: el alumno con la nota más alta (si hay empate, el primero en orden alfabético; `None` si no hay notas).",
                """
def resumen(notas):
    pass
""",
                """
def resumen(notas):
    if not notas:
        return {"promedio": 0.0, "aprobados": [], "mejor": None}
    promedio = round(sum(notas.values()) / len(notas), 1)
    aprobados = sorted(alumno for alumno, nota in notas.items() if nota >= 5)
    mejor = None
    for alumno in sorted(notas):
        if mejor is None or notas[alumno] > notas[mejor]:
            mejor = alumno
    return {"promedio": promedio, "aprobados": aprobados, "mejor": mejor}
""",
                """
r = resumen({"luis": 4, "ana": 9, "eva": 7})
assert r["promedio"] == 6.7, "(4 + 9 + 7) / 3 = 6.67 -> 6.7"
assert r["aprobados"] == ["ana", "eva"], "ordenados alfabéticamente"
assert r["mejor"] == "ana"
assert resumen({"zoe": 8, "ana": 8})["mejor"] == "ana", "empate: el primero en orden alfabético"
assert resumen({}) == {"promedio": 0.0, "aprobados": [], "mejor": None}
""",
                hint="Resuélvelo en tres partes independientes (promedio, aprobados, mejor) y junta el resultado al final. Empieza por el caso vacío.",
            ),
            parsons(
                "ld-ord-pasos", "Ordena: del pseudocódigo al código", SKILL_PROBLEMAS,
                "El pseudocódigo era: *«para cada pedido, si está pagado, sumar su total; al final, aplicar un 10 % de descuento si la suma pasa "
                "de 100»*. Ordena el código. Debe imprimir `108.0`.",
                [
                    "pedidos = [{'total': 80, 'pagado': True}, {'total': 50, 'pagado': False}, {'total': 40, 'pagado': True}]",
                    "suma = 0",
                    "for pedido in pedidos:",
                    "    if pedido['pagado']:",
                    "        suma += pedido['total']",
                    "if suma > 100:",
                    "    suma = suma * 0.9",
                    "print(suma)",
                ],
                "Cada línea del pseudocódigo se convierte en una o dos líneas de código, en el mismo orden. El descuento va después del bucle "
                "(«al final»), no dentro: 80 + 40 = 120, y 120 × 0.9 = 108.0.",
            ),
            quiz(
                "ld-quiz-primero", "El primer paso ante un problema nuevo", SKILL_PROBLEMAS,
                "Te piden una función y no sabes por dónde empezar. ¿Qué haces primero?",
                [
                    "Empezar a escribir código y ver qué pasa",
                    "Resolver a mano 2 o 3 ejemplos pequeños (incluido un caso borde) y anotar los pasos que hiciste",
                    "Buscar la solución exacta en internet",
                    "Escribir la función más general posible",
                ],
                1,
                "Si puedes resolverlo a mano con un ejemplo, los pasos que hiciste son el algoritmo. Si no puedes, todavía no entiendes el "
                "problema, y ningún código lo va a arreglar.",
            ),
            checklist(
                "ld-check-metodo", "Tu método para cada ejercicio", SKILL_PROBLEMAS,
                "Usa este método en los próximos 5 ejercicios que hagas (de cualquier tema) y márcalo cuando lo hayas aplicado.",
                [
                    "Reescribí el enunciado con mis palabras y anoté la entrada y la salida",
                    "Resolví a mano 2-3 ejemplos, incluido un caso borde (vacío, uno solo, empate)",
                    "Escribí los pasos en pseudocódigo antes de programar",
                    "Programé un paso cada vez y lo probé con print",
                    "Cuando falló, seguí el código con una tabla de variables en lugar de cambiar cosas al azar",
                ],
            ),
        ],
    },
]
