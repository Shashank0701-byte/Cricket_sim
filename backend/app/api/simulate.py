from fastapi import APIRouter
from pydantic import BaseModel
from app.ml.simulator import MatchSimulator

router = APIRouter()
# Initialize once at startup
simulator = MatchSimulator()

class SimulationRequest(BaseModel):
    batter_id: str
    bowler_id: str
    innings_number: int = 1
    over_number: int
    delivery_number: int
    innings_runs: int
    innings_wickets: int

@router.post("/ball")
def simulate_ball(req: SimulationRequest):
    outcome = simulator.simulate_ball(
        req.batter_id,
        req.bowler_id,
        req.innings_number,
        req.over_number,
        req.delivery_number,
        req.innings_runs,
        req.innings_wickets
    )
    return {"outcome": outcome}
