from fastapi import FastAPI

app = FastAPI(
    title="CricketSim API",
    version="0.1"
)

@app.get("/")
def home():
    return {
        "status": "running"
    }