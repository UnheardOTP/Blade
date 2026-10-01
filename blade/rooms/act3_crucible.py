"""
Act III: The Crucible
Rooms: Nitrogen Kiln, Confessional Crucible, Hallucinatory Corridor.
"""

from typing import Tuple, List, Optional
from blade.rooms.base import Room
from blade.player import Player
from blade.terminal import (
    RESET, BOLD, ITALIC, RED_BLOOD, RED_CRIMSON, RED_RUST, RED_DARK,
    YELLOW_AMBER, YELLOW_WARNING, BLUE_FROST, BLUE_STEEL, GRAY_SLATE,
    GRAY_LIGHT, WHITE_BONE, GREEN_ACID, corrupt_glitch
)


class NitrogenKilnRoom(Room):
    """The thermal paradox chamber (Liquid Nitrogen vs Scalding Steam)."""

    def __init__(self):
        super().__init__("nitrogen_kiln", "The Nitrogen Kiln", "Act III: The Crucible")

    def render(self, player: Player) -> Tuple[str, List[Tuple[str, str]]]:
        if not self.visited:
            self.visited = True
            player.unlock_tape("tape_04")

        text = (
            f"You step into an insulated pressure chamber bisected by a shimmering thermal rift.\n\n"
            f"On your left: A sub-zero void. White, rolling clouds of {BLUE_FROST}-40°C liquid nitrogen fog{RESET} "
            f"vent from frost-coated steel pipes. The iron catwalk is crusted with jagged hoarfrost.\n\n"
            f"On your right: A roaring blast furnace. {RED_BLOOD}95°C superheated industrial steam{RESET} jets from "
            f"ruptured iron flues, radiating blistering heat that warps the air.\n\n"
            f"In the center of the chamber stands a dual hydraulic bypass console with two opposing brass butterfly valves:\n"
            f"{BLUE_FROST}[VALVE A: CRYOGENIC BYPASS]{RESET}  &  {RED_CRIMSON}[VALVE B: THERMAL RELIEF]{RESET}\n\n"
            f"A pressure gauge needles into the red: both valves must be rotated 180 degrees simultaneously within seconds "
            f"to equalize the atmospheric pressure and unseal the blast doors."
        )

        choices = [
            ("1", "Wrap your hands in cloth/tourniquet, plunge into both zones, and turn both valves together"),
            ("2", "Use your brass lighter and copper wire to wedge and tether the steam valve before tackling the frozen side"),
            ("3", "Hesitate in the middle, looking for an electronic control panel or bypass wire")
        ]
        return text, choices

    def handle_choice(self, choice: str, player: Player) -> Tuple[Optional[str], str]:
        c = choice.strip()

        if c == "1":
            # Direct thermal endurance
            player.take_damage(16, pain="Thermal Shock")
            player.inflict_wound(
                "Superficial Frostbite on Left Hand & Steam Scald on Right Wrist",
                dex_loss=10
            )

            return "confessional", (
                f"{BLUE_FROST}[THERMAL EQUILIBRIUM]{RESET}\n\n"
                f"You wrap your forearms in cloth, take a deep breath of freezing, scalding air, and reach into both extremes!\n\n"
                f"Your left hand plunges into the nitrogen fog: the cold burns with the ferocity of acid, freezing droplets "
                f"of sweat onto your skin like glass beads (-8% HP). Your right hand grasps the superheated steam valve: "
                f"hot metal blisters your palms through the cloth (-8% HP)!\n\n"
                f"Gritting your teeth through the thermal paradox, you haul both brass wheels in unison: {WHITE_BONE}[HISS-THUD!]{RESET}\n\n"
                f"The pressure equalizer roars, venting steam and fog into the ceiling exhaust! The magnetic pressure seal drops, "
                f"and the exit vault slides open into {RED_DARK}The Confessional{RESET}."
            )

        elif c == "2":
            # Clever tether
            if "copper_wire" in player.inventory:
                player.take_damage(6, pain="Mild Frostbite")
                return "confessional", (
                    f"{GREEN_ACID}[TACTICAL BYPASS]{RESET}\n\n"
                    f"You refuse to divide your body between fire and ice. Using your {YELLOW_AMBER}copper wire{RESET}, "
                    f"you lasso the steam valve lever and anchor it to a steel railing, wrenching it open without standing in the heat plume!\n\n"
                    f"With the thermal side locked, you use both hands and your jacket to turn the frozen cryogenic valve. "
                    f"Frost bites your knuckles (-6% HP), but the valve spins open smoothly!\n\n"
                    f"The chamber depressurizes with a satisfied sigh. The vault door slides open into {RED_DARK}The Confessional{RESET}."
                )
            else:
                player.take_damage(12, pain="Singed Flesh")
                return "confessional", (
                    f"Lacking wire, you improvise with your lighter casing to jam the steam valve. You suffer light scalds (-12% HP), "
                    f"but manage to open both valves and depressurize the chamber."
                )

        elif c == "3":
            # Hesitation
            player.take_damage(28, pain="Thermal Rupture")
            player.inflict_wound(
                "Bilateral Thermal Shock & Severe Scalding",
                permanent_scar="Mottled Frost-Burn Keloids",
                mob_loss=15,
                dex_loss=15
            )
            player.inflict_trauma("Agony of Extremes", sanity_loss=15)

            return "confessional", (
                f"{RED_BLOOD}[OVERPRESSURE DISCHARGE!]{RESET} You hesitate in the center!\n\n"
                f"The overpressure safety fails! Rupture discs on both lines blow out simultaneously! "
                f"A shockwave of sub-zero nitrogen mist and boiling steam slams into your body from both flanks (-28% HP)! "
                f"Your clothes freeze on one side and melt on the other! Screaming in sheer agony, you throw yourself "
                f"against the console, violently kicking both valves open to stop the discharge!\n\n"
                f"The door blows open from the pressure wave, ejecting you into the next room."
            )

        return None, f"{GRAY_SLATE}The valves remain closed. The pressure needle climbs into the red.{RESET}"


class ConfessionalRoom(Room):
    """The psychological interrogation by Dr. Locke."""

    def __init__(self):
        super().__init__("confessional", "The Confessional Crucible", "Act III: The Crucible")
        self.question_stage = 1

    def render(self, player: Player) -> Tuple[str, List[Tuple[str, str]]]:
        if self.question_stage == 1:
            text = (
                f"You step into an eerie octagonal chamber lined with brass phonograph horns suspended like withered flowers.\n\n"
                f"In the center of the room sits a single cast-iron stool under a cold spotlight. Behind you, the iron door slams shut.\n\n"
                f"Dr. Gabriel Locke's voice speaks through the phonograph horns, calm, measured, terrifyingly intimate:\n\n"
                f"{GRAY_LIGHT}\"You have survived bone, blade, wire, and fire. You have shed blood and skin. "
                f"But the deepest cancer in modern man is not physical—it is the lie you tell yourself to sleep at night.\n\n"
                f"Let us perform an autopsy on your conscience.\n\n"
                f"QUESTION I: Why did you flee the scene of the hit-and-run on Miller Road three years ago? "
                f"Did you run in animal panic... or did you simply value your freedom more than the human life dying in the rain?\"{RESET}"
            )
            choices = [
                ("1", "\"I was terrified. I panicked like an animal, and I have hated myself every second since.\""),
                ("2", "\"It was an accident! It wasn't entirely my fault—the rain was blinding and they stepped into the road!\""),
                ("3", "\"I ran because I was selfish. I cared more about my own skin than theirs. That is the ugly truth.\"")
            ]
            return text, choices

        elif self.question_stage == 2:
            if "caleb_mutilated" in player.flags:
                q2_text = (
                    f"\"QUESTION II: At the Scales of Atonement, you picked up the saw and took the leg of an unconscious man. "
                    f"Do you admit you are a butcher who feeds on the weak to survive, or will you hide behind the excuse of necessity?\""
                )
                choices = [
                    ("1", "\"I had no choice. You put the blade in my hand—you made me do it!\""),
                    ("2", "\"I am a coward. I butchered a helpless man because I was terrified to bleed. I am a monster.\""),
                    ("3", "\"In a world of teeth, it was his flesh or mine. I chose survival without apology.\"")
                ]
            else:
                q2_text = (
                    f"\"QUESTION II: At the Scales, you chose to carve into your own flesh and sear your own palms rather than harm Caleb. "
                    f"Was that true compassion... or the pathetic vanity of an ego that wanted to play the holy martyr?\""
                )
                choices = [
                    ("1", "\"I did it because another human life had value, even if mine was forfeit.\""),
                    ("2", "\"I did it because I couldn't bear the thought of living with the guilt of murder.\""),
                    ("3", "\"I did it to prove you wrong. To prove that cruelty is not the only law.\"")
                ]

            text = (
                f"Dr. Locke's voice hums through the brass horns:\n\n"
                f"{GRAY_LIGHT}{q2_text}{RESET}"
            )
            return text, choices

        else:
            text = (
                f"Dr. Locke's voice drops to a near whisper:\n\n"
                f"{GRAY_LIGHT}\"FINAL QUESTION: Look at what remains of your body. Look at your missing blood, your scars, your ruined hands. "
                f"After everything you have suffered, taken, and shed... do you truly believe you deserve to walk out of this house alive?\"{RESET}"
            )
            choices = [
                ("1", "\"I don't know if I deserve it. But I fought for every inch of breath, and I will not lay down and die.\""),
                ("2", "\"Yes! I paid your insane toll, I endured your sadistic games, and I am entitled to my life!\""),
                ("3", "\"No one 'deserves' to live. Survival is taken with bare teeth. Open the door.\"")
            ]
            return text, choices

    def handle_choice(self, choice: str, player: Player) -> Tuple[Optional[str], str]:
        c = choice.strip()

        if self.question_stage == 1:
            if c in ["1", "3"]:
                self.question_stage = 2
                return None, (
                    f"{WHITE_BONE}[HONEST CONTRITION LOGGED]{RESET}\n"
                    f"Locke pauses. \"An incision into the ego. Admitting the cowardice is the first step toward excision.\""
                )
            else:
                # Denial / Excuses
                player.flags.add("lied_at_confession")
                self.question_stage = 2
                return None, (
                    f"{RED_CRIMSON}[DECEIT DETECTED]{RESET}\n"
                    f"Locke tsks softly. \"Still making excuses. Still deflecting the blame onto the rain. How pathetic.\""
                )

        elif self.question_stage == 2:
            if c in ["2", "1" if "self_sacrificed" in player.flags else "2", "3"]:
                self.question_stage = 3
                return None, (
                    f"{WHITE_BONE}[PSYCHOLOGICAL PROFILE UPDATED]{RESET}\n"
                    f"Locke speaks: \"You understand the weight of your actions, even when they disgust you.\""
                )
            else:
                player.flags.add("lied_at_confession")
                self.question_stage = 3
                return None, (
                    f"{RED_CRIMSON}[DECEIT DETECTED]{RESET}\n"
                    f"Locke sighs. \"The tongue lies, but the scalpel never does.\""
                )

        else:
            # Final question
            if "lied_at_confession" in player.flags or c == "2":
                # Neurotoxin spray!
                player.flags.add("phantasm_poisoned")
                player.sanity = max(10, player.sanity - 30)
                player.hallucinating = True
                return "hallucinatory_corridor", (
                    f"{RED_BLOOD}[HYPOCRISY PUNISHED: PHANTASM-9 DISCHARGE]{RESET}\n\n"
                    f"Locke's voice hardens with disgust: \"You learned nothing. You traded flesh, but kept your rotting delusion.\"\n\n"
                    f"Overhead brass nozzles HISS violently! A violet-tinted mist—{RED_CRIMSON}Phantasm-9 Neurotoxin{RESET}—floods the room!\n"
                    f"You cough, breathing the sweet, hallucinogenic vapor. The room begins to melt. "
                    f"The floor ripples like liquid blood. The walls whisper with the voices of everyone you ever hurt.\n\n"
                    f"You stumble blindly into the distorted darkness of the Hallucinatory Corridor! (-30% Sanity)"
                )
            else:
                return "engine_room", (
                    f"{GREEN_ACID}[ABSOLUTION THROUGH AGONY]{RESET}\n\n"
                    f"Locke's voice carries a strange, haunting warmth:\n"
                    f"\"Clarity. The cancer of your self-deceit has been excised. You see yourself without vanity, "
                    f"without illusion. That is the only state in which a human being is truly alive.\"\n\n"
                    f"A massive hydraulic deadbolt clanks open. The far archway slides aside, revealing the colossal, "
                    f"churning clockwork gears of {RED_BLOOD}Act IV: The Engine Room{RESET}."
                )

        return None, f"{GRAY_SLATE}The horns wait for your truth.{RESET}"


class HallucinatoryCorridor(Room):
    """The mind-bending neurotoxin nightmare."""

    def __init__(self):
        super().__init__("hallucinatory_corridor", "The Corridor of Hallucinations", "Act III: The Crucible")

    def render(self, player: Player) -> Tuple[str, List[Tuple[str, str]]]:
        text = (
            f"{RED_BLOOD}{ITALIC}REALITY IS UNRAVELING.{RESET}\n\n"
            f"The Phantasm-9 neurotoxin has hijacked your cerebral cortex. "
            f"The walls pulse like living, weeping internal organs. Crimson blood seeps upward into the ceiling vents.\n\n"
            f"Walking beside you are phantom figures: Caleb with hollow eyes, Dr. Locke holding a silver scalpel, "
            f"the victim from the car crash staring with broken teeth.\n\n"
            f"Before you stand three doors, warped and shimmering in surreal nightmare colors:\n\n"
            f"{RED_CRIMSON}[DOOR 1 - BLOOD RED]{RESET}: \"Slit your own throat with your scalpel to wake up from the dream.\"\n"
            f"{BLUE_STEEL}[DOOR 2 - COLD IRON]{RESET}: \"Focus on the searing physical pain of your real scars to ground yourself in reality.\"\n"
            f"{WHITE_BONE}[DOOR 3 - PALE IVORY]{RESET}: \"Follow the weeping voice of Caleb into the dark vent.\""
        )

        choices = [
            ("1", "Slit your own throat with your scalpel to end the hallucination"),
            ("2", "Grip your scarred, mutilated flesh and focus on the real physical pain to break the illusion"),
            ("3", "Follow Caleb's weeping voice into the dark floor vent")
        ]
        return text, choices

    def handle_choice(self, choice: str, player: Player) -> Tuple[Optional[str], str]:
        c = choice.strip()

        if c == "1":
            # Lethal illusion
            player.take_damage(60, blood_loss=50, pain="Fatal Carotid Severance")
            return "DEATH", (
                f"{RED_BLOOD}The neurotoxin deceives you to the end.{RESET} You press your surgical scalpel to your own throat "
                f"and draw the carbon steel blade deep across your carotid artery. Warm blood gushes across your chest. "
                f"As your consciousness fades into eternal cold, Locke's voice whispers from the dark: "
                f"\"A mind that cannot distinguish truth from delusion is already dead.\""
            )

        elif c == "2":
            # Grounding in pain
            player.sanity = min(100, player.sanity + 20)
            player.hallucinating = False
            return "engine_room", (
                f"{GREEN_ACID}[ANCHORED IN REAL PAIN]{RESET}\n\n"
                f"You drop to your knees. You dig your fingernails directly into your existing open wounds and burns!\n\n"
                f"Real, blistering, biological agony shoots through your nervous system like a lightning strike! "
                f"The visceral reality of your flesh burns through the neurotoxin's mist! "
                f"The bleeding walls dissolve back into cold, rusted iron plates. The phantom voices vanish.\n\n"
                f"You rise, lungs clearing, anchored in the truth of your scars (+20% Sanity).\n"
                f"You step through the iron doorway into {RED_BLOOD}Act IV: The Engine Room{RESET}!"
            )

        elif c == "3":
            # Vent trap
            player.take_damage(25, pain="Rusted Gear Punctures")
            player.inflict_wound("Punctured Thigh & Torn Ligaments", mob_loss=15)
            player.hallucinating = False
            return "engine_room", (
                f"You crawl into the dark floor vent following the phantom voice.\n\n"
                f"The floor gives way! You drop eight feet into an iron drainage chute lined with rusted machinery teeth! "
                f"Gears bite deep into your thigh and hip before you manage to kick free and tumble out onto the engine floor (-25% HP).\n\n"
                f"The shock shakes the neurotoxin from your mind."
            )

        return None, f"{GRAY_SLATE}The hallucinatory walls ripple with whispers.{RESET}"
