"""Estilos y helpers visuales compartidos — tema espacial (cian / navy)."""
from __future__ import annotations

import streamlit as st

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=IBM+Plex+Sans:wght@400;500;600&display=swap');

html, body, [class*="css"] {
  font-family: 'IBM Plex Sans', sans-serif;
}

.stApp {
  background:
    radial-gradient(1200px 600px at 10% -10%, rgba(34, 211, 238, 0.18), transparent 55%),
    radial-gradient(900px 500px at 90% 0%, rgba(56, 189, 248, 0.12), transparent 50%),
    linear-gradient(180deg, #06101c 0%, #0b1726 45%, #0a1420 100%);
  color: #e8eef7;
}

h1, h2, h3, .brand-title {
  font-family: 'Space Grotesk', sans-serif !important;
  letter-spacing: -0.02em;
}

.brand-wrap {
  padding: 1.25rem 0 0.5rem 0;
  animation: fadeRise 0.7s ease-out both;
}

.brand-title {
  font-size: clamp(2.1rem, 4vw, 3rem);
  font-weight: 700;
  margin: 0;
  background: linear-gradient(90deg, #f8fafc 0%, #67e8f9 55%, #38bdf8 100%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.brand-sub {
  margin: 0.4rem 0 0 0;
  color: #9fb3c8;
  font-size: 1.05rem;
  max-width: 42rem;
}

.kpi {
  background: linear-gradient(145deg, rgba(15, 35, 55, 0.9), rgba(12, 28, 44, 0.75));
  border: 1px solid rgba(103, 232, 249, 0.22);
  border-radius: 14px;
  padding: 1rem 1.1rem;
  animation: fadeRise 0.8s ease-out both;
}

.kpi .label {
  color: #8aa0b8;
  font-size: 0.85rem;
  margin-bottom: 0.25rem;
}

.kpi .value {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 1.8rem;
  font-weight: 700;
  color: #e0f2fe;
}

div[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #071422 0%, #0c1b2e 100%);
  border-right: 1px solid rgba(103, 232, 249, 0.12);
}

@keyframes fadeRise {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

[data-testid="stMetric"] {
  background: rgba(12, 28, 44, 0.65);
  border: 1px solid rgba(103, 232, 249, 0.18);
  border-radius: 12px;
  padding: 0.75rem 1rem;
}
"""


def inject_theme() -> None:
    st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)


def brand_header(subtitle: str) -> None:
    st.markdown(
        f"""
        <div class="brand-wrap">
          <p class="brand-title">Exoplanetas NASA</p>
          <p class="brand-sub">{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def kpi_row(items: list[tuple[str, str]]) -> None:
    cols = st.columns(len(items))
    for col, (label, value) in zip(cols, items):
        with col:
            st.markdown(
                f'<div class="kpi"><div class="label">{label}</div>'
                f'<div class="value">{value}</div></div>',
                unsafe_allow_html=True,
            )
