from fastapi import FastAPI

from movemate.api.routes.plan import router as plan_router


app = FastAPI(
    title="MoveMate Denmark",
    description=(
        "Agentic AI assistant for international residents "
        "settling in Denmark."
    ),
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(plan_router)