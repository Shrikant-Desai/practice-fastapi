# Learning Backend

A modular, robust, and scalable backend system built with **FastAPI**. It includes features such as JWT Authentication, PostgreSQL integrations using **SQLAlchemy** (with asynchronous support), fully-featured Redis caching, background task handling via **Celery**, and more. 

## Features

- **FastAPI Web Server:** High-performance async API using Uvicorn & Gunicorn.
- **Relational Database Management:** Integrated with PostgreSQL using SQLAlchemy. 
- **Database Migrations:** Managed smoothly using Alembic. 
- **Secure Authentication:** Implementation of stateless JWT-based authentication.
- **Background Jobs Processing:** Asynchronous background task execution including SMTP email sending using Celery & Redis.
- **Advanced DB Operations:** PostgreSQL full text-search implementation functionality options.
- **Clean Architecture:** Modular separation of concerns into Routers, Services, Repositories, Schemas, and Models.
- **Dockerized Ready:** Fully portable and straightforward production-ready setups matching the latest infrastructure standards utilizing multi-stage builds.

## Technology Stack

- **Framework:** FastAPI
- **Database:** PostgreSQL
- **ORM:** SQLAlchemy (Async/Sync) & Alembic
- **Caching / Message Broker:** Redis
- **Task Worker:** Celery
- **Runtime Environment:** Python 3.11+
- **Containerization:** Docker & Docker Compose

## Codebase Architecture

The project's logic and modular structure have been specifically segregated for optimal maintainability and clarity:

- `core/`: Core configurations handling logic and setups (Pydantic `BaseSettings`, secrets, constants).
- `models/`: SQLAlchemy database ORM model definitions.
- `schemas/`: Pydantic domain models for Request parsing, Response structures, and validation rules.
- `repositories/`: Database transaction implementations containing specialized query layers.
- `services/`: Business logic implementations wrapping interactions between API rules and database.
- `routers/`: Web application entry points specifying application controllers and path definitions.
- `middleware/`: Specific HTTP filters and hooks modifying/tracking requests globally.
- `tasks/`: Celery asynchronous operational units acting seamlessly in the background.

## Setup Instructions

### Pre-requisites

Ensure you have installed:
- [Docker](https://docs.docker.com/get-docker/) & Docker Compose
- Or locally: Python 3.11+, PostgreSQL instance, and a Redis server.

### 1. Environment Configurations

Make sure to establish an environment file representing secrets within your application layer. Create a `.env` file within the base repository directory. You may structure it to match variables in `core/config.py`:

```env
JWT_SECRET_KEY=your_secret_key
# The required DB & Redis endpoints are handled natively by Docker
# You can customize these optional DB secrets:
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=learning_db
# SMTP Configurations
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=third_party_app_password
```

### 2. Run via Docker (Recommended)

Start the entire application array via Docker compose. This will simultaneously build and instantiate: PostgreSQL Database, Redis Cache, API Web Server, and the Celery Worker Process in one go!

```bash
docker-compose up --build -d
```

Your API endpoints will now be served locally out of `http://localhost:8000`. You can explore the Interactive API Documentation Swagger UI by navigating directly to `http://localhost:8000/docs`.

### 3. Running Locally (Alternative)

If you'd like to develop seamlessly apart from container encapsulation:

1. Install system prerequisites: Virtual environment, PostgreSQL server, Redis caching utility.
2. Initialize and spawn python environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```
3. Install required libraries globally:
   ```bash
   pip install -r requirements.txt
   ```
4. Define your `.env` connection variables routing logic back to local installations:
   ```env
   DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/db_name
   SYNC_DATABASE_URL=postgresql://user:pass@localhost:5432/db_name
   REDIS_URL=redis://localhost:6379/0
   ```
5. Apply database schemas via Alembic:
   ```bash
   alembic upgrade head
   ```
6. Run the uvicorn service seamlessly:
   ```bash
   uvicorn main:app --reload
   ```
7. To run the background tasks, you must open a secondary terminal pane to execute the worker:
   ```bash
   celery -A tasks.celery_app.celery_app worker --loglevel=info
   ```

## Managing Schema changes

When modifying your models, record the alterations via alembic logic:
```bash
alembic revision --autogenerate -m "Add description here"
alembic upgrade head
```

## Useful Commands (Docker Environments)

- **View Active API logs**: `docker logs learning-api -f`
- **View Active Celery logs**: `docker logs learning-worker -f`
- **Apply migration from the API container**: 
  ```bash
  docker exec -it learning-api alembic upgrade head
  ```
- **Stop all containers**: `docker-compose stop`
- **Remove all containers** (stops containers and removes the network, keeps data): `docker-compose down`
- **Remove all containers and wipe data** (removes volumes too): `docker-compose down -v`
- **Stop or start a specific container**: `docker-compose stop api` or `docker-compose start api`
- **Rebuild and restart a specific container** (e.g., if you made changes in `api`):
  ```bash
  docker-compose up -d --build api
  ```
- **Force rebuild all containers**: `docker-compose up --build -d`
