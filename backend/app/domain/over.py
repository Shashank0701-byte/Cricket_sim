from dataclasses import dataclass

from app.domain.delivery import Delivery

@dataclass(slots=True)
class Over:

    number: int

    deliveries: list[Delivery]