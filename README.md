# AI-Powered Expense Tracker

An intelligent expense tracking application that helps individuals
and organizations record, manage, analyze, and understand financial
activities.

## Project Goals

- Manual income and expense tracking.
- Transaction categorization.
- Financial dashboards and analytics.
- Receipt uploads and OCR.
- AI-assisted transaction extraction.
- AI-powered financial insights.
- Multi-currency support.

## Architecture

- Frontend: Flutter
- Backend: Python / FastAPI
- Database: PostgreSQL
- ORM: SQLAlchemy
- Migrations: Alembic
- AI/OCR: To be integrated

## Repository Structure

- backend/ - FastAPI application
- frontend/ - Flutter application
- docs/ - Architecture and technical documentation
- scripts/ - Development and maintenance scripts

## Development

### Backend

```bash
cd backend
py -m venv .venv
```

Activate the virtual environment, install dependencies:

```bash
pip install -r requirements.txt
```

Configure your .env file.

Apply migrations:

```bash
alembic upgrade head
```

Run:

```bash
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
flutter pub get
flutter run -d chrome
```

### API Documentation

When the backend is running:

http://localhost:8000/docs

### Database Migrations

Create a migration:
```bash
alembic revision --autogenerate -m "describe change"
```

Apply migrations:
```bash
alembic upgrade head
```