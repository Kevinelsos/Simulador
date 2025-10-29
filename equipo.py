import json
import multiprocessing
import socket
import time
from dataclasses import dataclass
from typing import Optional

SERVER_IP = "127.0.0.1"
SERVER_PORT = 6000
TEAM_NAME = "Nacional"
BUFFER_SIZE = 8192
SOCKET_TIMEOUT = 2.0


@dataclass
class Client:
    host: str
    port: int
    sock: socket.socket

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(SOCKET_TIMEOUT)
        self.server_port = port

    def send(self, data: str):
        self.sock.sendto(data.encode(), (self.host, self.server_port))

    def receive(self, buffer_size: int = BUFFER_SIZE) -> str:
        try:
            msg, addr = self.sock.recvfrom(buffer_size)
            # Guardar el puerto del servidor (nuevo)
            self.server_port = addr[1]
            return msg.decode(errors="ignore").strip()
        except socket.timeout:
            return ""


@dataclass
class Client:
    host: str
    port: int
    sock: socket.socket

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(SOCKET_TIMEOUT)

    def send(self, data: str):
        _ = self.sock.sendto(data.encode(), (self.host, self.port))

    def receive(self, buffer_size: int = BUFFER_SIZE) -> str:
        try:
            msg, _ = self.sock.recvfrom(buffer_size)
            return msg.decode(errors="ignore").strip()
        except socket.timeout:
            return "Timeout"

    def close(self):
        self.sock.close()


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
        init_msg = f"(init {self.team}{is_goalie} (version 19){is_goalie})"
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
        if self.client:
            dash_command = f"(dash {force})"
            self.client.send(dash_command)
            time.sleep(0.2)

    def kick(self, force: int, direction: int):
        if self.client:
            dash_command = f"(kick {force} {direction})"
            self.client.send(dash_command)
            time.sleep(0.2)

    def move_to_initial_position(self):
        if self.client:
            move_command = f"(move {self.x} {self.y})"
            self.client.send(move_command)


# --- Lógica individual de cada jugador ---
def iniciar_jugador(player: Player):
    player.client = Client(SERVER_IP, SERVER_PORT)

    try:
        print(player.initializate_player())
        print(f"✅ Jugador {player.id} conectado al servidor")
    except socket.timeout:
        print(f"❌ Jugador {player.id} no recibió respuesta del servidor.")
        return

    # --- Mover jugador a su posición inicial ---
    player.move_to_initial_position()
    print(f"🚀 Jugador {player.id} movido a posición ({player.x}, {player.y})")

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
        formacion = json.load(f)

    print(f"⚙️  Cargando equipo: {formacion['team_name']}")

    jugadores = [Player(**jugador) for jugador in formacion["players"]]

    procesos = []

    # --- Lanzar jugadores en procesos paralelos ---
    for jugador in jugadores:
        jugador.team = formacion["team_name"]
        jugador.playing = False
        print(
            f"🚀 Iniciando jugador {jugador.id} ({jugador.role}) en X={jugador.x} Y={jugador.y}"
        )
        p = multiprocessing.Process(target=iniciar_jugador, args=(jugador,))
        p.start()
        procesos.append(p)
        time.sleep(0.3)  # pequeño delay para no saturar el servidor

    print("✅ Todos los jugadores han sido iniciados.")

    # --- Mantener equipo activo ---
    try:
        for p in procesos:
            p.join()
    except KeyboardInterrupt:
        print("🟥 Finalizando equipo...")
        for p in procesos:
            p.terminate()
