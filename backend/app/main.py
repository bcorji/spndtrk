from fastapi import FastAPI
from sqlalchemy import text

from app.core.config import settings
from app.db.session import engine


app = FastAPI(
    title=settings.APP_NAME,
    description="An AI-powered expense tracking API.",
    version="0.1.0",
    debug=settings.DEBUG,
)


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Welcome to the Spndtrk API",
        "version": "0.1.0",
    }


@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "healthy",
        "environment": settings.APP_ENV,
    }


@app.get("/health/db", tags=["Health"])
def database_health_check():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {
        "status": "healthy",
        "database": "connected",
    }