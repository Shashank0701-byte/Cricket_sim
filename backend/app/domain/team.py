from dataclasses import dataclass

@dataclass(slots=True)
class Team:
    name: str