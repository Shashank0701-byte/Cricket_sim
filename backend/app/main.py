from fastapi import FastAPI
from app.api.api_router import api_router

app = FastAPI(
    title="PowerPlay API",
    version="0.1.0"
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def root():
    return {
        "message": "PowerPlay Backend Running 🚀"
    }