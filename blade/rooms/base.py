"""
Base class for Death House rooms and challenge scenes.
"""

from typing import Tuple, List, Optional, Any, Dict
from blade.player import Player
from blade.terminal import (
    RESET, BOLD, ITALIC, RED_BLOOD, RED_CRIMSON, RED_RUST, RED_DARK,
    YELLOW_AMBER, YELLOW_WARNING, BLUE_STEEL, GRAY_SLATE, GRAY_LIGHT,
    WHITE_BONE, corrupt_glitch, box_text, horizontal_rule
)


class Room:
    """Base class for every chamber and trap in the house."""

    def __init__(self, room_id: str, title: str, act: str):
        self.room_id: str = room_id
        self.title: str = title
        self.act: str = act
        self.visited: bool = False

    def get_header(self) -> str:
        return (
            f"{horizontal_rule('═', RED_RUST, 76)}\n"
            f"  {WHITE_BONE}{BOLD}{self.title.upper()}{RESET}  {GRAY_SLATE}[{self.act}]{RESET}\n"
            f"{horizontal_rule('─', RED_DARK, 76)}"
        )

    def render(self, player: Player) -> Tuple[str, List[Tuple[str, str]]]:
        """
        Returns (room_narrative_text, list_of_choices).
        Each choice is a tuple: (choice_command, choice_label).
        """
        raise NotImplementedError

    def handle_choice(self, choice: str, player: Player) -> Tuple[Optional[str], str]:
        """
        Handles player input for this room.
        Returns:
            (next_room_id, response_narrative)
            If next_room_id is None, the player stays in this room.
            If next_room_id is "DEATH", game over triggers.
            If next_room_id is "VICTORY", ending triggers.
        """
        raise NotImplementedError

    def examine(self, target: str, player: Player) -> Optional[str]:
        """Optional context inspection for specific objects."""
        return None
