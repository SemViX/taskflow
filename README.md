# TaskFlow

TaskFlow is a single-page task manager for organising projects and their tasks.
It is built with Python 3.13, Django 5.2, PostgreSQL, Bootstrap 5, and HTMX.
Users can sign up, manage only their own projects and tasks, assign priorities and
deadlines, and mark tasks as complete without full-page reloads.

## Features

- Email-based registration, login, logout, and session management via
  [django-allauth](https://docs.allauth.org/).
- Create, edit, and delete projects with a custom header colour.
- Create, edit, delete, prioritise, and complete tasks within a project.
- Optional task deadlines; dates in the past are rejected.
- Server-side Django form validation and browser-side HTML validation.
- Per-user data access: a user cannot access another user's projects or tasks.
- HTMX partial updates and Bootstrap alerts without page reloads.
- Responsive Bootstrap grid for mobile and desktop layouts.

## Technology

- Python 3.13 and Django 5.2
- PostgreSQL 16
- Docker and Docker Compose
- Bootstrap 5, HTMX, Alpine.js, and hyperscript
- django-allauth and django-widget-tweaks
- Ruff for linting and import sorting

## Run locally

### Prerequisites

- Docker Desktop with Docker Compose v2
- An available port `8000` for the web app and `5432` for PostgreSQL

### 1. Create environment variables

Create a `.env` file in the project root. Do not commit it.

```env
POSTGRES_DB=taskflow
POSTGRES_USER=taskflow
POSTGRES_PASSWORD=change-me
```

### 2. Build and start the application

```bash
docker compose up --build
```

The container entrypoint applies migrations and collects static files. Open
<http://localhost:8000/accounts/signup/> to create an account. After login, the
application redirects to <http://localhost:8000/projects/>.

To stop the services, press `Ctrl+C`. To remove the containers and database volume:

```bash
docker compose down -v
```

> `docker compose down -v` deletes local PostgreSQL data.

## Quality checks

Run these commands inside the web container after starting the stack:

```bash
docker compose exec web ruff check .
docker compose exec web ruff format --check .
docker compose exec web python manage.py test
```

To automatically apply Ruff fixes where possible:

```bash
docker compose exec web ruff check . --fix
docker compose exec web ruff format .
```

Automated tests cover project and task CRUD workflows, form validation,
authentication requirements, ownership restrictions, priority ordering, and task
completion.

## Architecture

```text
config/       Django project configuration, settings, and root URLs
accounts/     allauth form customisation for Bootstrap-styled authentication
projects/     Project model, form, class-based CRUD views, URLs, and tests
tasks/        Task model, form, class-based CRUD views, URLs, and tests
templates/    Base layout, allauth pages, and HTMX partial templates
static/       Custom CSS assets
```
