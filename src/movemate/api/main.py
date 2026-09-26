from contextlib import asynccontextmanager

from fastapi import FastAPI

from movemate.api.routes.plan import router as plan_router
from movemate.infrastructure.database import create_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield


app = FastAPI(
    title="MoveMate Denmark",
    description=(
        "Agentic AI assistant for international residents "
        "settling in Denmark."
    ),
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(plan_router)
