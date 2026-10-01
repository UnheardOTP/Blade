"""
Room registration and room instantiation for Blade.
"""

from typing import Dict
from blade.rooms.base import Room
from blade.rooms.prologue import CisternWakeRoom, CisternDrainRoom
from blade.rooms.act1_flensing import RazorHallwayRoom, ScalesOfAtonementRoom, DecibelChamberRoom
from blade.rooms.act2_mechanism import PendulumTheatreRoom, ChemicalBasinRoom, OpticLabyrinthRoom
from blade.rooms.act3_crucible import NitrogenKilnRoom, ConfessionalRoom, HallucinatoryCorridor
from blade.rooms.act4_sanctum import EngineRoom, ArchitectSanctumRoom


def create_room_registry() -> Dict[str, Room]:
    """Creates a fresh isolated set of room instances for a game session."""
    return {
        "cistern_wake": CisternWakeRoom(),
        "cistern_drain": CisternDrainRoom(),
        "razor_hallway": RazorHallwayRoom(),
        "scales_of_atonement": ScalesOfAtonementRoom(),
        "decibel_chamber": DecibelChamberRoom(),
        "pendulum_theatre": PendulumTheatreRoom(),
        "chemical_basin": ChemicalBasinRoom(),
        "optic_labyrinth": OpticLabyrinthRoom(),
        "nitrogen_kiln": NitrogenKilnRoom(),
        "confessional": ConfessionalRoom(),
        "hallucinatory_corridor": HallucinatoryCorridor(),
        "engine_room": EngineRoom(),
        "architect_sanctum": ArchitectSanctumRoom()
    }
