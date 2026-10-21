"""Página principal — resumen del catálogo de exoplanetas."""
from __future__ import annotations

import streamlit as st

from lib.db import run_query
from lib.ui import brand_header, inject_theme, kpi_row

st.set_page_config(
    page_title="Exoplanetas NASA",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_theme()
brand_header(
    "Catálogo relacional de exoplanetas confirmados (NASA Exoplanet Archive). "
    "Explora estrellas, planetas, telescopios y descubrimientos."
)

counts = run_query(
    """
    SELECT
      (SELECT COUNT(*) FROM planeta) AS planetas,
      (SELECT COUNT(*) FROM estrella) AS estrellas,
      (SELECT COUNT(*) FROM telescopio) AS telescopios,
      (SELECT COUNT(*) FROM descubrimiento) AS descubrimientos
    """
).iloc[0]

kpi_row(
    [
        ("Planetas", f"{int(counts['planetas']):,}".replace(",", ".")),
        ("Estrellas", f"{int(counts['estrellas']):,}".replace(",", ".")),
        ("Telescopios", f"{int(counts['telescopios']):,}".replace(",", ".")),
        ("Descubrimientos", f"{int(counts['descubrimientos']):,}".replace(",", ".")),
    ]
)

st.markdown("---")

col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Métodos de descubrimiento más frecuentes")
    metodos = run_query(
        """
        SELECT metodo AS Método, COUNT(*) AS Cantidad
        FROM descubrimiento
        WHERE metodo IS NOT NULL
        GROUP BY metodo
        ORDER BY Cantidad DESC
        LIMIT 8
        """
    )
    st.dataframe(metodos, width="stretch", hide_index=True)

with col_b:
    st.subheader("Años con más descubrimientos")
    years = run_query(
        """
        SELECT `year` AS Año, COUNT(*) AS Cantidad
        FROM descubrimiento
        WHERE `year` IS NOT NULL
        GROUP BY `year`
        ORDER BY Cantidad DESC
        LIMIT 8
        """
    )
    st.dataframe(years, width="stretch", hide_index=True)

st.subheader("Muestra del catálogo")
sample = run_query(
    """
    SELECT
      p.nombre AS Planeta,
      e.nombre AS Estrella,
      p.masa AS `Masa (M⊕)`,
      p.radio AS `Radio (R⊕)`,
      p.periodo_orbital AS `Periodo (días)`,
      d.`year` AS Año,
      d.metodo AS Método
    FROM planeta p
    JOIN estrella e ON e.id_estrella = p.id_estrella
    LEFT JOIN descubrimiento d ON d.id_planeta = p.id_planeta
    ORDER BY d.`year` DESC
    LIMIT 15
    """
)
st.dataframe(sample, width="stretch", hide_index=True)

st.caption(
    "Datos: NASA Exoplanet Archive · Tabla pscomppars · Base MySQL `astronomia`"
)
