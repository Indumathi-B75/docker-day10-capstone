# Day 10 Docker Capstone: Flask + PostgreSQL

A containerized Flask application backed by PostgreSQL, built to demonstrate Docker fundamentals, multi-stage builds, container security, networking, health checks, and persistent storage.

## Project Overview

This project combines the Docker concepts covered in Days 6–9 into a multi-container application managed with Docker Compose.

The Flask API records application visits in PostgreSQL and returns the total number of visits as JSON.

## Architecture

```text
Client (Browser / curl)
          |
          | HTTP :5000
          v
   Flask Application
   (Gunicorn + Python)
          |
          | Private Docker Network
          v
      PostgreSQL
          |
          v
    Named Volume
    (Persistent Data)
```

## Technologies Used

- Python 3.12
- Flask
- Gunicorn
- PostgreSQL 16
- Docker Engine
- Docker Compose
- Multi-stage Docker builds
- Git and GitHub
- Docker Scout for vulnerability scanning

## Project Structure

```text
docker-day10-capstone/
├── app.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
├── .env
├── compose.yaml
└── README.md
```

**Important:** The `.env` file contains local database credentials and must not be committed to GitHub.

## Features

### 1. Flask API

The application provides two endpoints:

| Endpoint | Description |
|---|---|
| `GET /` | Records a visit and returns the total visit count |
| `GET /health` | Checks whether the Flask application responds |

Example response from `/`:

```json
{
  "status": "success",
  "message": "Docker Day 10 Capstone Active",
  "total_visits": 1
}
```

The visit count increases with each successful request to `/` and persists when the database volume is retained.

### 2. Multi-Stage Docker Build

The Dockerfile separates dependency installation from the runtime image.

Benefits:

- Keeps build-time artifacts out of the final image.
- Separates dependency installation from application execution.
- Uses a virtual environment copied from the builder stage.

### 3. Container Security

The Flask container is configured to use:

- A non-root user with UID `10001`.
- A read-only root filesystem.
- Temporary writable storage through `tmpfs`.
- Dropped Linux capabilities.
- `no-new-privileges` security configuration.

These controls reduce unnecessary container privileges.

### 4. PostgreSQL and Data Persistence

PostgreSQL runs in a separate container.

- Flask connects to PostgreSQL using `DATABASE_URL`.
- A custom Docker bridge network allows service-to-service communication.
- A named volume stores database data independently of the container lifecycle.
- PostgreSQL health checks verify database readiness.

### 5. Docker Compose

Docker Compose manages both services, their network, the database volume, startup dependencies, health checks, and runtime security settings.

## Prerequisites

Install and verify:

- Docker Engine
- Docker Compose
- Git
- curl

Check the installed versions:

```bash
docker --version
docker compose version
git --version
```

## Configuration

Create a local `.env` file containing:

```dotenv
POSTGRES_DB=capstone_db
POSTGRES_USER=capstone_user
POSTGRES_PASSWORD=REPLACE_WITH_A_UNIQUE_PASSWORD
```

Replace the placeholder with a strong, unique password.

Do not publish real credentials or commit `.env` to version control.

## Run the Application

### Step 1: Navigate to the project

```bash
cd ~/docker-day10-capstone
```

### Step 2: Validate the Compose configuration

```bash
docker compose config -q
```

No error output indicates that the Compose configuration passed validation.

### Step 3: Build and start the services

```bash
docker compose up -d --build
```

### Step 4: Check service status

```bash
docker compose ps
```

Wait for the health checks to complete.

### Step 5: View application logs

```bash
docker compose logs --tail=100
```

Follow live logs with:

```bash
docker compose logs -f
```

## Test the Application

Test the Flask health endpoint:

```bash
curl -i http://localhost:5000/health
```

Test database integration:

```bash
curl http://localhost:5000/
```

Run the second command again to verify that the visit count increases.

## Verify Database Persistence

Stop and remove the containers without deleting the named volume:

```bash
docker compose down
docker compose up -d
```

After the services become healthy, run:

```bash
curl http://localhost:5000/
```

The visit count should continue from its previous value.

**Warning:** Avoid `docker compose down -v` when you want to preserve the database. The `-v` option removes the Compose-managed named volume.

## Verify Container Security

### Check the Flask user

```bash
docker compose exec web id
```

The process should run as UID `10001`, not UID `0`.

### Check the read-only root filesystem

```bash
docker inspect "$(docker compose ps -q web)" \
  --format 'Read-only: {{.HostConfig.ReadonlyRootfs}}'
```

Expected output:

```text
Read-only: true
```

### Check PostgreSQL readiness

```bash
docker compose exec db pg_isready \
  -U capstone_user -d capstone_db
```

## Scan the Image with Docker Scout

Run the vulnerability scan if Docker Scout is available:

```bash
docker scout cves day10-capstone-web:1.0
```

Review the results and investigate reported vulnerabilities. A successful scan does not guarantee that an image is completely secure.

## Stop the Application

```bash
docker compose down
```

This stops and removes the containers and Compose network while retaining the named database volume.

## Troubleshooting

### Flask container exits

```bash
docker compose logs web
```

Check for Python errors, missing dependencies, and database connection failures.

### PostgreSQL is unhealthy

```bash
docker compose logs db
docker compose ps
```

Check database initialization, credentials, and health-check status.

### Connection refused

Verify that the Flask service is running and that port `5000` is available on the host.

```bash
docker compose ps
curl -i http://localhost:5000/health
```

### Configuration errors

```bash
docker compose config -q
```

Inspect `compose.yaml` and `.env` for incorrect syntax, indentation, or missing variables.

## GitHub Deployment

Initialize Git if necessary:

```bash
git init
git add app.py requirements.txt Dockerfile .dockerignore .gitignore compose.yaml README.md
git status
```

Verify that `.env` is not staged.

Commit the project:

```bash
git commit -m "feat: build Flask PostgreSQL Docker capstone"
git branch -M main
```

Connect your GitHub repository:

```bash
git remote set-url origin https://github.com/YOUR_USERNAME/docker-day10-capstone.git
```

If the `origin` remote does not exist, use:

```bash
git remote add origin https://github.com/YOUR_USERNAME/docker-day10-capstone.git
```

Push the project:

```bash
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username.

## Learning Outcomes

After completing this capstone, you should understand how to:

- Build and optimize Docker images using multi-stage builds.
- Run a Flask application and PostgreSQL as separate services.
- Configure service networking and database readiness checks.
- Persist database data using named volumes.
- Apply non-root execution and read-only filesystem restrictions.
- Validate Compose configurations and troubleshoot containers.
- Scan images for known vulnerabilities.
- Document and publish a Docker project using GitHub.

## Limitations and Future Improvements

This project is a learning capstone, not a fully production-ready deployment.

Potential improvements include:

- Automated tests using pytest.
- Database schema migrations.
- Database least-privilege roles.
- Production secrets management.
- CI/CD using GitHub Actions.
- Automated vulnerability scanning during builds.
- Structured logging, metrics, and monitoring.

---

**Project:** Docker Day 10 Capstone

**Stack:** Flask + Gunicorn + PostgreSQL + Docker Compose

**Repository:** `docker-day10-capstone`
