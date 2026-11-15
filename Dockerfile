FROM python:3.14.0-slim@sha256:0aecac02dc3d4c5dbb024b753af084cafe41f5416e02193f1ce345d671ec966e
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt
COPY pyproject.toml README.md ./
COPY src/ ./src/
RUN python -m pip install --no-cache-dir setuptools==80.9.0 && python -m pip install --no-cache-dir --no-deps --no-build-isolation .
COPY config/ ./config/
COPY tests/ ./tests/
COPY scripts/ ./scripts/
RUN useradd --create-home --uid 10001 analyst && mkdir -p /app/data/processed /app/data/logs && chown -R analyst:analyst /app
USER analyst
EXPOSE 8000
HEALTHCHECK --interval=10s --timeout=3s --start-period=60s --retries=3 CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=2)"
CMD ["python", "-m", "uvicorn", "sec_analyst.api:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
