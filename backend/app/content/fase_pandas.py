from ._helpers import checklist, py, quiz

TOPICS = [
    {
        "slug": "pandas-basico",
        "phase": "pandas",
        "title": "pandas: Series, DataFrames y selección",
        "summary": "Estructuras de pandas, selección con loc/iloc, filtros booleanos, columnas nuevas y orden.",
        "hours": 12,
        "theory": r"""
# pandas: Series, DataFrames y selección

**pandas** es la librería central del análisis de datos en Python. Un `DataFrame` es una tabla (filas + columnas
con nombre); una `Series` es una sola columna.

```python
import pandas as pd

df = pd.DataFrame({
    "nombre": ["Ana", "Luis", "Carla"],
    "ciudad": ["Caracas", "Bogota", "Caracas"],
    "edad": [28, 35, 41],
})
df.head()          # primeras filas
df.shape           # (filas, columnas)
df.dtypes          # tipo de cada columna
df.describe()      # resumen estadístico de columnas numéricas
df["ciudad"].value_counts()   # frecuencias
```

Para cargar datos reales: `pd.read_csv("archivo.csv")`, `pd.read_excel(...)`, `pd.read_sql(consulta, conexion)`.

## Seleccionar columnas y filas

```python
df["edad"]                 # una columna (Series)
df[["nombre", "edad"]]     # varias columnas (DataFrame)
df.loc[0:1, "nombre"]      # por ETIQUETA (incluye el extremo final)
df.iloc[0:2, 0]            # por POSICIÓN (no incluye el extremo final)
```

## Filtrar con máscaras booleanas

```python
df[df["edad"] > 30]                              # una condición
df[(df["ciudad"] == "Caracas") & (df["edad"] > 30)]   # AND -> &, OR -> |, NOT -> ~
df[df["ciudad"].isin(["Caracas", "Bogota"])]
df.loc[df["ciudad"] == "Caracas", ["nombre", "edad"]]  # filtrar filas Y elegir columnas
```

**Siempre** pon cada condición entre paréntesis cuando uses `&` o `|`.

## Crear columnas y ordenar

```python
df["edad_en_10"] = df["edad"] + 10                # modifica df
df2 = df.assign(mayor=df["edad"] >= 30)           # devuelve una copia nueva
df.sort_values("edad", ascending=False)
df.sort_values(["ciudad", "edad"], ascending=[True, False])
```

## Trampas habituales

- **`SettingWithCopyWarning`:** aparece cuando modificas una "vista" de otro DataFrame. Haz `.copy()` cuando quieras una copia independiente.
- **Operaciones que no modifican:** la mayoría de métodos devuelven un resultado nuevo; si no lo asignas, se pierde.
- **Bucles `for` sobre filas:** casi siempre hay una operación vectorizada (`df["a"] * df["b"]`) mucho más rápida.
- **`loc` vs `iloc`:** `loc` usa etiquetas del índice, `iloc` posiciones. Tras filtrar, el índice conserva las etiquetas originales.

## Cómo sabes que dominas este tema

- Filtras con varias condiciones sin errores de paréntesis.
- Explicas la diferencia entre `loc` e `iloc`.
- Creas columnas calculadas sin bucles.
""",
        "exercises": [
            py("pd-filtrar", "Filtrar y ordenar", "pandas: selección y filtros",
               "Escribe `filtrar_caros(df)` que devuelva solo las filas con `precio` mayor a 100, ordenadas de mayor a menor precio.",
               starter="""
import pandas as pd

def filtrar_caros(df):
    # tu código aquí
    pass
""",
               solution="""
import pandas as pd

def filtrar_caros(df):
    return df[df["precio"] > 100].sort_values("precio", ascending=False)
""",
               tests="""
import pandas as pd
df = pd.DataFrame({"nombre": ["a", "b", "c", "d"], "precio": [50, 300, 120, 100]})
res = filtrar_caros(df)
assert list(res["nombre"]) == ["b", "c"], "Esperaba ['b', 'c'] (precio > 100, de mayor a menor) y obtuve %r" % list(res["nombre"])
""",
               hint="Máscara booleana + sort_values(..., ascending=False).", packages=["pandas"]),
            py("pd-total", "Columna calculada sin modificar el original", "pandas: selección y filtros",
               "Escribe `agregar_total(df)` que devuelva una **copia** del DataFrame con una columna nueva `total = cantidad * precio`. "
               "El DataFrame original **no** debe modificarse.",
               starter="""
import pandas as pd

def agregar_total(df):
    # tu código aquí
    pass
""",
               solution="""
import pandas as pd

def agregar_total(df):
    return df.assign(total=df["cantidad"] * df["precio"])
""",
               tests="""
import pandas as pd
df = pd.DataFrame({"cantidad": [1, 2, 3], "precio": [10.0, 5.0, 2.0]})
res = agregar_total(df)
assert res["total"].tolist() == [10.0, 10.0, 6.0], "total debe ser cantidad * precio"
assert "total" not in df.columns, "No modifiques el DataFrame original: usa assign o copy"
""",
               hint="df.assign(total=...) devuelve una copia.", packages=["pandas"]),
            py("pd-loc", "Filas y columnas con loc", "pandas: selección y filtros",
               "Escribe `caraquenos(df)` que devuelva solo las columnas `nombre` y `edad` de las filas donde `ciudad` es `'Caracas'`.",
               starter="""
import pandas as pd

def caraquenos(df):
    # tu código aquí
    pass
""",
               solution="""
import pandas as pd

def caraquenos(df):
    return df.loc[df["ciudad"] == "Caracas", ["nombre", "edad"]]
""",
               tests="""
import pandas as pd
df = pd.DataFrame({"nombre": ["Ana", "Luis", "Carla"], "ciudad": ["Caracas", "Bogota", "Caracas"], "edad": [28, 35, 41]})
res = caraquenos(df)
assert list(res.columns) == ["nombre", "edad"], "Debe devolver solo las columnas nombre y edad"
assert list(res["nombre"]) == ["Ana", "Carla"], "Solo deben quedar las filas de Caracas"
""",
               hint="df.loc[máscara, [columnas]]", packages=["pandas"]),
            py("pd-frecuencias", "Categorías más frecuentes", "pandas: selección y filtros",
               "Escribe `top_categorias(df, n)` que devuelva un diccionario `{categoria: cantidad}` con las `n` categorías más frecuentes "
               "de la columna `categoria` (de más a menos frecuente).",
               starter="""
import pandas as pd

def top_categorias(df, n):
    # pista: value_counts()
    pass
""",
               solution="""
import pandas as pd

def top_categorias(df, n):
    return df["categoria"].value_counts().head(n).to_dict()
""",
               tests="""
import pandas as pd
df = pd.DataFrame({"categoria": ["a", "b", "a", "c", "a", "b"]})
res = top_categorias(df, 2)
assert res == {"a": 3, "b": 2}, "Esperaba {'a': 3, 'b': 2} y obtuve %r" % (res,)
assert list(res.keys()) == ["a", "b"], "Mantén el orden de más a menos frecuente"
""",
               hint="df['categoria'].value_counts().head(n).to_dict()", packages=["pandas"]),
            quiz("pd-quiz-loc", "loc vs iloc", "pandas: selección y filtros",
                 "Un DataFrame tiene el índice `[10, 20, 30]`. ¿Qué devuelve `df.iloc[0]`?",
                 ["La fila con etiqueta 0 (da error)", "La primera fila (la de etiqueta 10)", "La última fila", "La primera columna"], 1,
                 "`iloc` trabaja por **posición**: la posición 0 es la primera fila, sea cual sea su etiqueta. `loc[0]` buscaría la etiqueta 0."),
        ],
    },
    {
        "slug": "pandas-limpieza",
        "phase": "pandas",
        "title": "Limpieza de datos con pandas",
        "summary": "Nulos, duplicados, tipos, fechas y texto sucio: el 60 % del trabajo real de un analista.",
        "hours": 12,
        "theory": r"""
# Limpieza de datos con pandas

Se suele decir que **el 60-80 % del trabajo de datos es limpiar**. Un análisis sobre datos sucios produce conclusiones
equivocadas con mucha seguridad. Este flujo te sirve casi siempre:

1. **Inspecciona:** `df.info()`, `df.describe(include="all")`, `df.isna().sum()`, `df.duplicated().sum()`.
2. **Decide** qué hacer con cada problema (y anótalo: es parte del análisis).
3. **Aplica** transformaciones en un script reproducible, no a mano.
4. **Valida** el resultado (rangos, unicidad, conteos).

## Valores nulos

```python
df.isna().sum()                      # nulos por columna
df.dropna(subset=["email"])          # eliminar filas sin email
df["edad"] = df["edad"].fillna(df["edad"].median())   # imputar con la mediana
df["ciudad"] = df["ciudad"].fillna("desconocida")
```

¿Eliminar o imputar? Depende: si faltan pocos y al azar, eliminar es válido; si faltan muchos o hay un patrón
(por ejemplo, solo faltan en un canal), **investiga por qué** antes de rellenar. Prefiere la **mediana** a la media
cuando hay valores extremos.

## Duplicados

```python
df.duplicated(subset=["email"]).sum()
df = df.drop_duplicates(subset=["email"], keep="first")
```

## Tipos de datos y fechas

```python
df["monto"] = pd.to_numeric(df["monto"], errors="coerce")      # lo no numérico -> NaN
df["fecha"] = pd.to_datetime(df["fecha"], errors="coerce")     # lo inválido -> NaT
df["categoria"] = df["categoria"].astype("category")
df["mes"] = df["fecha"].dt.to_period("M")
```

`errors="coerce"` convierte lo que no se puede parsear en nulo en lugar de romper todo. **Cuenta cuántos** quedaron
nulos: si son muchos, hay un problema de formato que resolver.

## Texto sucio

```python
df["nombre"] = df["nombre"].str.strip().str.lower()
df["telefono"] = df["telefono"].str.replace(r"\D", "", regex=True)   # solo dígitos
df["pais"] = df["pais"].replace({"VE": "Venezuela", "ve": "Venezuela"})
```

## Outliers (valores atípicos)

Un valor extremo puede ser un error de captura o un caso real importante. Detecta con el rango intercuartil:

```python
q1, q3 = df["monto"].quantile([0.25, 0.75])
iqr = q3 - q1
atipicos = df[(df["monto"] < q1 - 1.5 * iqr) | (df["monto"] > q3 + 1.5 * iqr)]
```

No los borres automáticamente: **míralos primero**.

## Cómo sabes que dominas este tema

- Sigues siempre el ciclo inspeccionar → decidir → aplicar → validar.
- Usas `errors="coerce"` y cuentas lo que falló.
- Documentas cada decisión de limpieza (qué hiciste y por qué).
""",
        "exercises": [
            py("pdl-texto", "Normalizar texto", "pandas: limpieza",
               "Escribe `limpiar_nombres(serie)` que reciba una Series de textos y devuelva otra con los espacios sobrantes quitados y todo en minúsculas. "
               "Los valores nulos deben seguir siendo nulos.",
               starter="""
import pandas as pd

def limpiar_nombres(serie):
    # tu código aquí
    pass
""",
               solution="""
import pandas as pd

def limpiar_nombres(serie):
    return serie.str.strip().str.lower()
""",
               tests="""
import pandas as pd
res = limpiar_nombres(pd.Series(["  Ana ", "LUIS", None]))
assert res.iloc[0] == "ana" and res.iloc[1] == "luis", "Esperaba ['ana', 'luis', nulo]"
assert pd.isna(res.iloc[2]), "El valor nulo debe seguir siendo nulo"
""",
               hint="serie.str.strip().str.lower()", packages=["pandas"]),
            py("pdl-nulos", "Imputar valores nulos", "pandas: limpieza",
               "Escribe `rellenar_nulos(df)` que devuelva una copia donde los nulos de `edad` se rellenen con la **mediana** de `edad` "
               "y los de `ciudad` con el texto `'desconocida'`.",
               starter="""
import pandas as pd

def rellenar_nulos(df):
    # tu código aquí
    pass
""",
               solution="""
import pandas as pd

def rellenar_nulos(df):
    resultado = df.copy()
    resultado["edad"] = resultado["edad"].fillna(resultado["edad"].median())
    resultado["ciudad"] = resultado["ciudad"].fillna("desconocida")
    return resultado
""",
               tests="""
import pandas as pd
df = pd.DataFrame({"edad": [20.0, None, 40.0, 30.0], "ciudad": ["Caracas", None, "Bogota", "Quito"]})
res = rellenar_nulos(df)
assert res["edad"].isna().sum() == 0 and res["ciudad"].isna().sum() == 0, "No deben quedar nulos"
assert res["edad"].tolist() == [20.0, 30.0, 40.0, 30.0], "La mediana de [20, 40, 30] es 30"
assert res["ciudad"].tolist()[1] == "desconocida"
assert df["edad"].isna().sum() == 1, "No modifiques el DataFrame original"
""",
               hint="fillna(valor) en cada columna; usa .copy() para no tocar el original.", packages=["pandas"]),
            py("pdl-duplicados", "Eliminar duplicados", "pandas: limpieza",
               "Escribe `quitar_duplicados(df)` que elimine las filas con `email` repetido, conservando la **primera** aparición.",
               starter="""
import pandas as pd

def quitar_duplicados(df):
    # tu código aquí
    pass
""",
               solution="""
import pandas as pd

def quitar_duplicados(df):
    return df.drop_duplicates(subset=["email"], keep="first")
""",
               tests="""
import pandas as pd
df = pd.DataFrame({"email": ["a@x.com", "b@x.com", "a@x.com"], "nombre": ["Ana", "Beto", "Ana v2"]})
res = quitar_duplicados(df)
assert len(res) == 2, "Deben quedar 2 filas"
assert res["nombre"].tolist() == ["Ana", "Beto"], "Conserva la primera aparición de cada email"
""",
               hint="drop_duplicates(subset=[...], keep='first')", packages=["pandas"]),
            py("pdl-fechas", "Convertir fechas con seguridad", "pandas: limpieza",
               "Escribe `convertir_fechas(df)` que devuelva una copia donde la columna `fecha` (texto) pase a tipo fecha. "
               "Los textos que no sean fechas válidas deben quedar como nulos (`NaT`), sin lanzar error.",
               starter="""
import pandas as pd

def convertir_fechas(df):
    # tu código aquí
    pass
""",
               solution="""
import pandas as pd

def convertir_fechas(df):
    resultado = df.copy()
    resultado["fecha"] = pd.to_datetime(resultado["fecha"], errors="coerce")
    return resultado
""",
               tests="""
import pandas as pd
df = pd.DataFrame({"fecha": ["2024-01-15", "no es fecha", "2024-03-01"]})
res = convertir_fechas(df)
assert pd.api.types.is_datetime64_any_dtype(res["fecha"]), "La columna debe ser de tipo datetime"
assert res["fecha"].isna().sum() == 1, "El texto inválido debe quedar como NaT"
assert res["fecha"].dt.month.dropna().tolist() == [1, 3]
""",
               hint="pd.to_datetime(columna, errors='coerce')", packages=["pandas"]),
            quiz("pdl-quiz", "Qué hacer con los nulos", "pandas: limpieza",
                 "En una columna `ingresos` falta el 40 % de los valores y casi todos los faltantes son de clientes de un mismo canal. "
                 "¿Cuál es la mejor primera acción?",
                 ["Rellenar con la media y seguir", "Eliminar toda la columna sin mirar", "Investigar por qué faltan en ese canal antes de decidir",
                  "Rellenar con ceros"], 2,
                 "Cuando los nulos tienen un patrón, rellenar sin entender puede sesgar el análisis. Primero averigua la causa (error de captura, dato no aplicable...)."),
        ],
    },
    {
        "slug": "pandas-transformacion",
        "phase": "pandas",
        "title": "groupby, merge y pivot",
        "summary": "Agrupar y resumir, unir tablas, tablas dinámicas y agregaciones con nombre.",
        "hours": 12,
        "theory": r"""
# groupby, merge y pivot

Es el equivalente en pandas de `GROUP BY`, `JOIN` y las tablas dinámicas. Si ya dominas SQL, **piensa en SQL y traduce**.

## groupby: dividir, aplicar, combinar

```python
ventas.groupby("categoria")["monto"].sum()                      # una métrica
ventas.groupby("categoria", as_index=False)["monto"].sum()      # como DataFrame
ventas.groupby(["mes", "categoria"])["monto"].agg(["count", "sum", "mean"])
```

**Agregaciones con nombre** (la forma más legible):

```python
resumen = ventas.groupby("cliente_id").agg(
    n_pedidos=("pedido_id", "count"),
    total=("monto", "sum"),
    promedio=("monto", "mean"),
).reset_index()
```

`transform` devuelve un valor **por fila** (como una función de ventana en SQL):

```python
ventas["pct_categoria"] = ventas["monto"] / ventas.groupby("categoria")["monto"].transform("sum")
```

## merge: unir tablas

```python
pd.merge(clientes, pedidos, on="cliente_id", how="left")
pd.merge(a, b, left_on="id", right_on="cliente_id", how="inner", validate="one_to_many")
```

`how` equivale a INNER/LEFT/RIGHT/OUTER. **Usa `validate=`** (`"one_to_one"`, `"one_to_many"`...) para que pandas
falle si la relación no es la que esperabas: es la mejor defensa contra filas duplicadas por error.

## pivot_table: de largo a ancho

```python
pd.pivot_table(ventas, index="mes", columns="categoria", values="monto",
               aggfunc="sum", fill_value=0)
```

Lo contrario (de ancho a largo) es `df.melt(id_vars=[...])`, útil para graficar.

## concat y apilar

```python
pd.concat([enero, febrero], ignore_index=True)    # apilar filas con las mismas columnas
```

## Trampas habituales

- **Filas duplicadas tras un merge:** una clave repetida en ambas tablas produce combinaciones múltiples. Comprueba `len()` antes y después.
- **Tipos distintos en la clave** (`"1"` vs `1`) hacen que no haya coincidencias.
- **`groupby` ignora los nulos de la clave** por defecto (`dropna=False` para conservarlos).
- Después de agrupar el índice cambia: usa `reset_index()` o `as_index=False`.

## Cómo sabes que dominas este tema

- Traduces cualquier consulta con `GROUP BY` a pandas y al revés.
- Usas `validate=` en tus merges.
- Sabes cuándo usar `transform` en vez de `agg`.
""",
        "exercises": [
            py("pdt-groupby", "Ventas por categoría", "pandas: groupby, merge y pivot",
               "Escribe `ventas_por_categoria(df)` que devuelva un DataFrame con las columnas `categoria` y `total` (suma de `monto`), "
               "ordenado de mayor a menor `total`.",
               starter="""
import pandas as pd

def ventas_por_categoria(df):
    # tu código aquí
    pass
""",
               solution="""
import pandas as pd

def ventas_por_categoria(df):
    resumen = df.groupby("categoria", as_index=False)["monto"].sum()
    resumen = resumen.rename(columns={"monto": "total"})
    return resumen.sort_values("total", ascending=False)
""",
               tests="""
import pandas as pd
df = pd.DataFrame({"categoria": ["A", "B", "A", "C", "B"], "monto": [10, 50, 20, 5, 30]})
res = ventas_por_categoria(df)
assert list(res.columns) == ["categoria", "total"], "Las columnas deben ser ['categoria', 'total']"
assert res["categoria"].tolist() == ["B", "A", "C"], "Orden esperado: B (80), A (30), C (5)"
assert res["total"].tolist() == [80, 30, 5]
""",
               hint="groupby(..., as_index=False)[...].sum() + rename + sort_values.", packages=["pandas"]),
            py("pdt-merge", "Unir clientes con pedidos", "pandas: groupby, merge y pivot",
               "Escribe `combinar(clientes, pedidos)` que una ambas tablas por `cliente_id` conservando **todos los clientes** "
               "(aunque no tengan pedidos).",
               starter="""
import pandas as pd

def combinar(clientes, pedidos):
    # tu código aquí
    pass
""",
               solution="""
import pandas as pd

def combinar(clientes, pedidos):
    return pd.merge(clientes, pedidos, on="cliente_id", how="left")
""",
               tests="""
import pandas as pd
clientes = pd.DataFrame({"cliente_id": [1, 2, 3], "nombre": ["Ana", "Luis", "Carla"]})
pedidos = pd.DataFrame({"pedido_id": [10, 11, 12], "cliente_id": [1, 1, 2], "monto": [50, 70, 20]})
res = combinar(clientes, pedidos)
assert len(res) == 4, "Ana tiene 2 pedidos, Luis 1 y Carla 0 -> 4 filas; obtuve %d" % len(res)
assert res.loc[res["cliente_id"] == 3, "monto"].isna().all(), "Carla no tiene pedidos: monto debe ser nulo"
""",
               hint="how='left'", packages=["pandas"]),
            py("pdt-pivot", "Tabla dinámica", "pandas: groupby, merge y pivot",
               "Escribe `tabla_mensual(df)` que devuelva una tabla dinámica con `mes` en las filas, `categoria` en las columnas y la suma de `monto` "
               "como valores. Los huecos deben ser `0`.",
               starter="""
import pandas as pd

def tabla_mensual(df):
    # tu código aquí
    pass
""",
               solution="""
import pandas as pd

def tabla_mensual(df):
    return pd.pivot_table(df, index="mes", columns="categoria", values="monto", aggfunc="sum", fill_value=0)
""",
               tests="""
import pandas as pd
df = pd.DataFrame({"mes": ["2024-01", "2024-01", "2024-02"], "categoria": ["A", "B", "A"], "monto": [10, 5, 7]})
res = tabla_mensual(df)
assert res.loc["2024-01", "A"] == 10 and res.loc["2024-01", "B"] == 5, "Revisa index/columns/values"
assert res.loc["2024-02", "B"] == 0, "Los huecos deben rellenarse con 0 (fill_value=0)"
""",
               hint="pd.pivot_table(df, index=..., columns=..., values=..., aggfunc='sum', fill_value=0)", packages=["pandas"]),
            py("pdt-agg", "Agregaciones con nombre", "pandas: groupby, merge y pivot",
               "Escribe `resumen_clientes(df)` que agrupe por `cliente_id` y devuelva un DataFrame (con `cliente_id` como columna) con: "
               "`n_pedidos` (cantidad de filas), `total` (suma de `monto`) y `promedio` (media de `monto`).",
               starter="""
import pandas as pd

def resumen_clientes(df):
    # pista: groupby(...).agg(nombre=(columna, funcion)).reset_index()
    pass
""",
               solution="""
import pandas as pd

def resumen_clientes(df):
    return df.groupby("cliente_id").agg(
        n_pedidos=("monto", "count"),
        total=("monto", "sum"),
        promedio=("monto", "mean"),
    ).reset_index()
""",
               tests="""
import pandas as pd
df = pd.DataFrame({"cliente_id": [1, 1, 2], "monto": [10.0, 30.0, 8.0]})
res = resumen_clientes(df)
assert list(res.columns) == ["cliente_id", "n_pedidos", "total", "promedio"], "Columnas esperadas: cliente_id, n_pedidos, total, promedio"
fila = res[res["cliente_id"] == 1].iloc[0]
assert fila["n_pedidos"] == 2 and fila["total"] == 40.0 and fila["promedio"] == 20.0
""",
               hint="agg(n_pedidos=('monto','count'), ...)", packages=["pandas"]),
            quiz("pdt-quiz", "Merge que multiplica filas", "pandas: groupby, merge y pivot",
                 "Unes `pedidos` (1000 filas) con `clientes` por `cliente_id` y el resultado tiene 1350 filas. ¿Cuál es la causa más probable?",
                 ["pandas agrega filas aleatorias", "La clave cliente_id está duplicada en clientes", "Usaste how='left'", "Faltan índices"], 1,
                 "Si la clave se repite en la tabla de clientes, cada pedido se combina con **todas** las filas duplicadas. "
                 "`validate='many_to_one'` habría detectado el problema."),
        ],
    },
    {
        "slug": "visualizacion",
        "phase": "pandas",
        "title": "Visualización de datos",
        "summary": "Elegir el gráfico correcto, matplotlib/seaborn y principios para no engañar.",
        "hours": 10,
        "theory": r"""
# Visualización de datos

Un buen gráfico responde **una pregunta** de un vistazo. Un mal gráfico confunde o, peor, engaña.

## 1. Elige el gráfico según la pregunta

| Pregunta | Gráfico |
|---|---|
| ¿Cómo cambia en el tiempo? | **Líneas** |
| ¿Cómo se comparan categorías? | **Barras** (horizontales si los nombres son largos) |
| ¿Cómo se distribuye una variable? | **Histograma** o **boxplot** |
| ¿Hay relación entre dos variables numéricas? | **Dispersión** (scatter) |
| ¿Qué parte del total es cada una? | Barras apiladas o barras ordenadas (los gráficos de pastel solo con 2-3 partes) |

## 2. matplotlib: la base

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(8, 4))
ax.bar(["A", "B", "C"], [30, 55, 20])
ax.set_title("Ventas por categoria")
ax.set_xlabel("Categoria")
ax.set_ylabel("Ventas (miles de USD)")
plt.show()
```

Con pandas es aún más corto: `df.plot(kind="bar", x="categoria", y="ventas")`.
**seaborn** añade gráficos estadísticos con mejor estilo: `sns.histplot(df["monto"])`, `sns.boxplot(data=df, x="canal", y="monto")`.

## 3. Principios para no engañar

- **Las barras empiezan en cero.** Truncar el eje exagera diferencias.
- **Ordena** las categorías por valor (no alfabéticamente), salvo que el orden sea natural (meses).
- **Título que diga la conclusión**: "Las ventas crecieron 18 % en el Q2" informa más que "Ventas por mes".
- **Menos colores:** uno para destacar, gris para el resto. Evita arcoíris sin significado.
- **Etiquetas y unidades** siempre claras. Quita lo que no aporta (rejillas pesadas, bordes, 3D).
- **Accesibilidad:** no dependas solo del color (también ~8 % de los hombres tiene daltonismo).

## 4. Errores clásicos

- Doble eje Y que sugiere una correlación inexistente.
- Gráficos de pastel con muchas porciones.
- Comparar áreas o volúmenes en lugar de longitudes.
- Mostrar solo el promedio y esconder la distribución: dos grupos con el mismo promedio pueden ser muy distintos.

## Cómo sabes que dominas este tema

- Eliges el gráfico en segundos según la pregunta.
- Tus gráficos tienen título-conclusión, ejes etiquetados y un solo color de énfasis.
- Detectas gráficos engañosos en noticias y presentaciones.
""",
        "exercises": [
            py("viz-barras", "Gráfico de barras", "Visualización",
               "Escribe `grafico_barras(categorias, valores)` que cree un gráfico de barras con matplotlib y devuelva el objeto `ax` (ejes). "
               "Título: `'Ventas por categoria'` y etiqueta del eje Y: `'Ventas'`.",
               starter="""
import matplotlib.pyplot as plt

def grafico_barras(categorias, valores):
    fig, ax = plt.subplots()
    # tu código aquí
    return ax
""",
               solution="""
import matplotlib.pyplot as plt

def grafico_barras(categorias, valores):
    fig, ax = plt.subplots()
    ax.bar(categorias, valores)
    ax.set_title("Ventas por categoria")
    ax.set_ylabel("Ventas")
    return ax
""",
               tests="""
ax = grafico_barras(["A", "B"], [3, 5])
assert ax.get_title() == "Ventas por categoria", "El titulo debe ser 'Ventas por categoria'"
assert ax.get_ylabel() == "Ventas", "El eje Y debe llamarse 'Ventas'"
assert [p.get_height() for p in ax.patches] == [3, 5], "Debe haber una barra por categoria con su valor"
""",
               hint="ax.bar(...), ax.set_title(...), ax.set_ylabel(...)", packages=["matplotlib"]),
            py("viz-lineas", "Serie temporal", "Visualización",
               "Escribe `grafico_lineas(meses, ventas)` que dibuje una línea con matplotlib y devuelva `ax`. Título: `'Ventas mensuales'` y etiqueta del eje X: `'Mes'`.",
               starter="""
import matplotlib.pyplot as plt

def grafico_lineas(meses, ventas):
    fig, ax = plt.subplots()
    # tu código aquí
    return ax
""",
               solution="""
import matplotlib.pyplot as plt

def grafico_lineas(meses, ventas):
    fig, ax = plt.subplots()
    ax.plot(meses, ventas)
    ax.set_title("Ventas mensuales")
    ax.set_xlabel("Mes")
    return ax
""",
               tests="""
ax = grafico_lineas([1, 2, 3], [10, 20, 15])
assert ax.get_title() == "Ventas mensuales", "Titulo esperado: 'Ventas mensuales'"
assert ax.get_xlabel() == "Mes", "Etiqueta X esperada: 'Mes'"
assert len(ax.lines) == 1 and list(ax.lines[0].get_ydata()) == [10, 20, 15], "Dibuja una sola linea con ax.plot"
""",
               hint="ax.plot(x, y)", packages=["matplotlib"]),
            quiz("viz-quiz-1", "Elegir el gráfico", "Visualización",
                 "Quieres mostrar cómo evolucionó la tasa de cancelación mes a mes durante 2 años. ¿Qué gráfico es el más adecuado?",
                 ["Pastel", "Líneas", "Histograma", "Dispersión sin orden"], 1,
                 "Para una variable que cambia en el tiempo, el gráfico de líneas deja ver tendencia y estacionalidad."),
            quiz("viz-quiz-2", "Eje truncado", "Visualización",
                 "Un gráfico de barras tiene el eje Y empezando en 95 en lugar de 0, y la barra de 98 se ve el doble de alta que la de 96. ¿Cuál es el problema?",
                 ["Ninguno, es un buen uso del espacio", "Exagera visualmente una diferencia pequeña: las barras deben empezar en cero",
                  "Faltan colores", "Debería ser un gráfico de pastel"], 1,
                 "La **longitud** de una barra representa su valor; si no parte de cero, la proporción visual no coincide con la real."),
            checklist("viz-check", "Revisa uno de tus gráficos", "Visualización",
                      "Toma un gráfico de tu proyecto y comprueba cada punto. Márcalos cuando los cumplas.",
                      ["El título dice la conclusión, no solo el tema", "Los ejes tienen etiqueta y unidades",
                       "Las barras empiezan en cero", "Las categorías están ordenadas con criterio",
                       "Uso un color de énfasis y el resto en gris", "No hay elementos decorativos innecesarios"]),
        ],
    },
]
