# ───────────────────────────────────────────────────
# Dockerfile — Microservicio de Gestión de Tareas
# Multi-stage build con imagen base liviana
# ───────────────────────────────────────────────────

# ── Stage 1: Builder ──────────────────────────────
FROM python:3.10-slim AS builder

WORKDIR /build

# Copiar solo requirements primero (cache de capas Docker)
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ── Stage 2: Production ──────────────────────────
FROM python:3.10-slim AS production

# Metadatos de la imagen
LABEL maintainer="Gabriel Ferrufino & Matias Pulgar"
LABEL description="Microservicio de gestión de tareas — DOY0101"
LABEL version="1.0.0"

# Crear usuario no-root por seguridad
RUN groupadd -r appuser && useradd -r -g appuser -d /app -s /sbin/nologin appuser

WORKDIR /app

# Copiar dependencias instaladas desde el builder
COPY --from=builder /install /usr/local

# Copiar código fuente
COPY app.py .
COPY requirements.txt .

# Cambiar al usuario no-root
RUN chown -R appuser:appuser /app
USER appuser

# Variables de entorno
ENV PORT=5000
ENV FLASK_DEBUG=false
ENV APP_VERSION=1.0.0

# Exponer el puerto
EXPOSE 5000

# Health check para Docker y orquestadores
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

# Ejecutar con gunicorn en producción
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "120", "--access-logfile", "-", "app:app"]
