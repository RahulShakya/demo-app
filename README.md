# Hybrid Multi-Tenant Django SaaS Backend

Production-ready Django backend for hybrid tenant isolation:

- **Shared DB mode** with row-level tenant isolation via `tenant_id`.
- **Dedicated schema mode** via `django-tenants` per enterprise tenant.
- **Dedicated DB mode** support via custom DB router for future expansion.

## Stack

- Python 3.11+
- Django + DRF
- PostgreSQL
- django-tenants
- JWT (simplejwt)
- Redis cache + broker
- Celery workers
- drf-spectacular OpenAPI 3
- Gunicorn
- Nginx reverse proxy
- Docker and docker-compose
- Kubernetes manifests
- Helm chart
- Prometheus metrics endpoint
- Structured JSON logging

## Quick Start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH=$PWD/src
cp .env.example .env
python manage.py makemigrations
python manage.py migrate_schemas --shared
python manage.py migrate_schemas
python manage.py createsuperuser
python manage.py runserver
```

## Docker

```bash
docker compose up --build
```

## API Endpoints

- `POST /api/auth/token/`
- `POST /api/auth/token/refresh/`
- `GET /api/auth/me/`
- `POST /api/tenancy/tenants/` (admin)
- `POST /api/tenancy/tenants/<tenant_uuid>/switch-isolation/` (admin)
- `CRUD /api/projects/`
- `GET /api/schema/`
- `GET /api/docs/`
- `GET /metrics`

## Hybrid Isolation Behavior

1. **Shared mode** (`isolation_mode=shared`) uses `X-Tenant-ID` request header and row filter on tenant FK.
2. **Schema mode** (`isolation_mode=schema`) uses tenant domain routing through `django-tenants`.
3. **Dedicated DB mode** (`isolation_mode=dedicated_db`) routes reads/writes through `TenantDatabaseRouter` to `dedicated` alias.

## Kubernetes

Apply manifests:

```bash
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/
```

## Helm

```bash
helm upgrade --install hybrid-saas ./helm/hybrid-saas
```
