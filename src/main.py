import json
import multiprocessing
import sys

from behaviors import Behavior, behaviors
from models import *


def player_handler(player: Player, action: Behavior):
    player.client = Client(SERVER_IP, SERVER_PORT)

    try:
        _ = player.initializate_player()
        player.move_to_initial_position()
        while True:
            state = player.client.receive()
            action.perform(player, state)

    except KeyboardInterrupt:
        print(f"🟥 Jugador {player.id} desconectado.")
    except socket.timeout:
        print(f"❌ Jugador {player.id} no recibió respuesta del servidor.")


def read_formation(file: str) -> list[Player]:
    with open(file, "r") as f:
        formation = json.load(f)

    print(f"⚙️  Cargando equipo: {formation['team_name']}")
    players: list[Player] = []
    for player_dict in formation["players"]:
        player_dict["role"] = Role(player_dict["role"])
        player = Player(**player_dict)
        player.team = formation["team_name"]
        player.playing = False
        players.append(player)
    print("✅ Todos los jugadores han sido iniciados.")
    return players


def create_processes(players: list[Player]) -> list[multiprocessing.Process]:
    processes: list[multiprocessing.Process] = [
        multiprocessing.Process(
            target=player_handler, args=(player, behaviors[player.role])
        )
        for player in players
    ]

    return processes


def start_processes(processes: list[multiprocessing.Process]):
    try:
        for process in processes:
            process.start()
            time.sleep(0.3)
        for process in processes:
            process.join()
    except KeyboardInterrupt:
        for process in processes:
            process.terminate()
        print("🟥 Finalizando equipo...")


def main():
    if len(sys.argv) < 2:
        print("Uso: python src/main.py <archivo_de_formacion.json>")
        sys.exit(1)

    formation_file: str = sys.argv[1]
    players = read_formation(formation_file)
    processes = create_processes(players)
    start_processes(processes)


if __name__ == "__main__":
    main()
