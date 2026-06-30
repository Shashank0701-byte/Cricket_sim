import json
from pathlib import Path

class MatchParser:

    def load(self, file: Path):

        with open(file, encoding="utf-8") as f:
            return json.load(f)