from app.domain.player import Player


class PlayerParser:

    def parse(self, name: str, registry: dict) -> Player:

        return Player(

            registry_id=registry.get(name, ""),

            name=name
        )