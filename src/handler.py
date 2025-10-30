import multiprocessing
import socket
import time

from behaviors import Behavior, behaviors
from models import Client, Player


def player_handler(player: Player):
    try:
        player.initializate_player()
        player.move_to_initial_position()
        while True:
            player.act()

    except KeyboardInterrupt:
        print(f"🟥 Jugador {player.id} desconectado.")
    except socket.timeout:
        print(f"❌ Jugador {player.id} no recibió respuesta del servidor.")


def create_processes(players: list[Player]) -> list[multiprocessing.Process]:
    """Creates a process for each player on the given list, and returns that bunch of processes in a list"""
    processes: list[multiprocessing.Process] = [
        multiprocessing.Process(
            target=player_handler, args=(player,)
        )
        for player in players
    ]

    return processes


def start_processes(processes: list[multiprocessing.Process], delay: float):
    """Starts the given processes within a delay and joins them"""
    try:
        for process in processes:
            process.start()
            time.sleep(delay)
        for process in processes:
            process.join()
    except KeyboardInterrupt:
        for process in processes:
            process.terminate()
        print("🟥 Finalizando equipo...")
