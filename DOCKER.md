# Docker Deployment Guide

This guide shows how to run the Fashionista Price Optimizer using Docker and Docker Compose.

## Prerequisites

- Docker installed ([download](https://www.docker.com/products/docker-desktop))
- Docker Compose installed (included with Docker Desktop)

## Quick Start (Docker Compose — Recommended)

Docker Compose runs both the API and Streamlit together with networking already configured.

### 1. Build and Start Services

```bash
docker-compose up --build
```

This will:
- Build the Docker image from the Dockerfile
- Start the FastAPI service on `http://localhost:8001`
- Start the Streamlit service on `http://localhost:8501`
- Link them via a custom network so they can communicate

### 2. Access the App

- **Streamlit Dashboard:** http://localhost:8501
- **API Docs:** http://localhost:8001/docs (FastAPI Swagger UI)
- **API Root:** http://localhost:8001/

### 3. Stop Services

```bash
docker-compose down
```

To remove images as well:

```bash
docker-compose down --rmi all
```

---

## Running Individual Services

If you prefer to run services separately:

### Start just the API

```bash
docker build -t fashionista-api .
docker run -p 8001:8001 fashionista-api
```

### Start just Streamlit

```bash
docker build -t fashionista-streamlit .
docker run -p 8501:8501 fashionista-streamlit streamlit run app.py --server.port 8501 --server.address 0.0.0.0
```

---

## Dockerfile Explained

- **Base Image:** `python:3.9-slim` — minimal Python 3.9 runtime
- **Dependencies:** Installs from `requirements.txt`
- **Working Directory:** `/app` inside container
- **Exposed Ports:** 8001 (API) and 8501 (Streamlit)
- **Default Command:** Runs FastAPI server (override with `docker run -c` for other commands)

---

## Docker Compose Services

### `api` Service

- Runs FastAPI on `0.0.0.0:8001`
- Auto-reloads on code changes (volume mount)
- Network: `fashionista-network`

### `streamlit` Service

- Runs Streamlit on `0.0.0.0:8501`
- Depends on `api` service (waits for it to start)
- Auto-reloads on code changes (volume mount)
- Network: `fashionista-network`

Both services communicate via the custom bridge network, so the Streamlit app can reach the API at `http://api:8001` internally (though it currently uses `http://127.0.0.1:8001`).

---

## Production Deployment Tips

For production, consider:

1. **Remove volume mounts** (in docker-compose.yml) to avoid exposing local files
2. **Disable auto-reload** (remove `--reload` from uvicorn command)
3. **Set `PYTHONUNBUFFERED=0`** for better logging
4. **Use a reverse proxy** (nginx) in front of Streamlit
5. **Add health checks** to services

Example production-ready docker-compose:

```yaml
api:
  build: .
  ports:
    - "8001:8001"
  command: uvicorn api:app --host 0.0.0.0 --port 8001
  environment:
    - PYTHONUNBUFFERED=0
  healthcheck:
    test: ["CMD", "curl", "-f", "http://localhost:8001/"]
    interval: 30s
    timeout: 10s
    retries: 3
```

---

## Troubleshooting

- **Port already in use:** Change port mappings in docker-compose.yml (e.g., `9001:8001`)
- **Container exits immediately:** Check logs with `docker logs <container_id>`
- **Streamlit can't reach API:** Ensure both services are on the same network (they are in docker-compose.yml)
- **Permission denied on volume mount:** Use `sudo docker-compose up` or adjust file permissions

---

## Pushing to Docker Hub (Optional)

To share your Docker image:

```bash
# Tag the image
docker tag fashionista-api YOUR_DOCKERHUB_USERNAME/fashionista-api:latest

# Push to Docker Hub
docker push YOUR_DOCKERHUB_USERNAME/fashionista-api:latest
```

Others can then pull and run:

```bash
docker run -p 8001:8001 YOUR_DOCKERHUB_USERNAME/fashionista-api:latest
```

---

For more Docker info, see the [official Docker docs](https://docs.docker.com/).
