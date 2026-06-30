from app.domain.delivery import Delivery
from app.parser.player_parser import PlayerParser


class DeliveryParser:

    def __init__(self):

        self.player_parser = PlayerParser()

    def parse(self, delivery, registry):

        return Delivery(

            ball=delivery["actual_delivery"],

            batter=self.player_parser.parse(
                delivery["batter"],
                registry
            ),

            bowler=self.player_parser.parse(
                delivery["bowler"],
                registry
            ),

            non_striker=self.player_parser.parse(
                delivery["non_striker"],
                registry
            ),

            batter_runs=delivery["runs"]["batter"],

            extras=delivery["runs"]["extras"],

            total_runs=delivery["runs"]["total"]
        )