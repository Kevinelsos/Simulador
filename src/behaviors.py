from typing import cast, override

from models import Behavior, Entity, Player, Role


class GoalKeeperBehavior(Behavior):
    """Behavior of a GoalKeeper"""

    @override
    def perform(self, entity: Entity, state: str) -> None:
        player = cast(Player, entity)
        if "ball" in state:
            print(f"🧤 {player.name} se prepara para atajar")
        else:
            pass


class DefenseBehavior(Behavior):
    @override
    def perform(self, entity: Entity, state: str) -> None:
        player = cast(Player, entity)
        if "referee play_on" in state:
            player.playing = True
        if player.playing:
            player.dash(50)


class MiddleBehavior(Behavior):
    @override
    def perform(self, entity: Entity, state: str) -> None:
        player = cast(Player, entity)
        if "referee play_on" in state:
            player.playing = True
        if player.playing:
            player.dash(70)


class AttackBehavior(Behavior):
    @override
    def perform(self, entity: Entity, state: str) -> None:
        player = cast(Player, entity)
        if "referee play_on" in state:
            player.playing = True

        if "referee kick_off_l" in state:
            player.kick(100, 0)

        if player.playing:
            player.dash(90)


behaviors: dict[Role, Behavior] = {
    Role.GOALKEEPER: GoalKeeperBehavior(),
    Role.DEFENSE: DefenseBehavior(),
    Role.MIDDLE: MiddleBehavior(),
    Role.FORWARD: AttackBehavior(),
}
