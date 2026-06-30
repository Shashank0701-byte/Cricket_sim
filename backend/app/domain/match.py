from dataclasses import dataclass
from datetime import date

from app.domain.innings import Innings
from app.domain.outcome import Outcome
from app.domain.team import Team
from app.domain.toss import Toss
from app.domain.venue import Venue


@dataclass(slots=True)
class Match:

    season: str

    match_date: date

    venue: Venue

    teams: list[Team]

    toss: Toss

    outcome: Outcome

    innings: list[Innings]