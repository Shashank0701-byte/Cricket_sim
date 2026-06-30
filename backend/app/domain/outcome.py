from dataclasses import dataclass

from app.domain.team import Team


@dataclass(slots=True, frozen=True)
class Outcome:

    winner: Team | None

    by_runs: int | None = None

    by_wickets: int | None = None

    result: str | None = None