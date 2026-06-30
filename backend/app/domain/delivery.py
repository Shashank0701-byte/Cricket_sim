from dataclasses import dataclass

from app.domain.player import Player
from app.domain.wicket import Wicket


@dataclass(slots=True)
class Delivery:

    ball: str

    batter: Player

    bowler: Player

    non_striker: Player

    batter_runs: int

    extras: int

    total_runs: int

    wicket: Wicket | None = None