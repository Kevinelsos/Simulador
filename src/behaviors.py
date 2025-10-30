from models import *

def goal_keeper(player: Player, state: str):
    pass

def defense(player: Player, state: str):
    pass

def attack(player: Player, state: str):
    if "referee play_on" in state:
        player.playing = True

    if "referee kick_off_l" in state and player.role == "FW":
        player.kick(100, 0)
        print(f"💥 Jugador {player.id} patea el balón")

    if player.playing:
        player.dash(80)

def middle(player: Player, state: str):
    if "referee play_on" in state:
        player.playing = True

    if player.playing:
        player.dash(80)


behaviors: dict[str, BehaviorFn] = {
    "GK": goal_keeper,
    "DF": defense,
    "MF": middle,
    "FW": middle,
}
