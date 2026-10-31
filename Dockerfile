FROM python:3.14-slim@sha256:cd89c30eda26ee911a4611b18680086e0ea42e6f5f8cbe653d07fa7958c9cec8 AS builder
WORKDIR /app
COPY requirements.txt .
RUN python -m pip install --no-cache-dir --upgrade pip setuptools
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt
FROM python:3.14-slim@sha256:cd89c30eda26ee911a4611b18680086e0ea42e6f5f8cbe653d07fa7958c9cec8 AS runtime
WORKDIR /app
COPY --from=builder /install /usr/local
COPY src/ ./src/
COPY model.joblib .
RUN useradd --create-home --shell /usr/sbin/nologin appuser
RUN python -m pip uninstall -y pip
USER appuser
EXPOSE 8000
CMD ["python", "-m", "uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=3)"
