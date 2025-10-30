import json
import multiprocessing
import socket
import time
from dataclasses import dataclass
from typing import Callable

SERVER_IP = "127.0.0.1"
SERVER_PORT = 6000
BUFFER_SIZE = 8192
SOCKET_TIMEOUT = 2.0

BehaviorFn = Callable[[Player, str], None]



@dataclass
class Client:
    host: str
    port: int
    sock: socket.socket
    server_port: int

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.server_port = port  # Puerto inicial de conexión
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(SOCKET_TIMEOUT)

    def send(self, data: str):
        self.sock.sendto(data.encode(), (self.host, self.server_port))

    def receive(self, buffer_size: int = BUFFER_SIZE) -> str:
        try:
            msg, addr = self.sock.recvfrom(buffer_size)
            # Captura dinámicamente el puerto del servidor
            self.server_port = addr[1]
            return msg.decode(errors="ignore").strip()
        except socket.timeout:
            return ""

@dataclass
class Player:
    id: str
    name: str
    x: int
    y: int
    role: str
    team: str | None = None
    playing: bool = False
    client: Client | None = None

    def initializate_player(self):
        if not self.client:
            raise RuntimeError("Client not initialized")

        is_goalie = " (goalie)" if self.role == "GK" else ""
        init_msg = f"(init {self.team} (version 19){is_goalie})"
        self.client.send(init_msg)

        # Esperar respuesta del servidor
        try:
            reply = self.client.receive()
            print(f"🔗 Servidor respondió a {self.name}: {reply}")
            return reply
        except socket.timeout:
            print(f"⚠️ {self.name} no recibió respuesta de init.")
            return None

    def dash(self, force: int):
        if not self.client:
            raise RuntimeError("Client not initialized")
        dash_command = f"(dash {force})"
        self.client.send(dash_command)
        time.sleep(0.2)

    def kick(self, force: int, direction: int):
        if not self.client:
            raise RuntimeError("Client not initialized")
        dash_command = f"(kick {force} {direction})"
        self.client.send(dash_command)
        time.sleep(0.2)

    def move_to_initial_position(self):
        if not self.client:
            raise RuntimeError("Client not initialized")
        move_command = f"(move {self.x} {self.y})"
        self.client.send(move_command)
        print(f"Moviendo a {self.name} a ({self.x}, {self.y})")


# --- Lógica individual de cada jugador ---
def player_handler(player: Player, behavior: BehaviorFn):
    player.client = Client(SERVER_IP, SERVER_PORT)

    try:
        player.initializate_player()
        print(f"✅ Jugador {player.id} conectado al servidor")
    except socket.timeout:
        print(f"❌ Jugador {player.id} no recibió respuesta del servidor.")
        return

    # --- Mover jugador a su posición inicial ---
    player.move_to_initial_position()

    # --- Comportamiento según el rol ---
    try:
        while True:
            try:
                msg = player.client.receive()

                # PORTERO: se queda quieto
                if player.role == "GK":
                    continue

                # DEFENSA: no se mueve, pero podría mirar el balón
                if player.role == "DF":
                    continue

                # DELANTERO: si comienza el juego, se mueve o patea
                if "referee play_on" in msg:
                    player.playing = True

                # Si está el balón listo para saque, patea
                if "referee kick_off_l" in msg and player.role == "FW":
                    player.kick(100, 0)
                    print(f"💥 Jugador {player.id} patea el balón")

                if player.playing:
                    player.dash(80)

            except socket.timeout:
                continue

    except KeyboardInterrupt:
        print(f"🟥 Jugador {player.id} desconectado.")


# --- PROGRAMA PRINCIPAL ---
if __name__ == "__main__":
    with open("formacion.json", "r") as f:
        formation = json.load(f)

    print(f"⚙️  Cargando equipo: {formation['team_name']}")

    players = [Player(**player) for player in formation["players"]]

    processes: list[multiprocessing.Process] = []

    # --- Lanzar jugadores en procesos paralelos ---
    for player in players:
        player.team = formation["team_name"]
        player.playing = False
        print(
            f"🚀 Iniciando jugador {player.id} ({player.role}) en X={player.x} Y={player.y}"
        )
        process = multiprocessing.Process(target=player_handler, args=(player,))
        process.start()
        processes.append(process)
        time.sleep(0.3)  # pequeño delay para no saturar el servidor

    print("✅ Todos los jugadores han sido iniciados.")

    # --- Mantener equipo activo ---
    try:
        for process in processes:
            process.join()
    except KeyboardInterrupt:
        print("🟥 Finalizando equipo...")
        for process in processes:
            process.terminate()
