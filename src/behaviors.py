from typing import cast, override

from models import Behavior, Entity, Player, Role


class GoalKeeperBehavior(Behavior[Player]):
    """Behavior of a GoalKeeper"""

    @override
    def perform(self, entity: Player, state: str) -> None:
        if "ball" in state:
            print(f"🧤 {entity.name} se prepara para atajar")
        else:
            pass


class DefenseBehavior(Behavior[Player]):
    @override
    def perform(self, entity: Player, state: str) -> None:
        if "referee play_on" in state:
            entity.playing = True
        if entity.playing:
            entity.dash(50)


class MiddleBehavior(Behavior[Player]):
    @override
    def perform(self, entity: Player, state: str) -> None:
        if "referee play_on" in state:
            entity.playing = True
        if entity.playing:
            entity.dash(70)


class AttackBehavior(Behavior[Player]):
    @override
    def perform(self, entity: Player, state: str) -> None:
        if "referee play_on" in state:
            entity.playing = True

        if "referee kick_off_l" in state:
            entity.kick(100, 0)

        if entity.playing:
            entity.dash(90)


behaviors: dict[Role, Behavior] = {
    Role.GOALKEEPER: GoalKeeperBehavior(),
    Role.DEFENSE: DefenseBehavior(),
    Role.MIDDLE: MiddleBehavior(),
    Role.FORWARD: AttackBehavior(),
}
