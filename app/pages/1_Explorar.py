"""Explorador de planetas y estrellas."""
from __future__ import annotations

import streamlit as st

from lib.db import run_query
from lib.ui import brand_header, inject_theme

st.set_page_config(page_title="Explorar · Exoplanetas NASA", layout="wide")
inject_theme()
brand_header("Busca planetas y estrellas hospedadoras en el catálogo.")

tab_planetas, tab_estrellas = st.tabs(["Planetas", "Estrellas"])

with tab_planetas:
    q = st.text_input("Buscar planeta por nombre", placeholder="Ej. Kepler-186 f")
    c1, c2, c3 = st.columns(3)
    with c1:
        masa_max = st.number_input("Masa máxima (M⊕)", min_value=0.0, value=0.0, help="0 = sin filtro")
    with c2:
        radio_max = st.number_input("Radio máximo (R⊕)", min_value=0.0, value=0.0, help="0 = sin filtro")
    with c3:
        limite = st.slider("Filas a mostrar", 20, 500, 100, 20)

    sql = """
        SELECT
          p.nombre AS Planeta,
          e.nombre AS Estrella,
          p.masa AS `Masa (M⊕)`,
          p.radio AS `Radio (R⊕)`,
          p.periodo_orbital AS `Periodo (días)`,
          p.semieje_mayor AS `Semieje (UA)`
        FROM planeta p
        JOIN estrella e ON e.id_estrella = p.id_estrella
        WHERE (:q = '' OR p.nombre LIKE CONCAT('%', :q, '%'))
          AND (:masa_max = 0 OR (p.masa IS NOT NULL AND p.masa <= :masa_max))
          AND (:radio_max = 0 OR (p.radio IS NOT NULL AND p.radio <= :radio_max))
        ORDER BY p.nombre
        LIMIT :limite
    """
    df = run_query(
        sql,
        {
            "q": q.strip(),
            "masa_max": float(masa_max),
            "radio_max": float(radio_max),
            "limite": int(limite),
        },
    )
    st.caption(f"{len(df)} resultados")
    st.dataframe(df, width="stretch", hide_index=True)

with tab_estrellas:
    qe = st.text_input("Buscar estrella por nombre", placeholder="Ej. TRAPPIST-1")
    limite_e = st.slider("Filas de estrellas", 20, 500, 100, 20, key="lim_e")
    dfe = run_query(
        """
        SELECT
          e.nombre AS Estrella,
          e.masa AS `Masa (M☉)`,
          e.radio AS `Radio (R☉)`,
          e.temperatura AS `Teff (K)`,
          COUNT(p.id_planeta) AS Planetas
        FROM estrella e
        LEFT JOIN planeta p ON p.id_estrella = e.id_estrella
        WHERE (:q = '' OR e.nombre LIKE CONCAT('%', :q, '%'))
        GROUP BY e.id_estrella, e.nombre, e.masa, e.radio, e.temperatura
        ORDER BY Planetas DESC, e.nombre
        LIMIT :limite
        """,
        {"q": qe.strip(), "limite": int(limite_e)},
    )
    st.caption(f"{len(dfe)} resultados")
    st.dataframe(dfe, width="stretch", hide_index=True)
