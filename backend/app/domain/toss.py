from dataclasses import dataclass

from app.domain.team import Team


@dataclass(slots=True, frozen=True)
class Toss:

    winner: Team

    decision: str