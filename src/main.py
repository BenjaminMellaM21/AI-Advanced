"""Entrypoint de la aplicación FastAPI."""
from fastapi import FastAPI

from src.api.routes import router

app = FastAPI(
    title="JARVIS-Auto",
    description="Asistente conversacional con auto-aprendizaje y memoria vectorial",
    version="0.1.0",
)

app.include_router(router)


@app.get("/")
def root():
    return {
        "name": "JARVIS-Auto",
        "docs": "/docs",
        "endpoints": ["/chat", "/learn", "/memory/search", "/health"],
    }
