from dataclasses import dataclass

from app.domain.over import Over
from app.domain.team import Team
from app.domain.powerplay import PowerPlay


@dataclass(slots=True)
class Innings:

    batting_team: Team

    overs: list[Over]

    powerplays: list[PowerPlay]