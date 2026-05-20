# De CSV a Dashboard — Proyecto Final Módulo 2

Flujo end-to-end de datos: extracción desde Kaggle, modelado relacional en TiDB Cloud, análisis exploratorio en Python y visualización interactiva con Streamlit.

**Autor:** Diego Asis · **Fecha:** Mayo 2026 · **Bootcamp:** Data & IA — Módulo 2

---

## Dataset

[TMDB 5000 Movies](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata) — disponible en Kaggle. Consta de dos archivos CSV:

- `tmdb_5000_movies.csv` — metadatos de películas (presupuesto, recaudación, géneros, fechas, etc.)
- `tmdb_5000_credits.csv` — reparto y equipo técnico de cada película

---

## Tecnologías utilizadas

| Herramienta | Uso |
|---|---|
| `pandas` | Carga, limpieza y análisis de datos |
| `mysql-connector-python` | Conexión y carga de datos en TiDB |
| `plotly` | Visualizaciones interactivas en el EDA |
| `streamlit` | Dashboard final |
| `pyarrow` | Serialización en formato pickle/parquet |
| **TiDB Cloud** | Base de datos relacional (MySQL-compatible) en la nube |

---

## Estructura del proyecto

```
.
├── proyectoModulo2.ipynb       # Notebook principal con el flujo completo
├── credenciales.py             # Configuración de conexión a TiDB (no incluir en Git)
├── tmdb_5000_movies.csv        # Dataset original (descargar desde Kaggle)
├── tmdb_5000_credits.csv       # Dataset original (descargar desde Kaggle)
├── dataset_analitico.pkl       # Dataset tras el JOIN SQL (generado en Fase 5)
├── dataset_analitico_limpio.pkl # Dataset tras limpieza (generado en Fase 6)
└── streamlit.py                      # Aplicación Streamlit (Fase 8)
```

---

## Fases del proyecto

### Fase 1 — Elección del dataset
Selección del dataset TMDB 5000 desde Kaggle. Se eligió por tener una relación de clave foránea clara entre las dos tablas (`movies.id` → `credits.movie_id`).

### Fase 2 — Conexión a TiDB Cloud
Registro en [TiDB Cloud](https://tidbcloud.com/) (plan gratuito Starter), creación del cluster y obtención de credenciales. La conexión se gestiona mediante `mysql-connector-python`.

```python
# credenciales.py (ejemplo)
mysql_config = {
    "host": "tu-host.tidbcloud.com",
    "port": 4000,
    "user": "tu-usuario",
    "password": "tu-contraseña",
    "database": "proyecto_modulo2",
    "ssl_ca": "ruta/al/cert.pem"
}
```

### Fase 3 — Modelado y exploración inicial
Carga de los CSV en DataFrames de pandas e inspección de tipos, nulos y estructura antes de definir el esquema SQL.

### Fase 4 — Carga de datos en TiDB
Inserción de los DataFrames en las tablas `movies` y `credits` usando `executemany` en lotes de 1000 filas para mayor eficiencia. Se renombró la columna `cast` a `cast_members` por ser palabra reservada en SQL.

### Fase 5 — Extracción del dataset analítico
JOIN entre `movies` y `credits` filtrando solo películas con `status = 'Released'`. El resultado se serializa en `dataset_analitico.pkl`.

### Fase 6 — Limpieza y preprocesamiento
- Conversión de `release_date` a tipo datetime
- Generación de columnas derivadas: `release_year`, `release_decade`, `release_month`
- Filtrado de películas con presupuesto ≥ $100k, recaudación ≥ $100k y duración entre 75 y 240 minutos
- Cálculo del ROI: `revenue / budget`
- Parseo de columnas JSON (`genres`, `crew`) para extraer listas de géneros y nombre del director

### Fase 7 — Análisis Exploratorio (EDA)
Seis preguntas de negocio analizadas con pandas y visualizadas con Plotly:

1. **¿Qué géneros son los más rentables?** — ROI mediano por género (top 10)
2. **¿Los presupuestos han aumentado con el tiempo?** — Presupuesto medio por década
3. **¿Hay directores que garanticen taquilla?** — Recaudación media de directores con ≥5 películas
4. **¿Qué mes concentra más estrenos exitosos?** — Revenue medio por mes de estreno
5. **¿Relación entre número de votos y recaudación?** — Scatter `vote_count` vs `revenue`
6. **¿Las películas más largas tienen mejor puntuación?** — Scatter `runtime` vs `vote_average`

### Fase 8 — Dashboard con Streamlit
Aplicación interactiva con métricas, filtros y gráficos generados a partir del dataset limpio.

---

## Instalación y uso

### 1. Clonar el repositorio y descargar los datos
```bash
git clone <url-del-repo>
cd <nombre-del-repo>
```
Descarga los CSV desde Kaggle y colócalos en la raíz del proyecto.

### 2. Instalar dependencias
```bash
pip install pandas mysql-connector-python plotly streamlit pyarrow
```

### 3. Configurar credenciales
Crea un archivo `credenciales.py` con los datos de conexión a tu cluster de TiDB Cloud (ver ejemplo en Fase 2). **No subas este archivo a Git.**

### 4. Ejecutar el notebook
Abre `proyectoModulo2.ipynb` en Jupyter y ejecuta las celdas en orden. Las fases 1–6 generan los archivos `.pkl`; la fase 7 produce las visualizaciones EDA.

### 5. Lanzar el dashboard
```bash
streamlit run app.py
```

---

## Notas

- El archivo `credenciales.py` contiene datos sensibles — añádelo a `.gitignore`.
- Los archivos `.pkl` son artefactos intermedios y pueden regenerarse ejecutando el notebook.
- El dataset TMDB está bajo licencia CC0 (dominio público).
