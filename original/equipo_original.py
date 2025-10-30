import socket
import time
import json
import multiprocessing

SERVER_IP = "127.0.0.1"
SERVER_PORT = 6000
TEAM_NAME = "Nacional"

# --- Lógica individual de cada jugador ---
def iniciar_jugador(jugador):
    player_id = jugador["id"]
    x, y = jugador["x"], jugador["y"]
    rol = jugador["role"]

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(2.0)

    # --- Enviar mensaje de conexión ---
    init_msg = f"(init {TEAM_NAME} (version 19))"
    sock.sendto(init_msg.encode(), (SERVER_IP, SERVER_PORT))
    print(f"⚽ Jugador {player_id} ({rol}) enviado: {init_msg}")

    try:
        data, addr = sock.recvfrom(8192)
        msg = data.decode(errors="ignore").strip()
        print(f"✅ Jugador {player_id} conectado -> {msg}")
        server_port = addr[1]
    except socket.timeout:
        print(f"❌ Jugador {player_id} no recibió respuesta del servidor.")
        return

    # --- Mover jugador a su posición inicial ---
    move_cmd = f"(move {x} {y})"
    sock.sendto(move_cmd.encode(), (SERVER_IP, server_port))
    print(f"🚀 Jugador {player_id} movido a posición ({x}, {y})")

    # --- Comportamiento según el rol ---
    try:
        while True:
            try:
                data, _ = sock.recvfrom(8192)
                msg = data.decode(errors="ignore").strip()

                # PORTERO: se queda quieto
                if rol == "GK":
                    continue

                # DEFENSA: no se mueve, pero podría mirar el balón
                if rol == "DF":
                    continue

                # DELANTERO: si comienza el juego, se mueve o patea
                if "referee play_on" in msg:
                    sock.sendto(b"(dash 80)", (SERVER_IP, server_port))
                    time.sleep(0.2)

                # Si está el balón listo para saque, patea
                if "referee kick_off_l" in msg and rol == "FW":
                    sock.sendto(b"(kick 100 0)", (SERVER_IP, server_port))
                    print(f"💥 Jugador {player_id} patea el balón")

            except socket.timeout:
                continue
    except KeyboardInterrupt:
        print(f"🟥 Jugador {player_id} desconectado.")


# --- PROGRAMA PRINCIPAL ---
if __name__ == "__main__":
    with open("formacion.json", "r") as f:
        formacion = json.load(f)

    print(f"⚙️  Cargando equipo: {formacion['team_name']}")
    jugadores = formacion["players"]

    procesos = []

    # --- Lanzar jugadores en procesos paralelos ---
    for jugador in jugadores:
        print(f"🚀 Iniciando jugador {jugador['id']} ({jugador['role']}) en X={jugador['x']} Y={jugador['y']}")
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

