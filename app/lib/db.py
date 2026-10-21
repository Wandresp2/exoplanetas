"""Conexión a MySQL vía SQLAlchemy (host = nombre del servicio Compose)."""
from __future__ import annotations

import os

import pandas as pd
import streamlit as st
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError


def _env(key: str, default: str) -> str:
    return os.getenv(key, default)


def get_engine() -> Engine:
    host = _env("DB_HOST", "mysql")
    port = _env("DB_PORT", "3306")
    user = _env("DB_USER", "root")
    password = _env("DB_PASSWORD", "root")
    database = _env("DB_NAME", "astronomia")
    url = (
        f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
        "?charset=utf8mb4"
    )
    return create_engine(url, pool_pre_ping=True, pool_recycle=3600)


@st.cache_resource(show_spinner=False)
def engine() -> Engine:
    return get_engine()


def run_query(sql: str, params: dict | None = None) -> pd.DataFrame:
    try:
        with engine().connect() as conn:
            return pd.read_sql(text(sql), conn, params=params or {})
    except SQLAlchemyError as exc:
        st.error(
            "No se pudo conectar o consultar MySQL. "
            "Verifica que el servicio `mysql` esté healthy y las variables DB_*."
        )
        st.caption(str(exc))
        st.stop()
