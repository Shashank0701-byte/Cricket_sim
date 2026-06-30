from app.domain.innings import Innings
from app.domain.team import Team
from app.domain.powerplay import PowerPlay
from app.parser.over_parser import OverParser


class InningsParser:

    def __init__(self):
        self.over_parser = OverParser()

    def parse(self, innings_data, registry):

        overs = []

        for over in innings_data["overs"]:
            overs.append(
                self.over_parser.parse(
                    over,
                    registry
                )
            )

        powerplays = []

        for pp in innings_data.get("powerplays", []):

            powerplays.append(
                PowerPlay(
                    start=str(pp["from"]),
                    end=str(pp["to"]),
                    type=pp["type"]
                )
            )

        return Innings(

            batting_team=Team(
                innings_data["team"]
            ),

            overs=overs,

            powerplays=powerplays
        )