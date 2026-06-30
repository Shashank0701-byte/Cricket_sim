from fastapi import APIRouter

router = APIRouter()

@router.get("/players/{player_id}")
def get_player_stats(player_id: str):
    # Will aggregate player stats
    return {"message": f"Stats for player {player_id}"}

@router.get("/teams/{team_id}")
def get_team_stats(team_id: int):
    return {"message": f"Stats for team {team_id}"}
