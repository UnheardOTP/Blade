"""
Act IV: The Sanctum
Rooms: Master Engine Room, The Architect's Sanctum & Threshold (Endings).
"""

from typing import Tuple, List, Optional
from blade.rooms.base import Room
from blade.player import Player
from blade.terminal import (
    RESET, BOLD, ITALIC, RED_BLOOD, RED_CRIMSON, RED_RUST, RED_DARK,
    YELLOW_AMBER, YELLOW_WARNING, BLUE_STEEL, GRAY_SLATE, GRAY_LIGHT,
    WHITE_BONE, GREEN_ACID, GREEN_TOXIC, SKULL_ART, box_text
)


class EngineRoom(Room):
    """The colossal clockwork machinery room."""

    def __init__(self):
        super().__init__("engine_room", "The Master Engine Room", "Act IV: The Sanctum")

    def render(self, player: Player) -> Tuple[str, List[Tuple[str, str]]]:
        text = (
            f"You emerge into a cathedral of kinetic fury: the mechanical heart of the house.\n\n"
            f"Colossal {RED_RUST}20-foot cast-iron clockwork gears{RESET} rotate with earth-shaking thuds. "
            f"Steam pistons plunge with deafening pneumatic roars. Razor-toothed conveyor rollers carry "
            f"shredded steel and bone toward an open smelting hearth.\n\n"
            f"The walkway to the upper control balcony has been sheared away. You must cross the active machinery: "
            f"timing the rotating gear teeth, leaping between moving piston shafts, or finding an alternate route.\n\n"
            f"Above the machinery on the high observation deck, an illuminated glass archway beckons: "
            f"{WHITE_BONE}[THE ARCHITECT'S SANCTUM]{RESET}."
        )

        choices = [
            ("1", "Time the rhythm of the plunging steam pistons and sprint-jump across their flat heads"),
            ("2", "Drop onto your stomach and crawl through the narrow oil-lubrication conduit beneath the main drive gear"),
            ("3", "Jam the master gear train using a heavy item or ballast block from your inventory")
        ]
        return text, choices

    def handle_choice(self, choice: str, player: Player) -> Tuple[Optional[str], str]:
        c = choice.strip()

        if c == "1":
            # Jump pistons
            if player.mobility >= 55:
                player.take_damage(10, pain="Bruised Shins")
                return "architect_sanctum", (
                    f"You focus every ounce of remaining will into your legs. As the first 4-ton piston plunges, "
                    f"you leap onto its iron surface!\n\n"
                    f"The shock rattles your skeletal frame, but you launch forward to the second piston, "
                    f"then spring across the grinding gear teeth to grab the upper catwalk railing!\n\n"
                    f"You haul yourself over the steel lip, bruised and panting (-10% HP). "
                    f"Directly ahead lies the final chamber."
                )
            else:
                player.take_damage(26, pain="Crushed Tibia")
                player.inflict_wound(
                    "Compound Fracture of Left Fibula",
                    permanent_scar="Shattered & Deformed Lower Leg",
                    mob_loss=30
                )
                return "architect_sanctum", (
                    f"{RED_BLOOD}[CRUSH!]{RESET} Your crippled leg cannot clear the distance!\n\n"
                    f"As you land, the piston ascends violently, catching your lower leg against the steel frame! "
                    f"Bone snaps with an agonizing crack (-26% HP, -30% Mobility)! In a surge of blind survival terror, "
                    f"you drag your broken limb across the iron lip onto the observation catwalk.\n\n"
                    f"You drag yourself through the doorway into the Sanctum."
                )

        elif c == "2":
            # Crawl conduit
            player.take_damage(12, pain="Boiling Oil Scalds")
            player.inflict_wound("Boiling Machine Oil Scalds on Back", dex_loss=5)

            return "architect_sanctum", (
                f"You slide into the low drainage conduit beneath the churning gear train.\n\n"
                f"Boiling black lubricant and grease wash over your back and shoulders, scalding your skin (-12% HP), "
                f"but you keep your head low as the massive steel teeth churn mere inches above your spine.\n\n"
                f"You pull yourself out of the inspection hatch on the upper platform, covered in black grease and blood."
            )

        elif c == "3":
            # Jam gears
            if "lead_ballast" in player.inventory:
                player.remove_item("lead_ballast", 1)
                return "architect_sanctum", (
                    f"{GREEN_ACID}[CATASTROPHIC GEAR JAM]{RESET}\n\n"
                    f"You heave the dense {YELLOW_AMBER}2.5kg Lead Ballast Block{RESET} directly between the interlocking "
                    f"teeth of the master drive wheel!\n\n"
                    f"A sound like an artillery shell detonating tears through the chamber! "
                    f"The hardened lead block lodges into the forged cogs. The drive shaft violently torques, shearing iron teeth "
                    f"in a massive fountain of sparks! The entire engine room grinds to a shuddering, smoking HALT!\n\n"
                    f"With the machinery dead and silent, you walk serenely across the frozen gears to the Sanctum door."
                )
            else:
                return None, f"{GRAY_SLATE}You do not have a heavy enough object in your inventory to jam the massive gears.{RESET}"

        return None, f"{GRAY_SLATE}The clockwork gears continue their deafening roar.{RESET}"


class ArchitectSanctumRoom(Room):
    """The final confrontation and biometric vault threshold."""

    def __init__(self):
        super().__init__("architect_sanctum", "The Architect's Sanctum & Threshold", "Act IV: The Sanctum")

    def render(self, player: Player) -> Tuple[str, List[Tuple[str, str]]]:
        caleb_presence = ""
        if "self_sacrificed" in player.flags or "hands_burned" in player.flags:
            caleb_presence = f"\n{GREEN_TOXIC}Beside you stands Caleb, limping and pale, leaning on you for support.{RESET}"

        text = (
            f"You step into the final room: a cold, clinical amphitheater bathed in the flickering phosphor glow "
            f"of dozens of CRT security monitors. Every screen displays a room you crawled through—the cistern, "
            f"the razor hall, the scales, the pendulum, the kiln.\n\n"
            f"In the center, hooked to an intravenous drip and an audible cardiac monitor, sits an iron wheelchair. "
            f"Resting inside is {WHITE_BONE}Dr. Gabriel Locke{RESET}—emaciated, pale, wearing a surgical smock stained with old iodine, "
            f"his breathing aided by a whistling ventilator.\n\n"
            f"Behind Locke stands the final obstacle: a massive {WHITE_BONE}10-ton steel vault door{RESET}. "
            f"Through the seam of the door, {YELLOW_AMBER}thin beams of real morning sunlight{RESET} and the smell of fresh dawn rain "
            f"pour across the bloodstained tiles.\n\n"
            f"Beside the door sits a biometric terminal and scale: {RED_CRIMSON}[THRESHOLD BIOMETRICS: SACRIFICE EVALUATION]{RESET}.\n\n"
            f"Dr. Locke turns his gaunt, sunken face toward you. A faint, terrible smile touches his cracked lips.\n\n"
            f"{GRAY_LIGHT}\"Look at what you have become. You walked into this house hollow, blind, numb to the gift of breath. "
            f"Now, you stand before the dawn carved into something real.\n\n"
            f"Step onto the biometric scale, subject. Let the house measure what you have paid.\"{RESET}{caleb_presence}"
        )

        choices = [
            ("1", "Step onto the biometric scale and submit your transformed body to the final evaluation"),
            ("2", "Lunge across the room and drive your surgical scalpel into Dr. Locke's throat"),
            ("3", "Demand Locke explain what the point of all this agony was")
        ]
        return text, choices

    def handle_choice(self, choice: str, player: Player) -> Tuple[Optional[str], str]:
        c = choice.strip()

        if c == "3":
            return None, (
                f"Locke draws a ragged breath through his ventilator, his eyes burning with clinical devotion:\n\n"
                f"{GRAY_LIGHT}\"The point? The point is that humanity takes life for granted until the blade touches bone. "
                f"You never appreciated your fingers until you broke them. You never appreciated your blood until it drained. "
                f"I did not destroy you. I excised your numbness. The pain you feel right now is the only proof you have ever had "
                f"that you are truly, undeniably alive.\"{RESET}"
            )

        elif c == "2":
            # Kill Locke directly
            player.flags.add("killed_locke")
            return "VICTORY_DISCIPLE" if player.sanity < 30 else "VICTORY_SURVIVOR", (
                f"{RED_BLOOD}[THE FINAL INCISION]{RESET}\n\n"
                f"You grip your surgical scalpel and lunge at the frail man in the wheelchair. Locke does not flinch. "
                f"His dark eyes watch you with calm satisfaction as you drive the carbon blade deep into his jugular vein.\n\n"
                f"Warm arterial blood sprays across your face. Locke coughs, blood bubbling on his lips, and whispers:\n"
                f"{GRAY_LIGHT}\"Good... You have shed your hesitation. The scalpel is yours now...\"{RESET}\n\n"
                f"His heart monitor drops into a flatline: {RED_BLOOD}[BEEEEEEEP]{RESET}!\n"
                f"The flatline signal triggers the emergency fail-safe relay: the massive 10-ton vault door unlatches with an explosive roar!"
            )

        elif c == "1":
            # Biometric evaluation -> Branch to Endings!
            total_scars = len(player.scars_physical) + len(player.scars_mental)

            # Check Ending 2: Flayed Husk (Too weak / exsanguinated)
            if player.blood <= 25 or player.hp <= 15:
                return "ENDING_FLAYED_HUSK", (
                    f"{YELLOW_WARNING}[THE EXHAUSTION OF THE VESSEL]{RESET}\n\n"
                    f"You step onto the steel platform. The scale registers your weight, scanning your scars and vital signs.\n"
                    f"The biometric chime rings: {GREEN_ACID}[TRANSFORMATION VERIFIED. VAULT UNLATCHED.]{RESET}!\n\n"
                    f"The 10-ton steel door swings open. The blinding light of dawn floods your eyes. "
                    f"You step over the threshold onto the wet gravel driveway outside..."
                )

            # Check Ending 5: Psychotic Severance
            if player.sanity <= 15:
                return "ENDING_PSYCHOTIC", (
                    f"{RED_BLOOD}[THE SEVERED CONSCIOUSNESS]{RESET}\n\n"
                    f"You step onto the scale, but your eyes cannot focus. The sunlight streaming through the doorway "
                    f"looks like boiling white acid. Phantom voices scream from the walls..."
                )

            # Check Ending 4: The Broken Martyr (Caleb is alive and escaped)
            if ("self_sacrificed" in player.flags or "hands_burned" in player.flags) and player.mobility < 50:
                return "ENDING_MARTYR", (
                    f"{GREEN_ACID}[THE MARTYR'S SACRIFICE]{RESET}\n\n"
                    f"The scale registers your weight. A red buzzer blares: {RED_CRIMSON}[OVERLOAD: DUAL OCCUPANCY DETECTED. "
                    f"LOCKDOWN IN 10 SECONDS UNLESS ONE VESSEL REMAINS.]{RESET}\n\n"
                    f"You look at Caleb. He tries to pull you forward, but your broken legs give way..."
                )

            # Check Ending 3: Disciple
            if "caleb_mutilated" in player.flags and player.sanity < 45 and "killed_locke" not in player.flags:
                return "ENDING_DISCIPLE", (
                    f"{RED_DARK}[THE INHERITANCE OF THE BLADE]{RESET}\n\n"
                    f"You step onto the scale. Locke watches you not as a victim, but as a masterpiece.\n"
                    f"The terminal chimes: {WHITE_BONE}[SURGICAL LOGIC CONFIRMED. SUCCESSOR DETECTED.]{RESET}..."
                )

            # Default: Ending 1: The Hollow Survivor
            return "ENDING_HOLLOW_SURVIVOR", (
                f"{WHITE_BONE}[THE TOLL PAID IN FULL]{RESET}\n\n"
                f"You step onto the cold brass scale. The laser traces the map of scars across your body:\n"
                f"Your dislocated thumb, your burned palms, your wire gashes, your missing flesh, your haunted eyes.\n\n"
                f"The terminal computes the biological debt: {GREEN_ACID}[TRIBUTE SATISFIED. THE VESSEL IS PURIFIED.]{RESET}\n\n"
                f"With an earth-shaking pneumatic roar, the 10-ton blast door swings wide into the morning dawn!"
            )

        return None, f"{GRAY_SLATE}Locke waits in his wheelchair before the vault door.{RESET}"
