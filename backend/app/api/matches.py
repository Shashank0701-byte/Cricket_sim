from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_matches():
    # Will integrate with DB next
    return {"message": "List of matches"}

@router.get("/{match_id}")
def get_match(match_id: int):
    return {"message": f"Match details for {match_id}"}
