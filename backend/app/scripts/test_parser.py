from pathlib import Path

from app.parser.match_parser import MatchParser

parser = MatchParser()

match = parser.load(
    Path("data/raw/ipl/1082591.json")
)

print(match["info"]["venue"])