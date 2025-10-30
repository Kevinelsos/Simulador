import socket
import time
from dataclasses import dataclass
from typing import Callable

from config import *


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

    def send(self, data: str) -> None:
        _ = self.sock.sendto(data.encode(), (self.host, self.server_port))

    def receive(self, buffer_size: int = BUFFER_SIZE) -> str:
        try:
            msg, addr = self.sock.recvfrom(buffer_size)
            # Captura dinámicamente el puerto del servidor
            self.server_port = addr[1]
            return msg.decode(errors="ignore").strip()
        except socket.timeout:
            return "There Was a Timeout connecting to "


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


BehaviorFn = Callable[[Player, str], None]
