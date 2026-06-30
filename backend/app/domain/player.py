from dataclasses import dataclass

@dataclass(slots=True)
class Player:
    name: str