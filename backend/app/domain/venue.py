from dataclasses import dataclass

@dataclass(slots=True)
class Venue:
    name: str
    city: str | None = None