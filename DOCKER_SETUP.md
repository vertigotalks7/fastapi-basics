# Docker Setup Guide for FastAPI Application

## Overview

This guide explains how to containerize and run your FastAPI application using Docker. The setup includes:
- **Dockerfile**: Multi-stage build for optimized image size
- **docker-compose.yml**: Orchestrates FastAPI app + PostgreSQL database
- **.dockerignore**: Excludes unnecessary files from Docker context
- **.env.example**: Template for environment variables

---

## Prerequisites

1. **Docker**: [Install Docker Desktop](https://www.docker.com/products/docker-desktop)
2. **Docker Compose**: Usually included with Docker Desktop

Verify installation:
```bash
docker --version
docker-compose --version
```

---

## Quick Start (Recommended)

### 1. Setup Environment Variables

Copy `.env.example` to `.env` and update with your values:

```bash
cp .env.example .env
```

Edit `.env`:
```env
DATABASE_USERNAME=postgres
DATABASE_PASSWORD=your_secure_password
DATABASE_NAME=fastapi_db
SECRET_KEY=your_secure_secret_key_here
ALGO=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

### 2. Build and Run with Docker Compose

**Start all services:**
```bash
docker-compose up -d
```

**View logs:**
```bash
docker-compose logs -f
```

**Stop all services:**
```bash
docker-compose down
```

### 3. Access Your Application

- **API**: http://localhost:8000
- **Interactive API Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

---

## Manual Docker Build & Run

### Build the Image

```bash
docker build -t fastapi-app:latest .
```

### Run PostgreSQL Container

```bash
docker run -d \
  --name fastapi_db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=fastapi_db \
  -p 5432:5432 \
  postgres:16
```

### Run FastAPI Container

```bash
docker run -d \
  --name fastapi_app \
  --link fastapi_db:db \
  -e DATABASE_HOSTNAME=db \
  -e DATABASE_PORT=5432 \
  -e DATABASE_USERNAME=postgres \
  -e DATABASE_PASSWORD=postgres \
  -e DATABASE_NAME=fastapi_db \
  -e SECRET_KEY=your-secret-key \
  -e ALGO=HS256 \
  -e ACCESS_TOKEN_EXPIRE_MINUTES=60 \
  -p 8000:8000 \
  fastapi-app:latest
```

---

## Dockerfile Explanation

### Multi-Stage Build Benefits

```dockerfile
FROM python:3.11-slim as builder    # Stage 1: Build dependencies
FROM python:3.11-slim               # Stage 2: Runtime (smaller)
```

- **Reduces final image size** by ~50% (build tools excluded)
- **Faster deployments** with smaller images
- **Better security** with minimal surface area

### Key Components

| Component | Purpose |
|-----------|---------|
| `python:3.11-slim` | Lightweight Python base image |
| `gcc` (builder only) | Compiles C extensions for packages like `psycopg2` |
| `postgresql-client` (runtime) | Required for database connectivity |
| `HEALTHCHECK` | Monitors container health |
| `PYTHONUNBUFFERED=1` | Real-time log output |
| `EXPOSE 8000` | Documents the service port |

---

## Docker Compose Services

### Database Service (PostgreSQL)

```yaml
db:
  image: postgres:16
  healthcheck: Waits for DB readiness
  volumes: Persists data in `postgres_data`
```

**Health Check**: Ensures DB is ready before app starts

### Application Service

```yaml
app:
  build: .
  depends_on: Waits for DB health check
  volumes: Hot-reload code changes
  command: Runs with --reload for development
```

**Auto-reload**: Changes instantly without restart in development

---

## Common Commands

### View Running Containers

```bash
docker-compose ps
```

### Execute Commands in Container

```bash
# Run migrations
docker-compose exec app alembic upgrade head

# Access database
docker-compose exec db psql -U postgres -d fastapi_db
```

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f app
docker-compose logs -f db
```

### Rebuild Image After Dependency Changes

```bash
docker-compose build --no-cache
docker-compose up -d
```

### Clean Up Everything

```bash
docker-compose down -v  # -v removes volumes (DATABASE DATA!)
```

---

## Production Deployment

### Key Changes for Production

Edit `docker-compose.yml` or use separate `docker-compose.prod.yml`:

```yaml
app:
  # Remove volumes for hot-reload
  # Remove --reload flag
  command: uvicorn app.main:app --host 0.0.0.0 --port 8000
  # Use external secrets, not .env files
  # Add resource limits
  deploy:
    resources:
      limits:
        cpus: '1'
        memory: 512M
```

### Environment Variables

Use **secrets management** (not `.env` files):
- Docker Secrets
- AWS Secrets Manager
- HashiCorp Vault

### Example for Production:

```bash
docker-compose -f docker-compose.prod.yml up -d
```

---

## Troubleshooting

### Container Won't Start

```bash
# Check logs
docker-compose logs app

# Common issues:
# 1. Port 8000 already in use:
docker-compose up -p 9000:8000 app

# 2. Environment variables missing:
# Ensure .env file exists with all required variables
```

### Database Connection Errors

```bash
# Test database connectivity
docker-compose exec app \
  python -c "from app.database import engine; print('Connected!')"

# Check if DB is healthy
docker-compose ps db
```

### Rebuild Everything

```bash
docker-compose down -v
docker-compose up --build -d
```

---

## File Structure

```
fastapi/
├── Dockerfile              # Container image definition
├── .dockerignore          # Excludes files from build context
├── docker-compose.yml     # Multi-container orchestration
├── .env                   # Environment variables (create from .env.example)
├── .env.example          # Template for env vars
├── requirements.txt      # Python dependencies
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   └── ...
└── alembic/              # Database migrations
```

---

## Next Steps

1. ✅ Copy `.env.example` to `.env`
2. ✅ Update `.env` with your values
3. ✅ Run `docker-compose up -d`
4. ✅ Visit http://localhost:8000/docs
5. ✅ Check logs: `docker-compose logs -f`

For production, implement proper secrets management and security best practices.
