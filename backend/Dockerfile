# backend/Dockerfile
FROM python:3.11-slim

# 1. Install OS dependencies
RUN apt-get update \
 && apt-get install -y --no-install-recommends build-essential curl \
 && rm -rf /var/lib/apt/lists/*

# 2. Set working directory
WORKDIR /app

# 3. Copy & install Python dependencies so uvicorn lands in /usr/local/bin
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Create non-root user and switch
RUN adduser --disabled-password --gecos '' appuser
USER appuser

# 5. Copy your backend package into /app/backend
COPY backend/ /app/backend/

# 6. Expose port and launch Uvicorn pointing at backend.api:app
EXPOSE 8000
CMD ["uvicorn", "backend.api:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
