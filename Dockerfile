# BLADE: The House of Severance
# Containerized Terminal Psychological Horror Game Server

FROM python:3.12-slim

# Create dedicated non-root user for security
RUN useradd -m -u 1000 -s /bin/bash blade

WORKDIR /app

# Python environment configuration
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    TELNET_PORT=2323

# Copy application files
COPY blade/ /app/blade/
COPY main.py /app/main.py
COPY requirements.txt /app/requirements.txt
COPY README.md /app/README.md

# Set ownership
RUN chown -R blade:blade /app

USER blade

EXPOSE 2323

# Built-in health check to verify telnet socket is accepting connections
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import socket; s = socket.socket(); s.connect(('127.0.0.1', 2323)); s.close()" || exit 1

ENTRYPOINT ["python", "main.py", "--host", "0.0.0.0", "--port", "2323"]
