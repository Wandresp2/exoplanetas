FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY app/ .

EXPOSE 8501

CMD ["streamlit", "run", "Inicio.py", "--server.address=0.0.0.0", "--server.port=8501", "--browser.gatherUsageStats=false"]
