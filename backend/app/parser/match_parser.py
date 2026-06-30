import json
from pathlib import Path

from app.domain.match import Match
from app.domain.team import Team
from app.domain.venue import Venue
from app.domain.toss import Toss
from app.domain.outcome import Outcome

from app.parser.innings_parser import InningsParser


class MatchParser:

    def __init__(self):

        self.innings_parser = InningsParser()

    def parse(self, file: Path):

        with open(file, encoding="utf-8") as f:
            data = json.load(f)

        info = data["info"]

        registry = info["registry"]["people"]

        teams = [
            Team(name)
            for name in info["teams"]
        ]

        innings = [

            self.innings_parser.parse(
                inn,
                registry
            )

            for inn in data["innings"]
        ]

        toss = Toss(

            winner=Team(
                info["toss"]["winner"]
            ),

            decision=info["toss"]["decision"]
        )

        outcome = Outcome(

            winner=Team(
                info["outcome"].get("winner")
            )
            if "winner" in info["outcome"]
            else None,

            by_runs=info["outcome"].get("by", {}).get("runs"),

            by_wickets=info["outcome"].get("by", {}).get("wickets"),

            result=info["outcome"].get("result")
        )

        return Match(

            season=str(info["season"]),

            match_date=info["dates"][0],

            venue=Venue(

                name=info["venue"],

                city=info.get("city")
            ),

            teams=teams,

            toss=toss,

            outcome=outcome,

            innings=innings
        )