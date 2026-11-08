"""Área de interés: Análisis de datos y estadística.

Reutiliza los temas que ya existen en el currículo (pandas, visualización, estadística descriptiva, probabilidad, inferencia,
A/B testing, regresión, storytelling y el proyecto de EDA): el progreso es por tema, así que lo que completes en una ruta
aparece completado aquí y al revés. Los temas nuevos (prefijo `ad-`) cubren lo que faltaba para dominar la estadística.

Bloques A (fundamentos del análisis) y B (estadística a fondo) completos. El bloque C (proyectos aplicados) queda pendiente.
"""
from ..._helpers import checklist, py, quiz

SK_PROCESO = "Análisis: proceso"
SK_DIST = "Estadística: distribuciones"
SK_PRUEBAS = "Estadística: pruebas"
SK_REG = "Estadística: regresión múltiple"
SK_CAUSA = "Estadística: causalidad"
SK_BAYES = "Estadística: bayesiana"
SK_SERIES = "Estadística: series de tiempo"

_PENDIENTE = "Capítulo en preparación. " * 60

AREA = {
    "slug": "analisis-datos",
    "title": "Análisis de datos y estadística",
    "order": 3,
    "description": "Tomar un conjunto de datos y sacar conclusiones que aguanten un examen: del proceso y pandas a la estadística "
                   "a fondo (distribuciones, pruebas, regresión, causalidad, bayesiana y series de tiempo).",
    "notice": "**Progreso compartido:** varios temas de esta área también están en las rutas (pandas, estadística, A/B testing...). "
              "Son el mismo tema: si lo completas en un sitio, aparece completado en el otro. Los ejercicios se corrigen en el "
              "navegador con Python; muchos usan solo `math`, `statistics` y `random` para que veas la fórmula por dentro.",
    "blocks": [
        {
            "label": "A",
            "title": "Fundamentos del análisis",
            "description": "El proceso de la pregunta a la conclusión, pandas para cargar, limpiar y transformar, gráficos, estadística "
                           "descriptiva y un análisis exploratorio completo.",
            "topics": ["ad-proceso", "pandas-basico", "pandas-limpieza", "pandas-transformacion", "visualizacion", "estadistica",
                       "proyecto-eda"],
        },
        {
            "label": "B",
            "title": "Estadística a fondo",
            "description": "Probabilidad y distribuciones, inferencia, pruebas de hipótesis (A/B y el resto), regresión simple, múltiple "
                           "y logística, causalidad y sesgos, estadística bayesiana, series de tiempo y cómo comunicar lo que encuentras.",
            "topics": ["est-probabilidad", "ad-distribuciones", "est-inferencia", "est-ab-testing", "ad-pruebas", "est-regresion",
                       "ad-regresion-multiple", "ad-causalidad", "ad-bayes", "ad-series-tiempo", "data-storytelling"],
        },
    ],
}

TOPICS = [
    # ------------------------------------------------------------------------------------------ bloque A
    {
        "slug": "ad-proceso",
        "title": "Del dato a la conclusión: el proceso del análisis",
        "summary": "Preguntas que se pueden responder, unidad de análisis, tipos de variables, tasas y normalización, el ciclo completo "
                   "y dónde conseguir datos.",
        "hours": 5,
        "theory": _PENDIENTE,
        "exercises": [
            py("adp-tasa", "Tasa de interacción", SK_PROCESO,
               "Escribe `tasa_interaccion(videos)`: recibe una lista de diccionarios con `vistas`, `likes`, `comentarios` y `compartidos`, "
               "y devuelve una lista con la tasa de interacción de cada vídeo: `(likes + comentarios + compartidos) / vistas`, redondeada "
               "a 4 decimales. Si un vídeo tiene 0 vistas, su tasa es `0.0` (no dividas entre cero).",
               starter="""
def tasa_interaccion(videos):
    # tu código aquí
    pass
""",
               solution="""
def tasa_interaccion(videos):
    tasas = []
    for v in videos:
        if v["vistas"] == 0:
            tasas.append(0.0)
        else:
            tasas.append(round((v["likes"] + v["comentarios"] + v["compartidos"]) / v["vistas"], 4))
    return tasas
""",
               tests="""
videos = [
    {"vistas": 1000, "likes": 80, "comentarios": 10, "compartidos": 10},
    {"vistas": 0, "likes": 0, "comentarios": 0, "compartidos": 0},
    {"vistas": 300, "likes": 20, "comentarios": 3, "compartidos": 2},
]
res = tasa_interaccion(videos)
assert res == [0.1, 0.0, 0.0833], "Esperaba [0.1, 0.0, 0.0833]; obtuve %r" % (res,)
"""),
            py("adp-ponderado", "El promedio de los promedios", SK_PROCESO,
               "Tienes el número de pedidos y el ticket medio de cada tienda como una lista de tuplas `(pedidos, ticket_medio)`. Escribe "
               "`ticket_global(tiendas)` que devuelva el ticket medio **de todos los pedidos juntos**. Ojo: no es el promedio de los "
               "promedios; cada tienda pesa según sus pedidos.",
               starter="""
def ticket_global(tiendas):
    # tu código aquí
    pass
""",
               solution="""
def ticket_global(tiendas):
    pedidos = sum(n for n, _ in tiendas)
    total = sum(n * media for n, media in tiendas)
    return total / pedidos
""",
               tests="""
res = ticket_global([(100, 10), (10, 50)])
assert abs(res - 1500 / 110) < 1e-9, "1000 + 500 de ventas entre 110 pedidos = 13.64 (no 30); obtuve %r" % (res,)
assert ticket_global([(5, 20), (5, 40)]) == 30, "Con el mismo peso sí coincide con el promedio simple"
"""),
            py("adp-normalizar", "Comparar cuentas de tamaños distintos", SK_PROCESO,
               "Escribe `mejor_por_seguidor(cuentas)`: recibe diccionarios con `nombre`, `seguidores` y `vistas` (vistas medias por vídeo) "
               "y devuelve el `nombre` de la cuenta con más vistas **por seguidor**. Así comparas el rendimiento del contenido sin que "
               "gane siempre la cuenta más grande.",
               starter="""
def mejor_por_seguidor(cuentas):
    # tu código aquí
    pass
""",
               solution="""
def mejor_por_seguidor(cuentas):
    return max(cuentas, key=lambda c: c["vistas"] / c["seguidores"])["nombre"]
""",
               tests="""
cuentas = [
    {"nombre": "grande", "seguidores": 2_000_000, "vistas": 300_000},
    {"nombre": "pequena", "seguidores": 4_000, "vistas": 12_000},
    {"nombre": "media", "seguidores": 50_000, "vistas": 40_000},
]
assert mejor_por_seguidor(cuentas) == "pequena", "12 000 / 4 000 = 3 vistas por seguidor gana a 0.15 y 0.8"
"""),
            quiz("adp-quiz-tipo", "Tipo de variable", SK_PROCESO,
                 "Una encuesta pregunta \"¿Qué tan satisfecho estás?\" con las respuestas Nada, Poco, Bastante y Mucho. ¿Qué tipo de variable es?",
                 ["Nominal", "Ordinal", "Numérica continua", "Numérica discreta"], 1,
                 "Las categorías tienen un orden natural pero las distancias entre ellas no son iguales ni medibles: es ordinal. Puedes usar la "
                 "mediana o los porcentajes por categoría, pero un promedio de \"Poco = 2, Bastante = 3\" es discutible."),
            quiz("adp-quiz-pregunta", "Una pregunta que se pueda responder", SK_PROCESO,
                 "¿Cuál es la mejor pregunta para empezar un análisis de los vídeos de tu cuenta?",
                 ["¿Qué dicen mis datos?",
                  "¿Mis vídeos con un gancho en forma de pregunta retienen más a los 3 segundos que los demás, en los últimos 60 días?",
                  "¿Cómo me hago viral?",
                  "¿Cuál es el mejor contenido?"], 1,
                 "Es concreta: dice qué comparar (gancho con pregunta frente al resto), con qué métrica (retención a los 3 s) y en qué periodo. "
                 "Las otras no dicen qué medir ni qué decisión ayudarían a tomar."),
            quiz("adp-quiz-unidad", "La unidad de análisis", SK_PROCESO,
                 "Quieres saber si los clientes que compran más veces gastan más por pedido. Tu tabla tiene una fila por pedido. ¿Qué haces primero?",
                 ["Calcular la correlación entre el número de fila y el importe",
                  "Agrupar por cliente: número de pedidos y ticket medio de cada cliente, y comparar entre clientes",
                  "Calcular el ticket medio de todos los pedidos",
                  "Eliminar los clientes con un solo pedido"], 1,
                 "La pregunta es sobre clientes, así que la unidad de análisis es el cliente: primero se resume cada cliente en una fila y luego se compara."),
            checklist("adp-check", "Antes de sacar una conclusión", SK_PROCESO,
                      "Aplica esta lista a tu próximo análisis (por ejemplo, con los datos del sandbox o con las estadísticas de tus redes).",
                      ["Escribí la pregunta y la decisión que ayudará a tomar",
                       "Sé qué representa cada fila y qué periodo cubren los datos",
                       "Revisé vacíos, duplicados y valores imposibles",
                       "Usé tasas o valores normalizados cuando los grupos tienen tamaños distintos",
                       "Miré la distribución, no solo el promedio",
                       "Busqué al menos una explicación alternativa a mi resultado",
                       "Escribí la conclusión con su nivel de confianza y una acción"]),
        ],
    },
    # ------------------------------------------------------------------------------------------ bloque B
    {
        "slug": "ad-distribuciones",
        "title": "Distribuciones de probabilidad: los patrones del azar",
        "summary": "Binomial, geométrica, Poisson, uniforme, normal, exponencial, log-normal y colas largas: qué proceso genera cada una "
                   "y cómo reconocerlas en tus datos.",
        "hours": 8,
        "theory": _PENDIENTE,
        "exercises": [
            py("add-binomial", "Probabilidad binomial", SK_DIST,
               "Escribe `prob_binomial(n, k, p)`: la probabilidad de obtener exactamente `k` éxitos en `n` intentos independientes con "
               "probabilidad de éxito `p`. Fórmula: `C(n, k) · p^k · (1 - p)^(n - k)`. Usa `math.comb(n, k)`.",
               starter="""
import math

def prob_binomial(n, k, p):
    # tu código aquí
    pass
""",
               solution="""
import math

def prob_binomial(n, k, p):
    return math.comb(n, k) * p ** k * (1 - p) ** (n - k)
""",
               tests="""
assert abs(prob_binomial(10, 3, 0.5) - 0.1171875) < 1e-9, "3 caras en 10 lanzamientos: 120/1024"
assert abs(prob_binomial(5, 0, 0.2) - 0.32768) < 1e-9, "Ningún éxito en 5 con p = 0.2: 0.8^5"
"""),
            py("add-poisson", "Probabilidad de Poisson", SK_DIST,
               "Llegan de media `lam` mensajes por hora a un chatbot. Escribe `prob_poisson(k, lam)`: la probabilidad de recibir exactamente "
               "`k` mensajes en una hora. Fórmula: `e^(-lam) · lam^k / k!`. Usa `math.exp` y `math.factorial`.",
               starter="""
import math

def prob_poisson(k, lam):
    # tu código aquí
    pass
""",
               solution="""
import math

def prob_poisson(k, lam):
    return math.exp(-lam) * lam ** k / math.factorial(k)
""",
               tests="""
assert abs(prob_poisson(0, 2) - 0.135335) < 1e-6, "Con media 2, ningún mensaje: e^-2"
assert abs(prob_poisson(3, 2) - 0.180447) < 1e-6, "Exactamente 3 mensajes con media 2"
"""),
            py("add-normal", "Probabilidad acumulada de la normal", SK_DIST,
               "Escribe `prob_menor(x, media, desv)`: la probabilidad de que una variable normal con esa media y desviación sea menor que `x`. "
               "Fórmula: `0.5 · (1 + erf((x - media) / (desv · √2)))`. Usa `math.erf` y `math.sqrt`.",
               starter="""
import math

def prob_menor(x, media, desv):
    # tu código aquí
    pass
""",
               solution="""
import math

def prob_menor(x, media, desv):
    return 0.5 * (1 + math.erf((x - media) / (desv * math.sqrt(2))))
""",
               tests="""
assert abs(prob_menor(40, 40, 5) - 0.5) < 1e-9, "La mitad de los valores está por debajo de la media"
assert abs(prob_menor(50, 40, 5) - 0.97725) < 1e-4, "Dos desviaciones por encima: ~97.7 %"
assert abs(prob_menor(35, 40, 5) - 0.158655) < 1e-4, "Una desviación por debajo: ~15.9 %"
"""),
            py("add-pareto", "¿Cuánto se llevan los de arriba?", SK_DIST,
               "Escribe `cuota_top(valores, fraccion)`: la parte del total que suman los valores más altos, donde `fraccion` es la proporción "
               "de elementos de arriba (0.2 = el 20 % superior). El número de elementos es `max(1, round(len(valores) * fraccion))`. "
               "Sirve para ver lo concentradas que están las vistas de una cuenta.",
               starter="""
def cuota_top(valores, fraccion):
    # tu código aquí
    pass
""",
               solution="""
def cuota_top(valores, fraccion):
    ordenados = sorted(valores, reverse=True)
    k = max(1, round(len(valores) * fraccion))
    return sum(ordenados[:k]) / sum(valores)
""",
               tests="""
assert abs(cuota_top([100, 1, 1, 1, 1, 1, 1, 1, 1, 1], 0.1) - 100 / 109) < 1e-9, "Un vídeo se lleva casi todo"
assert abs(cuota_top([10] * 10, 0.2) - 0.2) < 1e-9, "Si todos son iguales, el 20 % de arriba suma el 20 %"
"""),
            quiz("add-quiz-cual", "¿Qué distribución?", SK_DIST,
                 "Cuentas cuántas consultas llegan al soporte en cada hora. Las consultas llegan de forma independiente y a un ritmo medio estable. "
                 "¿Qué distribución es el punto de partida natural?",
                 ["Normal", "Binomial", "Poisson", "Uniforme"], 2,
                 "Conteos de sucesos independientes en un intervalo, con ritmo medio constante: Poisson. Si la varianza sale mucho mayor que la "
                 "media (sobredispersión), el ritmo no es estable y hará falta otra (por ejemplo, binomial negativa)."),
            quiz("add-quiz-cola", "Colas largas", SK_DIST,
                 "Las vistas de tus 50 vídeos van de 300 a 900 000. La media es 31 000 y la mediana 1 400. ¿Qué número describe mejor un vídeo típico?",
                 ["La media, porque usa todos los datos", "La mediana", "El máximo", "La suma dividida entre 2"], 1,
                 "Con colas largas, un par de éxitos arrastran la media muy arriba. La mediana describe el vídeo típico; los éxitos se analizan aparte."),
            quiz("add-quiz-exp", "Tiempos de espera", SK_DIST,
                 "Si los clientes llegan según un proceso de Poisson, ¿cómo se distribuye el tiempo entre una llegada y la siguiente?",
                 ["Normal", "Exponencial", "Binomial", "Uniforme"], 1,
                 "Conteos de Poisson por intervalo y tiempos exponenciales entre sucesos son dos caras del mismo proceso."),
        ],
    },
    {
        "slug": "ad-pruebas",
        "title": "Elegir y aplicar la prueba estadística correcta",
        "summary": "Pruebas t (una muestra, Welch, pareada), chi-cuadrado, ANOVA, no paramétricas, permutación, comparaciones múltiples, "
                   "tamaño del efecto y potencia.",
        "hours": 9,
        "theory": _PENDIENTE,
        "exercises": [
            py("adt-welch", "Estadístico t de Welch", SK_PRUEBAS,
               "Escribe `t_welch(a, b)`: el estadístico t para comparar las medias de dos grupos independientes sin suponer varianzas iguales: "
               "`(media_a - media_b) / √(var_a / n_a + var_b / n_b)`, con varianzas **muestrales** (`statistics.variance`).",
               starter="""
import math
import statistics

def t_welch(a, b):
    # tu código aquí
    pass
""",
               solution="""
import math
import statistics

def t_welch(a, b):
    ea = statistics.variance(a) / len(a)
    eb = statistics.variance(b) / len(b)
    return (statistics.mean(a) - statistics.mean(b)) / math.sqrt(ea + eb)
""",
               tests="""
assert abs(t_welch([1, 2, 3, 4, 5], [2, 3, 4, 5, 6]) - (-1.0)) < 1e-9, "Diferencia -1 con error estándar 1"
assert abs(t_welch([10, 12, 14], [1, 2, 3]) - 7.745967) < 1e-5, "Diferencia 10 con error estándar √(5/3)"
"""),
            py("adt-chi", "Chi-cuadrado de independencia", SK_PRUEBAS,
               "Escribe `chi_cuadrado(tabla)`: recibe una tabla de contingencia (lista de filas con conteos) y devuelve el estadístico "
               "chi-cuadrado `Σ (observado - esperado)² / esperado`, donde el esperado de cada celda es "
               "`total_de_su_fila · total_de_su_columna / total_general`.",
               starter="""
def chi_cuadrado(tabla):
    # tu código aquí
    pass
""",
               solution="""
def chi_cuadrado(tabla):
    filas = [sum(f) for f in tabla]
    columnas = [sum(col) for col in zip(*tabla)]
    total = sum(filas)
    chi = 0.0
    for i, fila in enumerate(tabla):
        for j, observado in enumerate(fila):
            esperado = filas[i] * columnas[j] / total
            chi += (observado - esperado) ** 2 / esperado
    return chi
""",
               tests="""
assert abs(chi_cuadrado([[10, 20], [20, 10]]) - 100 / 15) < 1e-9, "Esperados 15 en cada celda: 4 · 25/15"
assert chi_cuadrado([[10, 10], [10, 10]]) == 0, "Si observado = esperado, el estadístico es 0"
assert abs(chi_cuadrado([[30, 10, 10], [10, 30, 10]]) - 20.0) < 1e-9, "Funciona con más de dos columnas"
"""),
            py("adt-multiples", "El problema de las comparaciones múltiples", SK_PRUEBAS,
               "Escribe `prob_algun_falso_positivo(k, alfa=0.05)`: si haces `k` pruebas independientes y en ninguna hay un efecto real, "
               "la probabilidad de que al menos una salga \"significativa\" por azar es `1 - (1 - alfa)^k`.",
               starter="""
def prob_algun_falso_positivo(k, alfa=0.05):
    # tu código aquí
    pass
""",
               solution="""
def prob_algun_falso_positivo(k, alfa=0.05):
    return 1 - (1 - alfa) ** k
""",
               tests="""
assert abs(prob_algun_falso_positivo(1) - 0.05) < 1e-12, "Una prueba: 5 %"
assert abs(prob_algun_falso_positivo(20) - 0.641514) < 1e-5, "Con 20 métricas, casi dos de cada tres veces 'encuentras' algo"
assert abs(prob_algun_falso_positivo(20, alfa=0.05 / 20) - 0.048830) < 1e-5, "Con la corrección de Bonferroni vuelve a ~5 %"
"""),
            py("adt-cohen", "Tamaño del efecto: d de Cohen", SK_PRUEBAS,
               "Escribe `d_cohen(a, b)`: la diferencia de medias dividida entre la desviación combinada "
               "`√(((n_a - 1)·var_a + (n_b - 1)·var_b) / (n_a + n_b - 2))`, con varianzas muestrales.",
               starter="""
import math
import statistics

def d_cohen(a, b):
    # tu código aquí
    pass
""",
               solution="""
import math
import statistics

def d_cohen(a, b):
    na, nb = len(a), len(b)
    combinada = math.sqrt(((na - 1) * statistics.variance(a) + (nb - 1) * statistics.variance(b)) / (na + nb - 2))
    return (statistics.mean(a) - statistics.mean(b)) / combinada
""",
               tests="""
assert abs(d_cohen([1, 2, 3, 4, 5], [3, 4, 5, 6, 7]) - (-1.264911)) < 1e-5, "Diferencia -2 entre una desviación de 1.58"
assert abs(d_cohen([5, 7, 9], [5, 7, 9])) < 1e-12, "Grupos iguales: efecto 0"
"""),
            py("adt-permutacion", "Prueba de permutación", SK_PRUEBAS,
               "Escribe `prueba_permutacion(a, b, n=2000, semilla=0)` que devuelva el valor p (bilateral) de la diferencia de medias:\n\n"
               "1. Calcula la diferencia observada `abs(media(a) - media(b))`.\n"
               "2. Junta los datos y, `n` veces, barájalos con `random.Random(semilla)`, reparte los primeros `len(a)` al grupo A y el resto al B, "
               "y calcula la diferencia absoluta de medias.\n"
               "3. Devuelve la proporción de repeticiones con una diferencia **mayor o igual** que la observada.",
               starter="""
import random
import statistics

def prueba_permutacion(a, b, n=2000, semilla=0):
    rng = random.Random(semilla)
    # tu código aquí
    pass
""",
               solution="""
import random
import statistics

def prueba_permutacion(a, b, n=2000, semilla=0):
    rng = random.Random(semilla)
    observada = abs(statistics.mean(a) - statistics.mean(b))
    juntos = list(a) + list(b)
    extremas = 0
    for _ in range(n):
        rng.shuffle(juntos)
        diferencia = abs(statistics.mean(juntos[:len(a)]) - statistics.mean(juntos[len(a):]))
        if diferencia >= observada:
            extremas += 1
    return extremas / n
""",
               tests="""
p = prueba_permutacion([5, 6, 7, 5, 6, 7, 6, 5], [9, 10, 11, 9, 10, 11, 10, 9])
assert p is not None and p < 0.01, "Grupos claramente distintos: p muy pequeño; obtuve %r" % (p,)
p = prueba_permutacion([5, 6, 7, 8, 6], [6, 5, 8, 7, 6])
assert p > 0.3, "Grupos casi iguales: p grande; obtuve %r" % (p,)
"""),
            quiz("adt-quiz-pareada", "Antes y después", SK_PRUEBAS,
                 "Mides el tiempo que tardan 30 usuarios en completar una tarea con el diseño viejo y, después, esos **mismos** 30 usuarios con el nuevo. "
                 "¿Qué prueba usas?",
                 ["t de Welch para dos grupos independientes", "t pareada (sobre las diferencias de cada usuario)", "Chi-cuadrado", "ANOVA"], 1,
                 "Son las mismas personas medidas dos veces: las observaciones no son independientes. La prueba pareada trabaja con la diferencia de "
                 "cada usuario y elimina la variación entre personas, por eso tiene más potencia."),
            quiz("adt-quiz-chi", "Dos variables categóricas", SK_PRUEBAS,
                 "Quieres saber si el tipo de publicación (vídeo, carrusel, foto) está relacionado con que la publicación consiga al menos un "
                 "seguidor nuevo (sí/no). ¿Qué prueba encaja?",
                 ["t de Student", "Chi-cuadrado de independencia", "Correlación de Pearson", "t pareada"], 1,
                 "Las dos variables son categóricas: se cruzan en una tabla de contingencia y se comparan los conteos observados con los esperados."),
            quiz("adt-quiz-efecto", "Significativo pero pequeño", SK_PRUEBAS,
                 "Con 2 millones de usuarios, un cambio sube el tiempo de sesión de 300,0 a 300,4 segundos con p < 0,001. ¿Qué concluyes?",
                 ["Es un gran éxito: p es muy pequeño",
                  "El efecto es casi seguro real, pero diminuto: hay que valorar si 0,4 segundos importan para el negocio",
                  "Es un error: con p tan pequeño debe haber un fallo",
                  "No se puede concluir nada"], 1,
                 "El valor p dice si el efecto es distinguible del azar, no si es grande. Con muestras enormes, efectos irrelevantes salen "
                 "significativos: informa siempre del tamaño del efecto con su intervalo."),
        ],
    },
    {
        "slug": "ad-regresion-multiple",
        "title": "Regresión múltiple y regresión logística",
        "summary": "Controlar por otras variables, interpretar coeficientes, variables categóricas, interacciones, logaritmos, diagnóstico "
                   "de residuos, sobreajuste y regresión logística con odds ratios.",
        "hours": 8,
        "theory": _PENDIENTE,
        "exercises": [
            py("adr-dummies", "Variables ficticias (dummies)", SK_REG,
               "Escribe `codificar(categorias, referencia)`: recibe una lista de categorías y devuelve, por cada elemento, un diccionario con una "
               "columna `\"es_<categoria>\"` (1 o 0) para cada categoría **excepto la de referencia**. Las columnas van en orden alfabético.",
               starter="""
def codificar(categorias, referencia):
    # tu código aquí
    pass
""",
               solution="""
def codificar(categorias, referencia):
    niveles = sorted(set(categorias) - {referencia})
    return [{"es_" + nivel: int(c == nivel) for nivel in niveles} for c in categorias]
""",
               tests="""
res = codificar(["video", "carrusel", "foto", "video"], "foto")
assert res == [
    {"es_carrusel": 0, "es_video": 1},
    {"es_carrusel": 1, "es_video": 0},
    {"es_carrusel": 0, "es_video": 0},
    {"es_carrusel": 0, "es_video": 1},
], "La foto (referencia) queda como todo ceros; obtuve %r" % (res,)
"""),
            py("adr-r2aj", "R² ajustado", SK_REG,
               "Escribe `r2_ajustado(r2, n, k)` con `n` observaciones y `k` variables explicativas: `1 - (1 - r2) · (n - 1) / (n - k - 1)`.",
               starter="""
def r2_ajustado(r2, n, k):
    # tu código aquí
    pass
""",
               solution="""
def r2_ajustado(r2, n, k):
    return 1 - (1 - r2) * (n - 1) / (n - k - 1)
""",
               tests="""
assert abs(r2_ajustado(0.5, 100, 3) - 0.484375) < 1e-9, "Con 100 datos y 3 variables penaliza poco"
assert abs(r2_ajustado(0.5, 20, 10) - (-0.055556)) < 1e-5, "Con 10 variables y 20 datos el ajuste 'bueno' era espejismo"
"""),
            py("adr-logistica", "Probabilidad de una regresión logística", SK_REG,
               "Escribe `probabilidad(intercepto, coefs, valores)`: calcula `z = intercepto + Σ coef · valor` y devuelve `1 / (1 + e^(-z))`.",
               starter="""
import math

def probabilidad(intercepto, coefs, valores):
    # tu código aquí
    pass
""",
               solution="""
import math

def probabilidad(intercepto, coefs, valores):
    z = intercepto + sum(c * v for c, v in zip(coefs, valores))
    return 1 / (1 + math.exp(-z))
""",
               tests="""
assert abs(probabilidad(0, [], []) - 0.5) < 1e-12, "z = 0 da 50 %"
assert abs(probabilidad(-2, [0.5], [4]) - 0.5) < 1e-12, "-2 + 0.5·4 = 0"
assert abs(probabilidad(-1, [1, 0.5], [3, 0]) - 0.880797) < 1e-5, "z = 2"
"""),
            quiz("adr-quiz-coef", "Interpretar un coeficiente", SK_REG,
                 "Un modelo de ventas diarias incluye precio, temporada y `tiene_descuento`. El coeficiente de `tiene_descuento` es 12. ¿Qué significa?",
                 ["Los días con descuento venden 12 unidades más que los días sin descuento, sin más matices",
                  "Comparando días con el mismo precio y la misma temporada, los días con descuento venden en promedio 12 unidades más",
                  "El descuento causa 12 ventas más con seguridad",
                  "El 12 % de las ventas se debe al descuento"], 1,
                 "En regresión múltiple cada coeficiente es la diferencia asociada a esa variable manteniendo constantes las demás del modelo. "
                 "Que sea causal depende del diseño, no de la regresión."),
            quiz("adr-quiz-odds", "Odds ratio", SK_REG,
                 "En una regresión logística de \"el cliente compra\", el coeficiente de `vio_la_demo` es 0,69. Como e^0,69 ≈ 2, ¿qué significa?",
                 ["La probabilidad de compra se duplica siempre",
                  "Las odds (probabilidad / (1 - probabilidad)) de comprar se multiplican por 2 al ver la demo, con lo demás constante",
                  "La probabilidad sube 69 puntos",
                  "El 69 % de los que ven la demo compran"], 1,
                 "Los coeficientes logísticos actúan sobre el logaritmo de las odds. Duplicar las odds solo es parecido a duplicar la probabilidad "
                 "cuando la probabilidad es pequeña."),
            quiz("adr-quiz-sobreajuste", "Más variables, mejor R²", SK_REG,
                 "Al añadir 15 variables más a tu modelo, el R² sube de 0,41 a 0,58. ¿Qué compruebas antes de celebrarlo?",
                 ["Nada: más R² siempre es mejor",
                  "El R² ajustado y, sobre todo, el error con datos que el modelo no vio (validación)",
                  "Que las variables tengan nombres claros",
                  "Que el R² no pase de 1"], 1,
                 "El R² nunca baja al añadir variables, aunque sean ruido. El R² ajustado penaliza las variables y la validación con datos nuevos "
                 "dice si el modelo de verdad generaliza."),
        ],
    },
    {
        "slug": "ad-causalidad",
        "title": "Causalidad y sesgos: cuándo un dato prueba algo",
        "summary": "Contrafactuales, confusores, mediadores y colisionadores, sesgo de supervivencia, regresión a la media y métodos para "
                   "estimar causas sin experimento: diferencias en diferencias, discontinuidad y emparejamiento.",
        "hours": 8,
        "theory": _PENDIENTE,
        "exercises": [
            py("adc-did", "Diferencias en diferencias", SK_CAUSA,
               "Escribe `diferencias_en_diferencias(trat_antes, trat_despues, ctrl_antes, ctrl_despues)`: el cambio del grupo tratado menos el "
               "cambio del grupo de control.",
               starter="""
def diferencias_en_diferencias(trat_antes, trat_despues, ctrl_antes, ctrl_despues):
    # tu código aquí
    pass
""",
               solution="""
def diferencias_en_diferencias(trat_antes, trat_despues, ctrl_antes, ctrl_despues):
    return (trat_despues - trat_antes) - (ctrl_despues - ctrl_antes)
""",
               tests="""
assert diferencias_en_diferencias(100, 130, 100, 115) == 15, "Subió 30, pero 15 habría subido igual"
assert diferencias_en_diferencias(50, 40, 60, 40) == 10, "Bajó menos que el control: efecto positivo"
"""),
            py("adc-colisionador", "El sesgo del colisionador", SK_CAUSA,
               "Cada vídeo tiene una `calidad` y un `gancho` que, en el total de vídeos, **no** están relacionados. Un vídeo se vuelve viral si "
               "`calidad + gancho > umbral`. Escribe `correlacion_entre_virales(videos, umbral)` que devuelva la correlación de Pearson "
               "(`statistics.correlation`) entre calidad y gancho **solo entre los vídeos virales**. Las pruebas te enseñarán qué pasa.",
               starter="""
import statistics

def correlacion_entre_virales(videos, umbral):
    # tu código aquí
    pass
""",
               solution="""
import statistics

def correlacion_entre_virales(videos, umbral):
    virales = [v for v in videos if v["calidad"] + v["gancho"] > umbral]
    return statistics.correlation([v["calidad"] for v in virales], [v["gancho"] for v in virales])
""",
               tests="""
import random
rng = random.Random(7)
videos = [{"calidad": rng.gauss(0, 1), "gancho": rng.gauss(0, 1)} for _ in range(3000)]
todos = correlacion_entre_virales(videos, -100)
assert todos is not None and abs(todos) < 0.1, "Con todos los vídeos no hay relación; obtuve %r" % (todos,)
virales = correlacion_entre_virales(videos, 1.5)
assert virales < -0.3, ("Solo entre los virales aparece una correlación negativa que no existe en realidad (%.2f): "
                        "si solo miras a los ganadores, parece que calidad y gancho se excluyen." % virales)
"""),
            quiz("adc-quiz-confusor", "Encuentra el confusor", SK_CAUSA,
                 "Los usuarios que activan las notificaciones compran el doble que los que no. ¿Cuál es la explicación alternativa más importante?",
                 ["Las notificaciones son molestas",
                  "Los usuarios más interesados en la tienda activan las notificaciones y también compran más: el interés causa las dos cosas",
                  "El tamaño de la muestra",
                  "El color de las notificaciones"], 1,
                 "El interés previo es un confusor: influye en activar notificaciones y en comprar. Para medir el efecto de las notificaciones "
                 "hace falta un experimento (activarlas al azar a una parte) o controlar muy bien el interés previo."),
            quiz("adc-quiz-media", "Regresión a la media", SK_CAUSA,
                 "Eliges los 10 vídeos con peor retención del mes, les cambias la miniatura y el mes siguiente mejoran. ¿Qué es lo primero que sospechas?",
                 ["Que la miniatura funciona seguro",
                  "Regresión a la media: los peores de un mes suelen mejorar al siguiente aunque no hagas nada, porque parte de su mal resultado era azar",
                  "Que los datos están mal",
                  "Que la plataforma te castigó antes"], 1,
                 "Cuando eliges casos por ser extremos, en la siguiente medición tienden a volver hacia la media. Sin un grupo de control "
                 "(otros vídeos malos a los que no tocas) no sabes qué parte de la mejora es tuya."),
            quiz("adc-quiz-mediador", "¿Controlar o no controlar?", SK_CAUSA,
                 "Quieres medir el efecto total de un curso gratuito sobre las ventas. El curso aumenta la confianza en tu marca y la confianza aumenta "
                 "las ventas. ¿Incluyes la confianza como variable de control?",
                 ["Sí, siempre hay que controlar todo lo posible",
                  "No: la confianza es un mediador (parte del camino del efecto); controlarla borraría justo el efecto que quieres medir",
                  "Sí, porque es un confusor",
                  "Da igual"], 1,
                 "Se controla por los confusores (causas comunes), no por los mediadores ni por los colisionadores (consecuencias comunes)."),
            checklist("adc-check", "Antes de afirmar que X causa Y", SK_CAUSA,
                      "Repasa esta lista con cualquier conclusión causal, tuya o de un artículo.",
                      ["¿La causa ocurrió antes que el efecto?",
                       "¿Qué variable podría causar las dos cosas a la vez (confusor)?",
                       "¿Podría ser al revés (causalidad inversa)?",
                       "¿Los datos incluyen solo a los ganadores o a los que sobrevivieron?",
                       "¿Se eligieron los casos por ser extremos (regresión a la media)?",
                       "¿Hay un grupo de comparación que no recibió el tratamiento?",
                       "¿El efecto aparece en más de un conjunto de datos o periodo?"]),
        ],
    },
    {
        "slug": "ad-bayes",
        "title": "Estadística bayesiana: actualizar creencias con datos",
        "summary": "Prior, verosimilitud y posterior, el modelo beta-binomial, intervalos de credibilidad, A/B testing bayesiano, medias "
                   "suavizadas para rankings y bandidos multibrazo.",
        "hours": 7,
        "theory": _PENDIENTE,
        "exercises": [
            py("adb-actualizar", "Actualizar con el teorema de Bayes", SK_BAYES,
               "Escribe `actualizar(priors, verosimilitudes)`: recibe las probabilidades previas de varias hipótesis y la verosimilitud de los datos "
               "bajo cada una, y devuelve las probabilidades posteriores: multiplica cada prior por su verosimilitud y divide entre la suma de "
               "esos productos para que sumen 1.",
               starter="""
def actualizar(priors, verosimilitudes):
    # tu código aquí
    pass
""",
               solution="""
def actualizar(priors, verosimilitudes):
    productos = [p * v for p, v in zip(priors, verosimilitudes)]
    total = sum(productos)
    return [x / total for x in productos]
""",
               tests="""
res = actualizar([0.5, 0.5], [0.9, 0.3])
assert [round(x, 6) for x in res] == [0.75, 0.25], "Esperaba [0.75, 0.25]; obtuve %r" % (res,)
res = actualizar([0.01, 0.99], [0.99, 0.05])
assert abs(res[0] - 0.166667) < 1e-5, "El ejemplo de la prueba médica: ~17 %"
"""),
            py("adb-beta", "Posterior beta-binomial", SK_BAYES,
               "Con un prior `Beta(a, b)` para una tasa y `exitos` y `fracasos` observados, el posterior es `Beta(a + exitos, b + fracasos)` y su "
               "media es `a' / (a' + b')`. Escribe `posterior_beta(a, b, exitos, fracasos)` que devuelva la tupla `(a', b', media)`.",
               starter="""
def posterior_beta(a, b, exitos, fracasos):
    # tu código aquí
    pass
""",
               solution="""
def posterior_beta(a, b, exitos, fracasos):
    a2, b2 = a + exitos, b + fracasos
    return (a2, b2, a2 / (a2 + b2))
""",
               tests="""
assert posterior_beta(1, 1, 8, 2) == (9, 3, 0.75), "Prior uniforme + 8 de 10"
a2, b2, media = posterior_beta(2, 38, 3, 0)
assert (a2, b2) == (5, 38) and abs(media - 5 / 43) < 1e-12, "Un prior que espera ~5 % frena 3 éxitos de 3"
"""),
            py("adb-ab", "A/B bayesiano por simulación", SK_BAYES,
               "Escribe `prob_b_mejor(exitos_a, total_a, exitos_b, total_b, simulaciones=20000, semilla=1)`: con priors uniformes, el posterior de cada "
               "variante es `Beta(1 + exitos, 1 + total - exitos)`. Con `rng = random.Random(semilla)`, saca en cada simulación una tasa de cada "
               "posterior con `rng.betavariate(...)` (primero A, luego B) y devuelve la proporción de simulaciones en que la de B es mayor.",
               starter="""
import random

def prob_b_mejor(exitos_a, total_a, exitos_b, total_b, simulaciones=20000, semilla=1):
    rng = random.Random(semilla)
    # tu código aquí
    pass
""",
               solution="""
import random

def prob_b_mejor(exitos_a, total_a, exitos_b, total_b, simulaciones=20000, semilla=1):
    rng = random.Random(semilla)
    gana_b = 0
    for _ in range(simulaciones):
        pa = rng.betavariate(1 + exitos_a, 1 + total_a - exitos_a)
        pb = rng.betavariate(1 + exitos_b, 1 + total_b - exitos_b)
        if pb > pa:
            gana_b += 1
    return gana_b / simulaciones
""",
               tests="""
p = prob_b_mejor(50, 1000, 80, 1000)
assert p is not None and p > 0.99, "8 % frente a 5 % con 1000 usuarios: B casi seguro mejor; obtuve %r" % (p,)
p = prob_b_mejor(50, 1000, 50, 1000)
assert 0.4 < p < 0.6, "Resultados iguales: ~50 %%; obtuve %r" % p
p = prob_b_mejor(5, 10, 6, 10)
assert 0.55 < p < 0.85, "Con 10 usuarios por grupo la evidencia es débil; obtuve %r" % p
"""),
            py("adb-suavizada", "Ranking con media suavizada", SK_BAYES,
               "Para ordenar vídeos por tasa de interacción sin que gane uno con 2 de 2, se usa una media suavizada: "
               "`(exitos + prior_media · prior_peso) / (total + prior_peso)`. Escribe `media_suavizada(exitos, total, prior_media, prior_peso)`.",
               starter="""
def media_suavizada(exitos, total, prior_media, prior_peso):
    # tu código aquí
    pass
""",
               solution="""
def media_suavizada(exitos, total, prior_media, prior_peso):
    return (exitos + prior_media * prior_peso) / (total + prior_peso)
""",
               tests="""
poco = media_suavizada(2, 2, 0.1, 20)
mucho = media_suavizada(450, 500, 0.1, 20)
assert abs(poco - 4 / 22) < 1e-9, "2 de 2 se queda en ~18 %, cerca del prior"
assert abs(mucho - 452 / 520) < 1e-9, "450 de 500 apenas se mueve: los datos dominan"
assert mucho > poco, "Con la media suavizada, 450 de 500 queda por encima de 2 de 2"
"""),
            quiz("adb-quiz-credibilidad", "Intervalo de credibilidad", SK_BAYES,
                 "Un análisis bayesiano da un intervalo de credibilidad del 95 % de [4,1 %, 5,9 %] para la conversión. ¿Qué dice?",
                 ["Que el 95 % de los usuarios convierte entre 4,1 % y 5,9 %",
                  "Que, con el modelo y el prior elegidos, hay un 95 % de probabilidad de que la conversión real esté en ese rango",
                  "Que el experimento salió significativo",
                  "Lo mismo que un intervalo de confianza en cualquier caso"], 1,
                 "Esa lectura directa (\"95 % de probabilidad de que el valor esté aquí\") es justo la que permite el enfoque bayesiano y no el "
                 "intervalo de confianza frecuentista. El precio: depende del prior y del modelo."),
            quiz("adb-quiz-prior", "El papel del prior", SK_BAYES,
                 "¿Qué pasa con la influencia del prior a medida que acumulas muchos datos?",
                 ["Crece", "Se mantiene igual", "Se diluye: los datos dominan el posterior", "Desaparece con el primer dato"], 2,
                 "Con pocos datos el prior pesa mucho (y eso protege de conclusiones precipitadas); con muchos datos, casi cualquier prior "
                 "razonable lleva al mismo posterior."),
        ],
    },
    {
        "slug": "ad-series-tiempo",
        "title": "Series de tiempo y tendencias",
        "summary": "Tendencia, estacionalidad y ruido, medias móviles, variaciones e interanuales, CAGR, índices como Google Trends, "
                   "autocorrelación, anomalías, correlaciones espurias y pronósticos sencillos bien evaluados.",
        "hours": 7,
        "theory": _PENDIENTE,
        "exercises": [
            py("ads-movil", "Media móvil", SK_SERIES,
               "Escribe `media_movil(valores, ventana)`: devuelve la lista de medias de cada tramo de `ventana` valores consecutivos "
               "(la primera media usa los valores 0 a ventana - 1). El resultado tiene `len(valores) - ventana + 1` elementos.",
               starter="""
def media_movil(valores, ventana):
    # tu código aquí
    pass
""",
               solution="""
def media_movil(valores, ventana):
    return [sum(valores[i:i + ventana]) / ventana for i in range(len(valores) - ventana + 1)]
""",
               tests="""
assert media_movil([1, 2, 3, 4, 5], 3) == [2, 3, 4], "Medias de [1,2,3], [2,3,4] y [3,4,5]"
assert media_movil([10, 0, 10, 0], 2) == [5, 5, 5], "Una media móvil de 2 elimina un zigzag de periodo 2"
"""),
            py("ads-variacion", "Variación porcentual", SK_SERIES,
               "Escribe `variacion_porcentual(valores)`: la variación de cada periodo respecto al anterior, en porcentaje y redondeada a 2 "
               "decimales. Tiene un elemento menos que `valores`.",
               starter="""
def variacion_porcentual(valores):
    # tu código aquí
    pass
""",
               solution="""
def variacion_porcentual(valores):
    return [round((actual - previo) / previo * 100, 2) for previo, actual in zip(valores, valores[1:])]
""",
               tests="""
assert variacion_porcentual([100, 110, 99]) == [10.0, -10.0], "Subir un 10 % y bajar un 10 % no te deja donde estabas"
assert variacion_porcentual([200, 300]) == [50.0]
"""),
            py("ads-cagr", "Crecimiento anual compuesto (CAGR)", SK_SERIES,
               "Escribe `cagr(inicial, final, periodos)`: la tasa constante que lleva de `inicial` a `final` en `periodos` periodos: "
               "`(final / inicial) ** (1 / periodos) - 1`.",
               starter="""
def cagr(inicial, final, periodos):
    # tu código aquí
    pass
""",
               solution="""
def cagr(inicial, final, periodos):
    return (final / inicial) ** (1 / periodos) - 1
""",
               tests="""
assert abs(cagr(100, 200, 3) - 0.259921) < 1e-6, "Duplicar en 3 años es ~26 % anual, no 33 %"
assert abs(cagr(1000, 1000, 5)) < 1e-12, "Sin cambio, 0 %"
"""),
            py("ads-indice", "Índice como Google Trends", SK_SERIES,
               "Google Trends no da búsquedas absolutas: escala la serie para que el máximo valga 100. Escribe `indice_100(valores)` que haga lo "
               "mismo, redondeando a enteros con `round`. Si todos los valores son 0, devuelve todo ceros.",
               starter="""
def indice_100(valores):
    # tu código aquí
    pass
""",
               solution="""
def indice_100(valores):
    maximo = max(valores)
    if maximo == 0:
        return [0 for _ in valores]
    return [round(v / maximo * 100) for v in valores]
""",
               tests="""
assert indice_100([5, 10, 20]) == [25, 50, 100]
assert indice_100([0, 0]) == [0, 0], "Sin datos, todo ceros"
assert indice_100([3, 1000, 7]) == [0, 100, 1], "Un pico enorme aplasta el resto de la serie"
"""),
            py("ads-naive", "Evaluar un pronóstico ingenuo estacional", SK_SERIES,
               "El pronóstico **ingenuo estacional** predice que cada valor será igual al de hace un `periodo` (por ejemplo, el mismo día de la "
               "semana anterior). Escribe `mae_naive_estacional(valores, periodo)`: el error absoluto medio de ese pronóstico, evaluado desde la "
               "posición `periodo` hasta el final.",
               starter="""
def mae_naive_estacional(valores, periodo):
    # tu código aquí
    pass
""",
               solution="""
def mae_naive_estacional(valores, periodo):
    errores = [abs(valores[t] - valores[t - periodo]) for t in range(periodo, len(valores))]
    return sum(errores) / len(errores)
""",
               tests="""
assert mae_naive_estacional([10, 20, 10, 20, 12, 18], 2) == 1.0, "Errores 0, 0, 2 y 2"
assert mae_naive_estacional([5, 7, 9, 5, 7, 9], 3) == 0.0, "Una estacionalidad perfecta se predice sin error"
"""),
            quiz("ads-quiz-yoy", "¿Con qué comparas diciembre?", SK_SERIES,
                 "Tu tienda vende un 40 % más en diciembre que en noviembre. ¿Qué comparación dice si el negocio va mejor?",
                 ["Diciembre contra noviembre", "Diciembre de este año contra diciembre del año pasado (interanual)",
                  "Diciembre contra la media de todo el año", "Ninguna, las ventas no se pueden comparar"], 1,
                 "Diciembre siempre vende más por la temporada. La comparación interanual elimina la estacionalidad: compara la misma época."),
            quiz("ads-quiz-espuria", "Dos series que suben", SK_SERIES,
                 "El número de seguidores de tu cuenta y el precio del café tienen una correlación de 0,93 en los últimos dos años. ¿Qué pasa?",
                 ["El café te da seguidores", "Es una correlación espuria: dos series con tendencia suben juntas aunque no tengan relación",
                  "Tus seguidores toman café", "Hay que publicar sobre café"], 1,
                 "Las series con tendencia correlacionan entre sí casi siempre. Antes de comparar dos series, compara sus cambios "
                 "(diferencias de un periodo a otro) en vez de sus niveles."),
        ],
    },
]
