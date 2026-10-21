"""Visualizaciones Plotly del catálogo."""
from __future__ import annotations

import plotly.express as px
import streamlit as st

from lib.db import run_query
from lib.ui import brand_header, inject_theme

st.set_page_config(page_title="Gráficos · Exoplanetas NASA", layout="wide")
inject_theme()
brand_header("Visualizaciones interactivas del catálogo de exoplanetas.")

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(8, 20, 34, 0.55)",
    font=dict(color="#e8eef7", family="IBM Plex Sans"),
    margin=dict(l=40, r=20, t=50, b=40),
)

# --- Descubrimientos por año ---
by_year = run_query(
    """
    SELECT `year` AS anio, COUNT(*) AS cantidad
    FROM descubrimiento
    WHERE `year` IS NOT NULL
    GROUP BY `year`
    ORDER BY `year`
    """
)
fig_year = px.area(
    by_year,
    x="anio",
    y="cantidad",
    title="Descubrimientos por año",
    labels={"anio": "Año", "cantidad": "Cantidad"},
)
fig_year.update_traces(line_color="#22d3ee", fillcolor="rgba(34, 211, 238, 0.25)")
fig_year.update_layout(**PLOTLY_LAYOUT)
st.plotly_chart(fig_year, width="stretch")

col1, col2 = st.columns(2)

with col1:
    by_method = run_query(
        """
        SELECT metodo, COUNT(*) AS cantidad
        FROM descubrimiento
        WHERE metodo IS NOT NULL
        GROUP BY metodo
        ORDER BY cantidad DESC
        LIMIT 10
        """
    )
    fig_m = px.bar(
        by_method,
        x="cantidad",
        y="metodo",
        orientation="h",
        title="Top métodos de descubrimiento",
        labels={"metodo": "Método", "cantidad": "Cantidad"},
        color="cantidad",
        color_continuous_scale=["#0e7490", "#22d3ee"],
    )
    fig_m.update_layout(**PLOTLY_LAYOUT, coloraxis_showscale=False, yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig_m, width="stretch")

with col2:
    scatter = run_query(
        """
        SELECT
          p.masa AS masa,
          p.radio AS radio,
          d.metodo AS metodo,
          p.nombre AS planeta
        FROM planeta p
        LEFT JOIN descubrimiento d ON d.id_planeta = p.id_planeta
        WHERE p.masa IS NOT NULL AND p.radio IS NOT NULL
          AND p.masa < 500 AND p.radio < 30
        LIMIT 3000
        """
    )
    fig_s = px.scatter(
        scatter,
        x="masa",
        y="radio",
        color="metodo",
        hover_name="planeta",
        title="Masa vs radio (planetas)",
        labels={"masa": "Masa (M⊕)", "radio": "Radio (R⊕)", "metodo": "Método"},
        opacity=0.75,
    )
    fig_s.update_layout(**PLOTLY_LAYOUT, legend_title_text="")
    st.plotly_chart(fig_s, width="stretch")

temp = run_query(
    """
    SELECT temperatura
    FROM estrella
    WHERE temperatura IS NOT NULL AND temperatura BETWEEN 2000 AND 10000
    """
)
fig_t = px.histogram(
    temp,
    x="temperatura",
    nbins=40,
    title="Distribución de temperatura efectiva de estrellas (K)",
    labels={"temperatura": "Teff (K)"},
)
fig_t.update_traces(marker_color="#38bdf8")
fig_t.update_layout(**PLOTLY_LAYOUT)
st.plotly_chart(fig_t, width="stretch")
