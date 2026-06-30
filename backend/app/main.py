from fastapi import FastAPI

app = FastAPI(
    title="PowerPlay API",
    version="0.1.0"
)

@app.get("/")
def root():
    return {
        "message": "PowerPlay Backend Running 🚀"
    }