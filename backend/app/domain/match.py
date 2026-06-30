from dataclasses import dataclass

from app.domain.team import Team
from app.domain.venue import Venue
from app.domain.innings import Innings

@dataclass(slots=True)
class Match:

    season: str

    venue: Venue

    teams: list[Team]

    innings: list[Innings]