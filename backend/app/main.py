from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.core.config import settings
from app.db.session import engine

from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
from app.api.v1.transactions import router as transactions_router


app = FastAPI(
    title=settings.APP_NAME,
    description="An AI-powered expense tracking API.",
    version="0.2.0",
    debug=settings.DEBUG,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:8000",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)


app.include_router(
    auth_router,
    prefix=settings.API_V1_PREFIX,
)

app.include_router(
    users_router,
    prefix=settings.API_V1_PREFIX,
)

app.include_router(
    transactions_router,
    prefix=settings.API_V1_PREFIX,
)


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Welcome to the Spndtrk API",
        "version": "0.2.0",
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