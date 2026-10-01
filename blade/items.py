"""
Items, medical supplies, and inventory items for Blade.
"""

from typing import Dict, Any

ITEMS: Dict[str, Dict[str, Any]] = {
    "tourniquet": {
        "id": "tourniquet",
        "name": "Elastic Tourniquet / Clean Cloth",
        "desc": "Heavy-duty medical band or torn sterile cloth. Can stanch active arterial bleeding.",
        "usable": True,
        "consumable": True,
        "category": "medical"
    },
    "scalpel": {
        "id": "scalpel",
        "name": "No. 10 Surgical Scalpel",
        "desc": "Rusted knurled brass handle with a terrifyingly sharp carbon-steel blade.",
        "usable": True,
        "consumable": False,
        "category": "tool"
    },
    "lighter": {
        "id": "lighter",
        "name": "Brass Zippo Lighter",
        "desc": "Heavy brass lighter with a dim flickering flame. Can illuminate dark areas or cauterize severe wounds.",
        "usable": True,
        "consumable": False,
        "category": "tool"
    },
    "adrenaline_syringe": {
        "id": "adrenaline_syringe",
        "name": "Epinephrine Auto-Injector",
        "desc": "Emergency syringe loaded with 1mg of adrenaline. Drastically boosts heart rate, suppresses pain shock, and restores mobility, at the cost of sanity.",
        "usable": True,
        "consumable": True,
        "category": "medical"
    },
    "copper_wire": {
        "id": "copper_wire",
        "name": "Spool of Insulated Copper Wire",
        "desc": "Salvaged from an electric relay. Can be used to short-circuit electronic locks or probe tripwires.",
        "usable": True,
        "consumable": False,
        "category": "tool"
    },
    "bone_splint": {
        "id": "bone_splint",
        "name": "Carved Bone Splint & Gauze",
        "desc": "Rigid splint fashioned from human rib bone and medical gauze. Stabilizes broken limbs to restore mobility.",
        "usable": True,
        "consumable": True,
        "category": "medical"
    },
    "cassette_player": {
        "id": "cassette_player",
        "name": "Pocket Cassette Player",
        "desc": "Rattling portable cassette player with a tinny speaker and bloodstained rewind button.",
        "usable": True,
        "consumable": False,
        "category": "tool"
    },
    "formalin_eye": {
        "id": "formalin_eye",
        "name": "Preserved Prosthetic Glass Eye",
        "desc": "A cold, hand-painted glass iris extracted from Dr. Locke's anatomical dummy. Matches the optical scanner.",
        "usable": True,
        "consumable": False,
        "category": "quest"
    },
    "lead_ballast": {
        "id": "lead_ballast",
        "name": "2.5kg Lead Ballast Block",
        "desc": "Dense lead weight retrieved from the electrified cage. Seared with the charred imprint of human skin.",
        "usable": True,
        "consumable": False,
        "category": "quest"
    }
}
