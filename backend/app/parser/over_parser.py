from app.domain.over import Over
from app.parser.delivery_parser import DeliveryParser


class OverParser:

    def __init__(self):
        self.delivery_parser = DeliveryParser()

    def parse(self, over_data, registry):

        deliveries = []

        for delivery in over_data["deliveries"]:
            deliveries.append(
                self.delivery_parser.parse(
                    delivery,
                    registry
                )
            )

        return Over(
            number=over_data["over"],
            deliveries=deliveries
        )