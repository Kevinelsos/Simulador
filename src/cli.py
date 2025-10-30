import argparse
from config import (DEFAULT_PLAYER_CREATION_DELAY, DEFAULT_SERVER_IP,
                    DEFAULT_SERVER_PORT)


def parse_args():
    """Parse CLI arguments for simulator client configuration."""

    parser = argparse.ArgumentParser(
        description="Simulador de equipo de fútbol: conecta jugadores al servidor."
    )

    parser.add_argument(
        "formation_file",
        type=str,
        help="Ruta al archivo JSON con la formación del equipo (e.g. formacion.json)",
    )

    parser.add_argument(
        "--server-ip",
        type=str,
        default=DEFAULT_SERVER_IP,
        help="Dirección IP del servidor (por defecto: 127.0.0.1)",
    )

    parser.add_argument(
        "--server-port",
        type=int,
        default=DEFAULT_SERVER_PORT,
        help="Puerto del servidor (por defecto: 6000)",
    )

    parser.add_argument(
        "--player-creation-delay",
        type=float,
        default=DEFAULT_PLAYER_CREATION_DELAY,
        help="Tiempo de espera entre creación de jugadores (segundos, por defecto: 0.3)",
    )

    return parser.parse_args()
