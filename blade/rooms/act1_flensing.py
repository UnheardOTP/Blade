"""
Act I: The Flensing
Rooms: Razor Hallway, Scales of Atonement, Soundless Chamber.
"""

from typing import Tuple, List, Optional
from blade.rooms.base import Room
from blade.player import Player
from blade.audio_tapes import render_tape
from blade.terminal import (
    RESET, BOLD, ITALIC, RED_BLOOD, RED_CRIMSON, RED_RUST, RED_DARK,
    YELLOW_AMBER, YELLOW_WARNING, BLUE_STEEL, GRAY_SLATE, GRAY_LIGHT,
    WHITE_BONE, GREEN_ACID, corrupt_glitch
)


class RazorHallwayRoom(Room):
    """The razor-wire corridor."""

    def __init__(self):
        super().__init__("razor_hallway", "The Razor Hallway", "Act I: The Flensing")

    def render(self, player: Player) -> Tuple[str, List[Tuple[str, str]]]:
        text = (
            f"You stand at the entrance of a narrow 60-foot corridor of rusted corrugated steel.\n\n"
            f"Spanning wall to wall, strung at eye level, throat level, chest level, and shin level, "
            f"are hundreds of strands of taut, razor-sharp {RED_CRIMSON}monofilament piano wire{RESET}, "
            f"intertwined with barbed stainless-steel treble hooks dangling like cruel ornaments.\n\n"
            f"An industrial strobe light overhead flashes rhythmically: "
            f"{WHITE_BONE}[FLASH... dark... dark... FLASH...]{RESET}\n"
            f"In the white flashes, you see shredded denim and dried flaps of skin clinging to the steel mesh. "
            f"At the far end, an open exit portal glows with dim amber illumination."
        )

        choices = [
            ("1", "Drop flat on your stomach and crawl beneath the lowest wires along the concrete"),
            ("2", "Time the strobe light and sprint through the gaps in the wire web"),
            ("3", "Use your surgical scalpel to carefully sever the wire tension anchors along the wall")
        ]
        return text, choices

    def handle_choice(self, choice: str, player: Player) -> Tuple[Optional[str], str]:
        c = choice.strip()

        if c == "1":
            # Crawl under wires
            player.take_damage(12, blood_loss=4, pain="Sharp Stinging")
            player.inflict_wound("Shrapnel & Glass Punctures on Forearms and Knees", dex_loss=5, mob_loss=5)
            return "scales_of_atonement", (
                f"You drop to your belly. The concrete floor is carpeted with rusted metal shavings, shattered bottle glass, "
                f"and industrial staples. You drag yourself inch by inch beneath the razor wires.\n\n"
                f"Glass shards bite deep into your palms, forearms, and kneecaps (-12% HP, -4% Blood). "
                f"A low-hanging wire scrapes the crown of your scalp, drawing a warm trickle of blood, "
                f"but you avoid the lethal throat lines. You roll out the far end, gasping and bleeding."
            )

        elif c == "2":
            # Sprint timing
            if player.mobility >= 75:
                player.take_damage(8, blood_loss=2, pain="Lacerated Shoulder")
                return "scales_of_atonement", (
                    f"You wait for the strobe flash, fix the gaps in your memory, and launch forward in a desperate sprint!\n\n"
                    f"You twist your torso, ducking beneath a throat-level cord and leaping over an ankle snare. "
                    f"A hanging fishhook catches your shoulder, tearing your shirt and slicing a shallow line across your deltoid (-8% HP). "
                    f"You crash through the far threshold, chest heaving with adrenaline!"
                )
            else:
                player.take_damage(24, blood_loss=15, pain="Searing Agony")
                player.inflict_wound(
                    "Deep Quadriceps & Bicep Wire Laceration",
                    permanent_scar="Razor-Wire Crosshatch Scarring",
                    mob_loss=20,
                    dex_loss=10,
                    bleed_severity=2
                )
                player.inflict_trauma("Panic of Entanglement", sanity_loss=10)
                return "scales_of_atonement", (
                    f"{RED_BLOOD}[SNAG!]{RESET} Your impaired legs cannot match the timing of the strobe!\n\n"
                    f"Halfway down the hall, your shin catches an unseen tripwire. You stumble directly into a web of taut piano wires! "
                    f"High-tensile steel slices through your clothing and bites deep into your right thigh and left bicep! "
                    f"Barbed treble hooks sink into your flesh. With a scream of pure animal terror, you wrench yourself free, "
                    f"leaving strips of muscle behind on the wires!\n\n"
                    f"You tumble out of the hallway in a spray of blood. (-24% HP, -15% Blood, Level 2 Arterial Bleed, Permanent -20 Mobility)"
                )

        elif c == "3":
            # Disarm wires with scalpel
            if "scalpel" not in player.inventory:
                return None, f"{GRAY_SLATE}You do not have a surgical scalpel in your inventory.{RESET}"

            if player.dexterity >= 65:
                return "scales_of_atonement", (
                    f"With surgical focus, you approach the wall brackets. You use the scalpel to saw through the lead crimps "
                    f"anchoring three primary tension cables.\n\n"
                    f"With loud metallic *TWANGS*, the wires slacken and coil harmlessly onto the floor! "
                    f"You walk cleanly through the created path without suffering a single scratch."
                )
            else:
                player.take_damage(18, blood_loss=8, pain="Throbbing Agony")
                player.inflict_wound(
                    "High-Tension Wire Whiplash across Forearm",
                    permanent_scar="Deep Cord Contusion across Wrist",
                    dex_loss=15,
                    bleed_severity=1
                )
                return "scales_of_atonement", (
                    f"{RED_CRIMSON}[TWANG-WHIP!]{RESET} Your trembling, injured hands slip on the tension clamp!\n\n"
                    f"The high-tensile wire snaps under tremendous tension, whipping across your forearm like a steel razor! "
                    f"A deep arterial gash opens across your wrist (-18% HP, -8% Blood, Level 1 Bleed). "
                    f"The path clears as the web collapses, but you clutch your bleeding arm in agony."
                )

        return None, f"{GRAY_SLATE}The strobe light continues to flash against the waiting razor wires.{RESET}"


class ScalesOfAtonementRoom(Room):
    """The 2.5kg flesh sacrifice challenge."""

    def __init__(self):
        super().__init__("scales_of_atonement", "The Scales of Atonement", "Act I: The Flensing")

    def render(self, player: Player) -> Tuple[str, List[Tuple[str, str]]]:
        if not self.visited:
            self.visited = True
            player.unlock_tape("tape_02")

        caleb_text = (
            f"Inside an iron cage against the left wall lies {WHITE_BONE}Caleb{RESET}, a young man in his late 20s, "
            f"unconscious in stained scrubs, breathing in shallow, terrified gasps."
        )
        if "caleb_mutilated" in player.flags:
            caleb_text = f"Inside the cage, Caleb lies in a pool of dark blood, his severed lower leg roughly bandaged, weeping in shock."

        text = (
            f"You step into an octagonal surgical theater tiled in stained clinical white.\n\n"
            f"In the center, suspended by heavy iron chains above a bubbling pit of {GREEN_ACID}boiling caustic quicklime{RESET}, "
            f"is a massive brass balance scale.\n\n"
            f"The exit vault door is sealed by hydraulic deadbolts connected to the scale mechanism. A digital terminal displays:\n"
            f"{RED_BLOOD}[REQUIRED COUNTERWEIGHT: 2.50 KG]  [CURRENT WEIGHT: 0.00 KG]{RESET}\n\n"
            f"{caleb_text}\n\n"
            f"On an autopsy tray beside the brass scale sits a surgical bone saw, a scalpel, and tourniquet strips.\n\n"
            f"Against the right wall, inside a heavy copper mesh cage, sits an alternative: a dense {YELLOW_AMBER}2.5kg Lead Ballast Block{RESET}. "
            f"However, the cage is actively electrified with a roaring {YELLOW_WARNING}200-Volt transformer{RESET} crackling with sparks."
        )

        choices = [
            ("1", "Take the bone saw and amputate Caleb's lower leg to provide the 2.5kg counterweight"),
            ("2", "Carve into your own body: flay 2.5kg from your own thigh and sever your left pinky finger"),
            ("3", "Plunge both bare hands into the electrified cage to seize the 2.5kg lead ballast block"),
            ("4", "Attempt to pry the hydraulic lock cylinder open with your scalpel")
        ]
        return text, choices

    def handle_choice(self, choice: str, player: Player) -> Tuple[Optional[str], str]:
        c = choice.strip()

        if c == "1":
            # Mutilate Caleb
            if "caleb_mutilated" in player.flags:
                return None, f"{GRAY_SLATE}You have already taken Caleb's flesh.{RESET}"

            player.flags.add("caleb_mutilated")
            player.inflict_trauma("Executioner's Guilt / Caleb's Screams", sanity_loss=35)
            player.pain = "Cold Nausea"

            return "decibel_chamber", (
                f"{RED_BLOOD}[THE TOLL OF ANOTHER]{RESET}\n\n"
                f"You pick up the heavy surgical bone saw. You step into Caleb's cage. He stirs, eyes fluttering open in horror "
                f"as you pin his leg down to the concrete.\n\n"
                f"\"NO! PLEASE! GOD, PLEASE NO—!\"\n\n"
                f"The stainless-steel teeth bite into his tibia. Blood fountains across the tiles. Caleb's screams tear the air "
                f"until his vocal cords hemorrhage and he blacks out from neurogenic shock.\n\n"
                f"You carry the severed lower leg, dripping with arterial blood, and drop it onto the brass scale pan. "
                f"The scale groans: {WHITE_BONE}[REGISTERED: 2.68 KG]{RESET}!\n\n"
                f"The hydraulic blast door groans and unlocks. You turn away from Caleb's bleeding form, your hands coated in warm, "
                f"guilty blood. You saved your own skin, but your humanity is hollowed out. (-35% Sanity, Permanent Trauma)"
            )

        elif c == "2":
            # Self-mutilation
            player.flags.add("self_sacrificed")
            player.take_damage(30, blood_loss=25, pain="Excruciating Agony")
            player.inflict_wound(
                "Surgically Flayed Quadriceps & Amputated Left Pinky",
                permanent_scar="Flayed Thigh & Four-Finger Left Hand",
                mob_loss=25,
                dex_loss=15,
                bleed_severity=2
            )
            player.inflict_trauma("Memory of Self-Carving", sanity_loss=15)

            return "decibel_chamber", (
                f"{RED_BLOOD}[THE TOLL OF THE SELF]{RESET}\n\n"
                f"You refuse to become Locke's monster. You lay your left hand on the tray, take the scalpel, and slice through "
                f"the knuckle joint of your left pinky. Agony flares white in your skull as bone shears free!\n\n"
                f"You bite down on your sleeve until your gums bleed, then drive the scalpel deep into your own right quadriceps. "
                f"In agonizing, deliberate strokes, you peel slabs of dense adipose tissue and muscle from your own leg, "
                f"heaping the wet, steaming flesh onto the brass scale.\n\n"
                f"Your vision darkens with catastrophic blood loss. Finally: {WHITE_BONE}[REGISTERED: 2.51 KG]{RESET}!\n\n"
                f"The blast door hisses open. You collapse against the doorway, applying a desperate tourniquet to your mutilated leg. "
                f"Caleb remains unharmed in his cage, staring at you in disbelieving horror. "
                f"(-30% HP, -25% Blood, Level 2 Bleed, Permanent -25 Mobility, -15 Dexterity)"
            )

        elif c == "3":
            # Seize electrified ballast
            player.flags.add("hands_burned")
            player.take_damage(25, pain="Searing Agony")
            player.inflict_wound(
                "Third-Degree Electrical Arc Burns on Both Palms",
                permanent_scar="Charred Carbon-Scarred Palms",
                dex_loss=30
            )
            player.inflict_trauma("Memory of 200V Arc Convulsion", sanity_loss=12)
            player.add_item("lead_ballast", 1)

            return "decibel_chamber", (
                f"{YELLOW_WARNING}[THE PATH OF PURE WILLPOWER]{RESET}\n\n"
                f"You refuse the knife entirely. You step up to the humming copper cage, wrap your fingers around the heavy "
                f"lead block, and pull.\n\n"
                f"200 VOLTS OF ELECTRIC CURRENT SURGES INTO YOUR ARMS!\n"
                f"Your muscles violently contract in tetanic spasm! The scent of scorched flesh and ozone fills the air as the "
                f"epidermis of both palms chars to black carbon. Teeth rattling violently, through sheer superhuman defiance, "
                f"you wrench the 2.5kg ballast block out of the arc-mesh and slam it down onto the brass scale!\n\n"
                f"The scale drops with a heavy *CLANG*! The hydraulic door unlatches!\n\n"
                f"You look down at your smoking, blackened hands. You spared all blood and flesh, but your fingers will never hold "
                f"a delicate tool the same way again. (-25% HP, Permanent -30 Dexterity)"
            )

        elif c == "4":
            # Pry door with scalpel
            player.take_damage(15, pain="Shrapnel in Face")
            player.inflict_wound("Scalpel Blade Fragment Embedded in Cheek", per_loss=10)
            return None, (
                f"You wedge the surgical scalpel into the hydraulic seam and lever your weight against it.\n\n"
                f"{RED_CRIMSON}[SNAP!]{RESET} The brittle surgical carbon blade shatters! A razor fragment ricochets violently "
                f"into your cheek, slicing open your face (-15% HP, -10% Perception). The heavy hydraulic deadbolts laugh at your effort."
            )

        return None, f"{GRAY_SLATE}The brass scale hangs balanced over the boiling quicklime. The toll remains unpaid.{RESET}"


class DecibelChamberRoom(Room):
    """The soundless corridor with acoustic transducers and spike hammers."""

    def __init__(self):
        super().__init__("decibel_chamber", "The Soundless Chamber", "Act I: The Flensing")

    def render(self, player: Player) -> Tuple[str, List[Tuple[str, str]]]:
        if not self.visited:
            self.visited = True
            player.unlock_tape("tape_03")

        text = (
            f"You step into an eerie, sound-dampened chamber lined with dark charcoal acoustic baffles.\n\n"
            f"Mounted every six feet along the walls are sensitive directional microphones wired to glowing red LED meters:\n"
            f"{RED_CRIMSON}[THRESHOLD: 15 DECIBELS — EXCESS SOUND TRIGGERS KINETIC EJECTION]{RESET}\n\n"
            f"The floor is a minefield: four inches deep in shattered window glass, dried animal ribs, and loose "
            f"brass windchime clappers.\n\n"
            f"At the far end of the room sits a stone pedestal. Inside an open glass bell jar rests a heavy {YELLOW_AMBER}Copper Skeleton Key{RESET}.\n\n"
            f"Directly above the pathway, suspended on high-tension steel cables, are two massive {RED_BLOOD}40-pound iron spike hammers{RESET}, "
            f"cocked back against powerful industrial coil springs, aimed directly across the corridor."
        )

        choices = [
            ("1", "Remove shoes and crawl inch by inch across the glass, suppressing every sound and breath"),
            ("2", "Throw an object (a bone shard or loose tool) at the far corner to trip the acoustic sensors safely"),
            ("3", "Sprint with everything you have to the pedestal and snatch the key before the hammers can release")
        ]
        return text, choices

    def handle_choice(self, choice: str, player: Player) -> Tuple[Optional[str], str]:
        c = choice.strip()

        if c == "1":
            # Stealth crawl
            player.take_damage(6, pain="Pricked Palms")
            player.inflict_trauma("Paralyzing Fear of Sound", sanity_loss=10)
            player.add_item("copper_key", 1)

            return "pendulum_theatre", (
                f"You strip your shoes and drop onto the sea of glass and dry bone.\n\n"
                f"Every inch demands supreme muscle control. Glass fragments pierce your knees and palms (-6% HP), but you "
                f"force your throat closed, swallowing your groans of pain. The red LED decibel meters flicker: "
                f"{YELLOW_WARNING}[8 dB... 11 dB... 13 dB...]{RESET}\n\n"
                f"Your heart thumps like a war drum in your chest. After ten agonizing minutes of glacial crawling, your trembling fingers "
                f"reach into the bell jar and lift the {YELLOW_AMBER}Copper Skeleton Key{RESET}!\n\n"
                f"You slide into the exit archway and unlock the heavy iron gate into {RED_BLOOD}Act II: The Mechanism{RESET}!"
            )

        elif c == "2":
            # Clever disarm
            player.add_item("copper_key", 1)
            player.inflict_trauma("Sonic Shock", sanity_loss=5)

            return "pendulum_theatre", (
                f"You pick up a heavy, jagged animal rib from the doorway and fling it with precise aim toward the far concrete corner!\n\n"
                f"{RED_BLOOD}[CRACK!]{RESET} The bone shatters against the far wall! The decibel meters instantly spike to {RED_BLOOD}92 dB{RESET}!\n\n"
                f"With a deafening mechanical roar: {BOLD}[WHAM! WHAM!]{RESET}\n"
                f"The two 40-pound spike hammers whip violently across the empty room, embedding their foot-long steel spikes "
                f"deep into the opposite concrete wall in a spray of sparks and pulverized stone!\n\n"
                f"The kinetic springs hang expended and inert. You walk safely over the glass, retrieve the {YELLOW_AMBER}Copper Skeleton Key{RESET}, "
                f"and unlock the portal to {RED_BLOOD}Act II: The Mechanism{RESET}!"
            )

        elif c == "3":
            # Panic sprint
            player.take_damage(34, blood_loss=20, pain="Crushed Ribs")
            player.inflict_wound(
                "Blunt Chest Trauma & Fractured Left Ribs",
                permanent_scar="Ruptured Left Eardrum & Severe Tinnitus",
                mob_loss=15,
                per_loss=25,
                bleed_severity=2
            )
            player.add_item("copper_key", 1)

            return "pendulum_theatre", (
                f"{RED_BLOOD}[CRUNCH-CRACK-CLATTER!]{RESET} You launch into a reckless dash across the broken glass!\n\n"
                f"Glass screams under your boots, bones snap, brass clappers chime! The LED meters overload into blinding crimson: "
                f"{RED_BLOOD}[110 dB! MAXIMUM DISCHARGE!]{RESET}\n\n"
                f"A siren wails at 130 decibels, instantly rupturing your left eardrum in a wash of warm blood! "
                f"From the ceiling, the first spike hammer snaps forward with horrific kinetic force, "
                f"smashing into the side of your chest!\n\n"
                f"Three ribs crack like dry pine branches. Air explodes from your lungs as you are flung violently across the room, "
                f"crashing onto the stone plinth. Your bloodied fingers clasp around the {YELLOW_AMBER}Copper Key{RESET}.\n\n"
                f"Coughing frothy blood, you drag yourself through the exit threshold into Act II. "
                f"(-34% HP, -20% Blood, Level 2 Bleed, Permanent Tinnitus / -25 Perception)"
            )

        return None, f"{GRAY_SLATE}The acoustic transducers hum in the dead silence. One false sound will release the hammers.{RESET}"
