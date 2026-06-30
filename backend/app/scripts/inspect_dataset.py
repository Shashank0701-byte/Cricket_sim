from pathlib import Path
import json
from pprint import pprint

DATASET = Path("data/raw/ipl")

sample = list(DATASET.glob("*.json"))[0]

with open(sample, encoding="utf-8") as f:
    match = json.load(f)

delivery = match["innings"][0]["overs"][0]["deliveries"][0]

print("=" * 60)
print("FIRST DELIVERY")
print("=" * 60)

pprint(delivery)