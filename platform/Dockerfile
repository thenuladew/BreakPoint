FROM python:3.12-slim

# Non-root user
RUN addgroup --system ctf && adduser --system --ingroup ctf ctf

WORKDIR /app

# Install dependencies first (layer cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Database directory (will be mounted as a named volume)
RUN mkdir -p /app/database && chown ctf:ctf /app/database

USER ctf

EXPOSE 5000

# Gunicorn: 2 sync workers is fine for a single-room CTF
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "30", "app:app"]
