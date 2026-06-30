from dataclasses import dataclass

from app.domain.team import Team
from app.domain.over import Over

@dataclass(slots=True)
class Innings:

    batting_team: Team

    overs: list[Over]