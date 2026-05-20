import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Análisis de películas TMDB",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Paleta ────────────────────────────────────────────────────────────────────
BG        = "#f7f6f2"
CARD_BG   = "#f0efe9"
BORDER    = "#e2e0d8"
GREEN     = "#1D9E75"
TEXT_DARK = "#1a1a18"
TEXT_MID  = "#6b6b68"
TEXT_DIM  = "#aaa9a5"

# ── CSS global ────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;600&display=swap');

html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {{
    background: {BG} !important;
    font-family: 'DM Sans', sans-serif;
}}

[data-testid="stSidebar"] {{
    background: {CARD_BG} !important;
    border-right: 1px solid {BORDER};
}}
[data-testid="stSidebar"] * {{
    font-family: 'DM Sans', sans-serif !important;
    color: {TEXT_MID} !important;
}}

/* Tags verdes del multiselect */
[data-testid="stSidebar"] span[data-baseweb="tag"] {{
    background: rgba(29,158,117,0.15) !important;
    border: 1px solid rgba(29,158,117,0.35) !important;
}}
[data-testid="stSidebar"] span[data-baseweb="tag"] span {{
    color: {GREEN} !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 11px !important;
}}
[data-testid="stSidebar"] span[data-baseweb="tag"] button span {{
    color: {GREEN} !important;
}}

/* Botón colapsar sidebar */
button[data-testid="baseButton-header"],
[data-testid="collapsedControl"],
button[aria-label="Close sidebar"],
button[aria-label="Open sidebar"] {{
    font-size: 0 !important;
    background: transparent !important;
    border: 1px solid {BORDER} !important;
    border-radius: 6px !important;
    width: 28px !important;
    height: 28px !important;
}}
button[data-testid="baseButton-header"]::after,
[data-testid="collapsedControl"]::after,
button[aria-label="Close sidebar"]::after,
button[aria-label="Open sidebar"]::after {{
    content: '‹';
    font-size: 18px;
    color: {TEXT_MID};
    font-family: sans-serif;
    line-height: 1;
}}

/* Ocultar topbar / toolbar de Streamlit — múltiples versiones */
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stHeader"],
header[data-testid="stHeader"],
#MainMenu,
footer,
.stDeployButton {{
    display: none !important;
    visibility: hidden !important;
    height: 0 !important;
}}

[data-testid="stMetric"] {{
    background: {CARD_BG};
    border: 1px solid {BORDER};
    border-radius: 10px;
    padding: 20px 24px !important;
}}
[data-testid="stMetricLabel"] {{
    font-family: 'Space Mono', monospace !important;
    font-size: 10px !important;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: {TEXT_DIM} !important;
}}
[data-testid="stMetricValue"] {{
    font-family: 'DM Sans', sans-serif !important;
    font-size: 28px !important;
    font-weight: 600 !important;
    color: {TEXT_DARK} !important;
}}

[data-testid="stPlotlyChart"] {{
    background: {CARD_BG};
    border: 1px solid {BORDER};
    border-radius: 10px;
    padding: 8px;
}}

h1, h2, h3 {{
    font-family: 'DM Sans', sans-serif !important;
    color: {TEXT_DARK} !important;
}}
</style>
""", unsafe_allow_html=True)


# ── Header principal ──────────────────────────────────────────────────────────
st.markdown(f"""
<div style="background:{BG};background-image:linear-gradient(rgba(29,158,117,0.05) 1px,transparent 1px),linear-gradient(90deg,rgba(29,158,117,0.05) 1px,transparent 1px);background-size:40px 40px;border-radius:14px;padding:48px 0 40px;box-sizing:border-box;margin-bottom:32px;">
  <div style="border-left:4px solid {GREEN};padding-left:24px;">
    <p style="font-family:'Space Mono',monospace;font-size:11px;color:{GREEN};letter-spacing:0.15em;text-transform:uppercase;margin:0 0 12px;">Bootcamp Data &amp; IA · Módulo 2 · Proyecto Final</p>
    <h1 style="font-family:'DM Sans',sans-serif;font-size:52px;font-weight:600;color:{TEXT_DARK};line-height:1.05;margin:0 0 6px;letter-spacing:-0.02em;">Análisis de películas <span style="color:{GREEN};">TMDB</span></h1>
    <p style="font-size:16px;font-weight:400;color:{TEXT_MID};margin:14px 0 0;line-height:1.6;max-width:620px;">Exploración de rentabilidad, taquilla, presupuesto, géneros, directores e idioma original a partir del dataset TMDB 5000 Movies.</p>
  </div>
</div>
""", unsafe_allow_html=True)


# ── Datos ─────────────────────────────────────────────────────────────────────
@st.cache_data
def cargar_datos():
    return pd.read_pickle("dataset_analitico_limpio.pkl")

df = cargar_datos()
df["release_decade"] = df["release_decade"].astype(int)


# ── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.markdown(f"""
<p style="font-family:'Space Mono',monospace;font-size:11px;color:{GREEN};letter-spacing:0.12em;text-transform:uppercase;margin-bottom:4px;">Filtros</p>
""", unsafe_allow_html=True)

decadas = st.sidebar.multiselect(
    "Década",
    sorted(df["release_decade"].dropna().unique()),
    default=sorted(df["release_decade"].dropna().unique())
)

directores = st.sidebar.multiselect(
    "Director",
    sorted(df["director"].dropna().unique()),
    default=[]
)

df_f = df[df["release_decade"].isin(decadas)]
if directores:
    df_f = df_f[df_f["director"].isin(directores)]

# ── Guard: sin datos ──────────────────────────────────────────────────────────
if df_f.empty:
    st.markdown(f"""
<div style="background:{CARD_BG};border:1px solid {BORDER};border-left:4px solid #c47d10;border-radius:10px;padding:28px 32px;margin-top:32px;box-sizing:border-box;">
  <p style="font-family:'Space Mono',monospace;font-size:10px;color:#c47d10;letter-spacing:0.12em;text-transform:uppercase;margin:0 0 10px;">Sin resultados</p>
  <p style="font-size:15px;color:{TEXT_MID};margin:0;line-height:1.6;">No hay datos para los filtros seleccionados. Selecciona al menos una década.</p>
</div>
""", unsafe_allow_html=True)
    st.stop()

# ── Métricas ──────────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns(3)
col1.metric("Películas",     len(df_f))
col2.metric("Revenue medio", f"${df_f['revenue'].mean():,.0f}")
col3.metric("ROI mediano",   f"{df_f['ROI'].median():.2f}")

st.markdown("<div style='margin-top:32px'></div>", unsafe_allow_html=True)


# ── Helper: section header ────────────────────────────────────────────────────
def section_header(tag, titulo, desc, color=GREEN, color_rgba="rgba(29,158,117,0.12)", border_rgba="rgba(29,158,117,0.3)"):
    st.markdown(f"""
<div style="background:{BG};background-image:linear-gradient(rgba(29,158,117,0.05) 1px,transparent 1px),linear-gradient(90deg,rgba(29,158,117,0.05) 1px,transparent 1px);background-size:40px 40px;border-radius:10px;padding:20px 28px 22px;margin:32px 0 16px;box-sizing:border-box;">
  <span style="display:inline-block;font-family:'Space Mono',monospace;font-size:11px;font-weight:700;padding:4px 12px;border-radius:6px;background:{color_rgba};color:{color};border:1px solid {border_rgba};vertical-align:middle;margin-right:14px;">{tag}</span><span style="font-size:20px;font-weight:600;color:{TEXT_DARK};vertical-align:middle;">{titulo}</span>
  <span style="display:block;font-size:13px;color:{TEXT_MID};margin-top:8px;">{desc}</span>
</div>
""", unsafe_allow_html=True)


# ── Plotly base layout ────────────────────────────────────────────────────────
PLOT_LAYOUT = dict(
    paper_bgcolor=CARD_BG,
    plot_bgcolor=CARD_BG,
    font=dict(family="DM Sans, sans-serif", color=TEXT_MID),
    title_font=dict(family="DM Sans, sans-serif", color=TEXT_DARK, size=16),
    title_x=0.5,
    margin=dict(t=48, b=32, l=32, r=32),
)


# ── Gráfico 1: ROI por género ─────────────────────────────────────────────────
section_header("Géneros", "Géneros más rentables", "ROI mediano por género · Top 10",
               color="#2a7fd4", color_rgba="rgba(55,138,221,0.12)", border_rgba="rgba(55,138,221,0.3)")

df_generos = df_f.explode("genres_parsed")
roi_generos = (
    df_generos
    .groupby("genres_parsed")["ROI"]
    .median()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)
roi_generos.columns = ["Género", "ROI mediano"]

fig1 = px.bar(
    roi_generos,
    x="ROI mediano",
    y="Género",
    orientation="h",
    color="ROI mediano",
    color_continuous_scale=[[0, "#d4eaf7"], [1, "#2a7fd4"]],
    title=" ",
)
fig1.update_layout(**PLOT_LAYOUT, yaxis=dict(autorange="reversed"), coloraxis_showscale=False)
fig1.update_traces(marker_line_width=0)
st.plotly_chart(fig1, use_container_width=True)


# ── Gráfico 2: Presupuesto por década ────────────────────────────────────────
section_header("Presupuesto", "Evolución del presupuesto", "Presupuesto medio por década",
               color="#c47d10", color_rgba="rgba(186,117,23,0.12)", border_rgba="rgba(186,117,23,0.3)")

budget_decada = (
    df_f
    .groupby("release_decade")["budget"]
    .mean()
    .sort_index()
)

fig2 = px.line(
    x=budget_decada.index,
    y=budget_decada.values,
    markers=True,
    labels={"x": "Década", "y": "Presupuesto medio (USD)"},
    title=" ",
)
fig2.update_traces(line_color="#c47d10", marker_color="#c47d10", marker_size=8)
fig2.update_layout(**PLOT_LAYOUT)
st.plotly_chart(fig2, use_container_width=True)


# ── Gráfico 3: Directores con mayor recaudación ───────────────────────────────
section_header("Directores", "Directores con mayor recaudación", "Recaudación media · Top 10",
               color=GREEN, color_rgba="rgba(29,158,117,0.12)", border_rgba="rgba(29,158,117,0.3)")

numero_directores = (df_f["director"].value_counts())
directores_varias_peliculas = (numero_directores[numero_directores >= 5].index)
df_directores = df_f[df_f["director"].isin(directores_varias_peliculas)]

revenue_director = (
    df_directores.groupby("director")["revenue"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)
revenue_director.columns = ["Director", "Recaudación media (USD)"]

fig3 = px.bar(
    revenue_director,
    x="Recaudación media (USD)",
    y="Director",
    orientation="h",
    color="Recaudación media (USD)",
    color_continuous_scale=[[0, "#d4f0e7"], [1, GREEN]],
    title=" ",
)
fig3.update_layout(
    **PLOT_LAYOUT,
    yaxis=dict(autorange="reversed"),
    bargap=0.4,
    coloraxis_showscale=False,
)
fig3.update_yaxes(ticklabelstandoff=20)
fig3.update_traces(marker_line_width=0)
st.plotly_chart(fig3, use_container_width=True)


# ── Gráfico 4: Recaudación por mes ───────────────────────────────────────────
section_header("Estacionalidad", "Recaudación por mes de estreno", "Revenue medio según el mes de lanzamiento",
               color="#5a52c7", color_rgba="rgba(83,74,183,0.12)", border_rgba="rgba(83,74,183,0.3)")

revenue_mes = (
    df_f.groupby("release_month")["revenue"]
    .mean()
    .sort_index()
    .round(2)
)
meses = {1.0:"Ene", 2.0:"Feb", 3.0:"Mar", 4.0:"Abr", 5.0:"May", 6.0:"Jun",
         7.0:"Jul", 8.0:"Ago", 9.0:"Sep", 10.0:"Oct", 11.0:"Nov", 12.0:"Dic"}
revenue_mes.index = revenue_mes.index.map(meses)
revenue_mes = revenue_mes.reset_index()
revenue_mes.columns = ["Mes", "Revenue medio (USD)"]

fig4 = px.bar(
    revenue_mes,
    x="Mes",
    y="Revenue medio (USD)",
    color="Revenue medio (USD)",
    color_continuous_scale=[[0, "#e8e4f7"], [1, "#5a52c7"]],
    title=" ",
)
fig4.update_layout(**PLOT_LAYOUT, coloraxis_showscale=False)
fig4.update_traces(marker_line_width=0)
st.plotly_chart(fig4, use_container_width=True)


# ── Gráfico 5: Votos vs recaudación ──────────────────────────────────────────
section_header("Popularidad", "Votos vs recaudación", "Relación entre número de votos y taquilla",
               color="#c4426e", color_rgba="rgba(210,82,126,0.12)", border_rgba="rgba(210,82,126,0.3)")

fig5 = px.scatter(
    df_f,
    x="vote_count",
    y="revenue",
    labels={"vote_count": "Número de votos", "revenue": "Recaudación (USD)"},
    opacity=0.5,
    color_discrete_sequence=[GREEN],
    title=" ",
)
fig5.update_layout(**PLOT_LAYOUT)
fig5.update_traces(marker_size=6)
st.plotly_chart(fig5, use_container_width=True)


# ── Gráfico 6: Duración vs puntuación ────────────────────────────────────────
section_header("Calidad", "Duración vs puntuación", "Relación entre duración de la película y su puntuación media",
               color="#c47d10", color_rgba="rgba(186,117,23,0.12)", border_rgba="rgba(186,117,23,0.3)")

fig6 = px.scatter(
    df_f,
    x="runtime",
    y="vote_average",
    labels={"runtime": "Duración (minutos)", "vote_average": "Puntuación media"},
    opacity=0.6,
    color_discrete_sequence=["#c47d10"],
    title=" ",
)
fig6.update_layout(**PLOT_LAYOUT)
fig6.update_traces(marker_size=6)
st.plotly_chart(fig6, use_container_width=True)


# ── Conclusiones ──────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="background:{CARD_BG};border:1px solid {BORDER};border-left:4px solid {GREEN};border-radius:10px;padding:28px 32px;margin-top:32px;box-sizing:border-box;">
  <p style="font-family:'Space Mono',monospace;font-size:10px;color:{GREEN};letter-spacing:0.12em;text-transform:uppercase;margin:0 0 16px;">Conclusiones</p>
  <p style="font-size:15px;color:{TEXT_MID};margin:0 0 10px;line-height:1.7;">→ &nbsp;Los documentales y películas musicales son los géneros con mayor ROI mediano, lo que indica que suelen ser los más rentables en relación con su presupuesto.</p>
  <p style="font-size:15px;color:{TEXT_MID};margin:0 0 10px;line-height:1.7;">→ &nbsp;El presupuesto medio de las películas ha aumentado claramente con el paso de las décadas, especialmente a partir de los años 80 y 90.</p>
  <p style="font-size:15px;color:{TEXT_MID};margin:0 0 10px;line-height:1.7;">→ &nbsp;James Cameron destaca como el director con mayor éxito en términos de recaudación media por película.</p>
  <p style="font-size:15px;color:{TEXT_MID};margin:0 0 10px;line-height:1.7;">→ &nbsp;Las películas estrenadas en junio, mayo y noviembre son las que tienen, de media, una mayor recaudación en taquilla; seguidas de julio y diciembre.</p>
  <p style="font-size:15px;color:{TEXT_MID};margin:0 0 10px;line-height:1.7;">→ &nbsp;Existe una relación positiva entre el número de votos y la recaudación de las películas. En general, las películas con más votos tienden a tener mayores ingresos, aunque la relación no es perfectamente lineal y existen algunas excepciones.</p>
  <p style="font-size:15px;color:{TEXT_MID};margin:0;line-height:1.7;">→ &nbsp;Se observa una ligera tendencia a que las películas más largas tengan mejores puntuaciones. Aun así, la relación no es muy fuerte.</p>
</div>
""", unsafe_allow_html=True)