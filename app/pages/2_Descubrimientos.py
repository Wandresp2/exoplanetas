"""Descubrimientos, métodos y telescopios."""
from __future__ import annotations

import streamlit as st

from lib.db import run_query
from lib.ui import brand_header, inject_theme

st.set_page_config(page_title="Descubrimientos · Exoplanetas NASA", layout="wide")
inject_theme()
brand_header("Métodos, instalaciones y telescopios detrás de cada hallazgo.")

metodos = run_query(
    """
    SELECT DISTINCT metodo
    FROM descubrimiento
    WHERE metodo IS NOT NULL
    ORDER BY metodo
    """
)["metodo"].tolist()

c1, c2, c3 = st.columns(3)
with c1:
    metodo = st.selectbox("Método", ["(todos)"] + metodos)
with c2:
    anio_min = st.number_input("Año desde", min_value=1988, max_value=2030, value=1988)
with c3:
    anio_max = st.number_input("Año hasta", min_value=1988, max_value=2030, value=2030)

df = run_query(
    """
    SELECT
      p.nombre AS Planeta,
      d.`year` AS Año,
      d.metodo AS Método,
      t.nombre AS Telescopio,
      t.instalacion AS Instalación,
      t.instrumento AS Instrumento
    FROM descubrimiento d
    JOIN planeta p ON p.id_planeta = d.id_planeta
    LEFT JOIN telescopio t ON t.id_telescopio = d.id_telescopio
    WHERE (:metodo = '(todos)' OR d.metodo = :metodo)
      AND (d.`year` IS NULL OR (d.`year` BETWEEN :ymin AND :ymax))
    ORDER BY d.`year` DESC, p.nombre
    LIMIT 400
    """,
    {
        "metodo": metodo,
        "ymin": int(anio_min),
        "ymax": int(anio_max),
    },
)
st.caption(f"Mostrando {len(df)} descubrimientos (máx. 400)")
st.dataframe(df, width="stretch", hide_index=True)

st.subheader("Ranking de instalaciones")
rank = run_query(
    """
    SELECT
      COALESCE(t.instalacion, '(sin instalación)') AS Instalación,
      COUNT(*) AS Descubrimientos
    FROM descubrimiento d
    LEFT JOIN telescopio t ON t.id_telescopio = d.id_telescopio
    GROUP BY t.instalacion
    ORDER BY Descubrimientos DESC
    LIMIT 15
    """
)
st.dataframe(rank, width="stretch", hide_index=True)
