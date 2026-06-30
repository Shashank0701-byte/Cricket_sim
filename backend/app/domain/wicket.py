from dataclasses import dataclass
from app.domain.player import Player


@dataclass(slots=True)
class Wicket:
    player_out: Player
    kind: str