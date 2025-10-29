import socket
import time

SERVER_IP = "127.0.0.1"
SERVER_PORT = 6000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(2.0)

sock.sendto(b"(init debug_team (version 19))", (SERVER_IP, SERVER_PORT))
print(">> init enviado")


data, addr = sock.recvfrom(8192)
msg = data.decode(errors="ignore").strip()
print(f"<< desde {addr} -> {msg}")

# Puerto real de comunicación con el servidor
server_port = addr[1]
print(f"Puerto real del servidor: {server_port}")

estado = "antes_del_kickoff"
send_move = "(move -0.38 0)"
sock.sendto(send_move.encode(), (SERVER_IP, server_port))
print(f">> {send_move}")
print(" Esperando inicio del partido...")

while True:
    try:
        data, _ = sock.recvfrom(8192)
        msg = data.decode(errors="ignore").strip()
        #print(msg)
        # Detectar kickoff (mensaje del árbitro)
        if "referee kick_off_l" in msg and estado == "antes_del_kickoff":
            estado = "kickoff"
            print("Patear")
            time.sleep(0.3)
            pateo = "(kick 100 0)"
            sock.sendto(pateo.encode(), (SERVER_IP, server_port))
            print("Pateó el balón hacia adelante")
            continue

        # Detectar que el juego comenzó
        if "referee play_on" in msg and estado != "jugando":
            estado = "jugando"
            print("¡Comienza el partido!")
            continue

        # Si ya estamos en juego, seguir corriendo
        if estado == "jugando":
            sock.sendto(b"(dash 80)", (SERVER_IP, server_port))
            time.sleep(0.3)
            continue

    except socket.timeout:
        continue
    except KeyboardInterrupt:
        print("Cliente detenido manualmente.")
        break

