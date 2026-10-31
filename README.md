
# AI381 Lab 2 — Churn Prediction MLOps

[![CI](https://github.com/ibrahim3alzoubi3-ux/ai381-lab2/actions/workflows/ci.yml/badge.svg)](https://github.com/ibrahim3alzoubi3-ux/ai381-lab2/actions/workflows/ci.yml)

## Project Overview

This project demonstrates an MLOps workflow for a customer churn prediction model.

It includes:
- Machine learning training with scikit-learn
- A FastAPI prediction service
- Input validation using Pydantic
- Automated testing with pytest
- Code linting with Ruff
- Multi-stage Docker build with a non-root user
- Security scanning using Trivy
- Docker image publishing to GitHub Container Registry (GHCR)

## Project Structure

- `src/train/train.py` — Model training
- `src/app/main.py` — FastAPI application
- `tests/test_api.py` — Automated tests
- `Dockerfile` — Container configuration
- `.github/workflows/ci.yml` — CI testing and linting
- `.github/workflows/docker.yml` — Docker build, security scan and publishing

## Run with Docker

```bash
docker build -t ai381-lab2 .
docker run --rm -p 8000:8000 ai381-lab2
```

Open http://localhost:8000/docs to access the API documentation.

## API Endpoints

### GET /health

Checks whether the API is running.

### POST /predict

Example request:

```json
{
  "tenure_months": 12,
  "monthly_charges": 70,
  "contract": "month-to-month",
  "internet_service": "fiber",
  "support_calls": 3
}
```

Returns a churn probability.

## Run Tests

Install the project and test dependencies:

```bash
python -m pip install -r requirements.txt
python -m pip install pytest httpx ruff
python -m pytest tests/ -v
python -m ruff check src/ tests/
```

## Container Image

GHCR repository:

`ghcr.io/ibrahim3alzoubi3-ux/ai381-lab2`

Image digest:

`sha256:daec118f56f63bebf057c83a8acd66f24756016da0da1e72b15a128ffd1f7634`

## Security

The Docker workflow scans the image using Trivy and checks for HIGH and CRITICAL vulnerabilities with available fixes.

## CI/CD

GitHub Actions runs linting and tests on pushes and pull requests targeting main.

The Docker workflow builds and scans the container image, then publishes it to GHCR on successful pushes to main.
