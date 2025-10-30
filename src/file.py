import json

from models import Client, Player, Role
from behaviors import behaviors


def read_formation(file: str, server_ip: str, server_port: int) -> list[Player]:
    with open(file, "r") as f:
        formation = json.load(f)

    players: list[Player] = []
    for player_dict in formation["players"]:
        player_dict["role"] = Role(player_dict["role"])
        player = Player(**player_dict)
        player.team = formation["team_name"]
        player.playing = False
        player.client = Client(server_ip, server_port)
        player.action = behaviors[player.role]
        players.append(player)
    return players
