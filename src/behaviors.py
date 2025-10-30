from abc import ABC, abstractmethod
from typing import override

from models import Player, Role


class Behavior(ABC):
    """Abstract base class for player behaviors."""

    @abstractmethod
    def perform(self, player: Player, state: str) -> None:
        """Defines how a player behaves given the current game state."""
        pass


class GoalKeeperBehavior(Behavior):
    @override
    def perform(self, player: Player, state: str) -> None:
        if "ball" in state:
            print(f"🧤 {player.name} se prepara para atajar")
        else:
            pass


class DefenseBehavior(Behavior):
    @override
    def perform(self, player: Player, state: str) -> None:
        if "referee play_on" in state:
            player.playing = True
        if player.playing:
            player.dash(50)
            print(f"🛡️ {player.name} defiende su zona")


class MiddleBehavior(Behavior):
    @override
    def perform(self, player: Player, state: str) -> None:
        if "referee play_on" in state:
            player.playing = True
        if player.playing:
            player.dash(70)
            print(f"🏃 {player.name} apoya el ataque")


class AttackBehavior(Behavior):
    @override
    def perform(self, player: Player, state: str) -> None:
        if "referee play_on" in state:
            player.playing = True

        if "referee kick_off_l" in state:
            player.kick(100, 0)
            print(f"💥 {player.name} patea el balón")

        if player.playing:
            player.dash(90)


behaviors: dict[Role, Behavior] = {
    Role.GOALKEEPER: GoalKeeperBehavior(),
    Role.DEFENSE: DefenseBehavior(),
    Role.MIDDLE: MiddleBehavior(),
    Role.FORWARD: AttackBehavior(),
}
