"""
Act II: The Mechanism
Rooms: Pendulum Theatre, Catwalk of Vitriol, Optic Labyrinth.
"""

from typing import Tuple, List, Optional
from blade.rooms.base import Room
from blade.player import Player
from blade.terminal import (
    RESET, BOLD, ITALIC, RED_BLOOD, RED_CRIMSON, RED_RUST, RED_DARK,
    YELLOW_AMBER, YELLOW_WARNING, BLUE_STEEL, GRAY_SLATE, GRAY_LIGHT,
    WHITE_BONE, GREEN_ACID, GREEN_TOXIC, PENDULUM_ART
)


class PendulumTheatreRoom(Room):
    """The oscillating pendulum execution gurney."""

    def __init__(self):
        super().__init__("pendulum_theatre", "The Pendulum Theatre", "Act II: The Mechanism")

    def render(self, player: Player) -> Tuple[str, List[Tuple[str, str]]]:
        text = (
            f"{PENDULUM_ART}\n"
            f"You step into a darkened anatomical amphitheater. The instant your weight touches the center platform, "
            f"heavy forged steel shackles {RED_CRIMSON}[CLAP-SHUT!]{RESET} around your wrists, ankles, and neck, "
            f"slamming you flat onto a cold cast-iron operating gurney!\n\n"
            f"High in the darkness of the rafters, a massive {RED_BLOOD}6-foot curved steel crescent scythe{RESET} swings into motion:\n"
            f"{BOLD}{GRAY_SLATE}[SWOOSH... SWOOSH... SWOOSH...]{RESET}\n\n"
            f"Every oscillation, an overhead clockwork gear reels down two inches, descending directly over your sternum!\n\n"
            f"Flanking your pinned hands are two steel cylindrical tubes. Inside each tube, eight inches down, "
            f"is a red copper contact switch buried beneath {WHITE_BONE}four inches of jagged crushed bottle glass{RESET} "
            f"and wired to humming electrical contacts.\n\n"
            f"Dr. Locke's voice echoes from an overhead horn:\n"
            f"{GRAY_LIGHT}\"To disengage the gurney shackles, you must depress both contact buttons simultaneously and hold them down "
            f"for fifteen seconds against the glass and voltage. Suffer the glass, or be cleaved in two.\"{RESET}"
        )

        choices = [
            ("1", "Plunge both hands into the glass-filled tubes and press the buttons down with all your might"),
            ("2", "Thrash with all your strength and attempt to slip your wrists out of the forged iron shackles"),
            ("3", "Attempt to kick the pendulum drive cable housing with your foot to jam the gears")
        ]
        return text, choices

    def handle_choice(self, choice: str, player: Player) -> Tuple[Optional[str], str]:
        c = choice.strip()

        if c == "1":
            # Endure glass and voltage
            player.take_damage(22, blood_loss=10, pain="Searing Agony")
            player.inflict_wound(
                "Shredded Thenar Muscles & Deep Glass Lacerations on Both Palms",
                permanent_scar="Glass-Shredded Tendons & Voltage Burns",
                dex_loss=20,
                bleed_severity=1
            )
            player.inflict_trauma("Memory of the Descending Blade", sanity_loss=12)

            return "chemical_basin", (
                f"{RED_BLOOD}[THE CRUCIBLE OF GLASS]{RESET}\n\n"
                f"You force your trembling hands down into the steel cylinders. Razor-sharp bottle glass bites deep into "
                f"your palms, fingertips, and knuckles. You press your shredded palms down onto the copper buttons.\n\n"
                f"120 VOLTS OF ELECTRIC CURRENT COURSES THROUGH YOUR FOREARMS!\n"
                f"Your teeth clatter violently. Above you, the pendulum scythe drops with a horrifying whistle: "
                f"{RED_BLOOD}[SWOOSH!]{RESET} The whistling blade descends to three inches... two inches... "
                f"the wind of the razor edge parts the hair on your chest!\n\n"
                f"You scream into the darkness, refusing to let go. Tears, saliva, and sweat blind you.\n\n"
                f"At the final second: {GREEN_ACID}[PNEUMATIC RELEASE!]{RESET}\n"
                f"The shackles snap open! You throw your body sideways off the gurney, crashing onto the cold stone floor "
                f"just as the crescent blade slices through the empty leather mattress, splitting the steel bed in two!\n\n"
                f"You pull your hands from the tubes, dripping with blood and embedded with glass shards. "
                f"(-22% HP, -10% Blood, Level 1 Bleed, Permanent -20 Dexterity)"
            )

        elif c == "2":
            # Squirm in panic
            player.take_damage(36, blood_loss=22, pain="Pectoral Laceration")
            player.inflict_wound(
                "Deep Transverse Pectoral Crescent Laceration",
                permanent_scar="Crescent Chest Scar Across Sternum",
                mob_loss=10,
                dex_loss=15,
                bleed_severity=2
            )
            player.inflict_trauma("Terror of the Blade", sanity_loss=20)

            return "chemical_basin", (
                f"Panic overwhelms your reason. You thrash against the forged shackles, scraping your wrists raw to the bone.\n\n"
                f"The steel does not budge! The pendulum descends: {RED_BLOOD}[SWOOSH... SWOOSH!]{RESET}\n"
                f"The razor edge hits your chest! The scythe carves a horrific five-inch trench through your denim, adipose tissue, "
                f"and pectoral muscle, scoring the surface of your sternum! Blood erupts across your face!\n\n"
                f"Confronted with imminent decapitation on the next swing, you slam your hands blindly into the glass tubes! "
                f"The voltage shocks your heart, the release triggers, and you tumble onto the floor in a spray of arterial blood!\n\n"
                f"You stagger forward, clutching your cleaved chest. (-36% HP, -22% Blood, Level 2 Bleed, -15 Dexterity)"
            )

        elif c == "3":
            # Kick cable
            if player.mobility >= 70:
                player.take_damage(14, pain="Twisted Ankle")
                return None, (
                    f"You arch your torso and drive the heel of your boot into the overhead drive chain! "
                    f"The chain shudders with a metallic screech, skipping three teeth! The blade's descent stalls for a few seconds, "
                    f"but the iron links groan and resume their descent. You must decide!"
                )
            else:
                player.take_damage(20, pain="Fractured Metatarsal")
                player.inflict_wound("Fractured Right Metatarsal", mob_loss=20)
                return None, (
                    f"Your weakened leg kicks out, but strikes the reinforced steel housing! "
                    f"Bone snaps in your foot with a sickening crunch (-20% HP, -20% Mobility). "
                    f"The pendulum blade swings lower, now only four inches from your throat!"
                )

        return None, f"{GRAY_SLATE}The pendulum swings lower: SWOOSH... SWOOSH... Inches remain.{RESET}"


class ChemicalBasinRoom(Room):
    """The catwalk over boiling sulfuric acid."""

    def __init__(self):
        super().__init__("chemical_basin", "The Catwalk of Vitriol", "Act II: The Mechanism")

    def render(self, player: Player) -> Tuple[str, List[Tuple[str, str]]]:
        caleb_event = ""
        if "caleb_mutilated" in player.flags:
            caleb_event = (
                f"\n{RED_CRIMSON}On the wall beside the abyss, written in dripping smeared blood, is Caleb's handwriting: "
                f"\"YOU BUTCHERED ME TO SAVE YOURSELF. I HOPE THE ACID BURNS YOU SLOW.\"{RESET}"
            )
        elif "self_sacrificed" in player.flags or "hands_burned" in player.flags:
            caleb_event = (
                f"\n{GREEN_ACID}On the upper gantry across the chasm, you see Caleb! Bandaged and limping, he managed to escape "
                f"his unlocked cage and is waiting near the manual bridge winch!{RESET}"
            )

        text = (
            f"You stagger onto a narrow rusted steel catwalk suspended 30 feet above a churning reservoir of "
            f"{GREEN_ACID}concentrated sulfuric acid and formalin{RESET}.\n\n"
            f"Thick, yellow acidic fumes rise from the vat, burning your throat and stinging your eyes. "
            f"Directly in front of you, the middle 25-foot span of the catwalk has been retracted into the iron wall.\n\n"
            f"Suspended eight feet overhead is a single corroded steel steam pipe spanning the void.\n\n"
            f"On your side of the chasm is an emergency hydraulic override valve inside an inspection port, "
            f"where {YELLOW_WARNING}superheated corrosive steam{RESET} vents violently every six seconds.{caleb_event}"
        )

        choices = [
            ("1", "Jump and shimmy hand-over-hand across the overhead corroded steam pipe"),
            ("2", "Reach your arm deep into the scalding inspection port to crank the manual hydraulic valve"),
            ("3", "Call out to the other side and search for a rope or alternate anchor")
        ]
        return text, choices

    def handle_choice(self, choice: str, player: Player) -> Tuple[Optional[str], str]:
        c = choice.strip()

        if c == "1":
            # Shimmy pipe
            if player.dexterity >= 55 and player.mobility >= 50:
                player.take_damage(8, pain="Acid Fume Burns")
                return "optic_labyrinth", (
                    f"You leap upward, gripping the hot, rusted steam pipe with both hands.\n\n"
                    f"Acid fumes rise from the boiling pit below, blistering your skin and choking your lungs (-8% HP). "
                    f"Your muscles scream with exhaustion as you shimmy hand-over-hand across the 25-foot abyss.\n\n"
                    f"Halfway across, a rust flake peels from the pipe—your grip slips, but you lock your forearms in place! "
                    f"With a final surge of willpower, you swing your legs up and drop safely onto the far catwalk!"
                )
            else:
                player.take_damage(26, pain="Acid Vapor & Muscle Tear")
                player.inflict_wound(
                    "Torn Rotator Cuff & Acid Vapor Blisters",
                    permanent_scar="Caustic Chemical Blister Scarring",
                    mob_loss=15,
                    dex_loss=15
                )
                player.inflict_trauma("Near-Fall Acid Terror", sanity_loss=15)
                return "optic_labyrinth", (
                    f"{RED_BLOOD}[SLIP!]{RESET} Your mutilated, glass-shredded hands cannot maintain grip on the slick pipe!\n\n"
                    f"Over the center of the boiling acid pit, your fingers give way! You plummet downward—"
                    f"In sheer panic, you throw your arm out and catch a lower steel girder! The shock violently dislocates "
                    f"your rotator cuff with a sickening pop! The acid surface churns mere inches below your dangling boots, "
                    f"splashing corrosive drops that dissolve your denim and burn deep into your skin (-26% HP)!\n\n"
                    f"Sobbing in pain and terror, you claw your way up the iron ribbing and collapse onto the far platform."
                )

        elif c == "2":
            # Reach into steam vent
            player.take_damage(20, pain="Scalded Flesh")
            player.inflict_wound(
                "Second-Degree Steam & Chemical Scald across Right Forearm",
                permanent_scar="Mottled Acid-Scald Scarring on Arm",
                dex_loss=15
            )
            return "optic_labyrinth", (
                f"{YELLOW_WARNING}[THE SCALDING CRANK]{RESET}\n\n"
                f"You time the venting steam, thrust your right arm into the inspection port, and seize the brass wheel.\n\n"
                f"A sudden jet of 90°C acidic steam blasts across your arm! You scream as blisters instantly balloon and rupture "
                f"across your forearm (-20% HP). You refuse to let go, violently wrenching the wheel three full rotations!\n\n"
                f"With a heavy mechanical groan, the steel catwalk sections extend from the walls, locking into a solid bridge. "
                f"You cradle your smoking, scalded arm and cross safely into the next portal."
            )

        elif c == "3":
            # Caleb assistance or search
            if "self_sacrificed" in player.flags or "hands_burned" in player.flags:
                return "optic_labyrinth", (
                    f"{GREEN_TOXIC}[ALLIANCE BOUGHT IN BLOOD]{RESET}\n\n"
                    f"Caleb recognizes you! \"You... you spared me at the scales! Hold on!\"\n\n"
                    f"Caleb throws his weight against the heavy gantry counterweight winch. With a metallic screech, an overhead "
                    f"maintenance cable swings toward you with an iron harness hook! You latch the hook under your belt, "
                    f"and Caleb pulls the release, swinging you safely across the boiling pit of acid!\n\n"
                    f"You land beside Caleb. He looks at your mutilated body with profound gratitude and horror. "
                    f"\"We can make it out of here. Together.\""
                )
            else:
                return None, (
                    f"You call out, but your voice is swallowed by the hiss of boiling acid. "
                    f"Only silence and the stench of sulfur reply. No one is coming to save you."
                )

        return None, f"{GRAY_SLATE}The acid churns below. The void must be crossed.{RESET}"


class OpticLabyrinthRoom(Room):
    """The retinal scanner and needle-filled formalin dummy."""

    def __init__(self):
        super().__init__("optic_labyrinth", "The Optic Labyrinth", "Act II: The Mechanism")

    def render(self, player: Player) -> Tuple[str, List[Tuple[str, str]]]:
        text = (
            f"You enter a circular reinforced vault lined with cold riveted steel plates.\n\n"
            f"The exit bulkhead is sealed by an electronic magnetic seal wired to a state-of-the-art "
            f"{RED_CRIMSON}retinal scanning aperture{RESET}. A phosphor screen reads:\n"
            f"{WHITE_BONE}[BIOMETRIC SCAN REQUIRED: DR. GABRIEL LOCKE — OCULAR SIGNATURE]{RESET}\n\n"
            f"In the center of the room stands a clear acrylic cylinder filled with yellow formalin. "
            f"Suspended in the fluid is a lifelike anatomical mannequin. In its left socket sits a preserved "
            f"{YELLOW_AMBER}Glass Prosthetic Eye{RESET} hand-painted with Dr. Locke's registered retinal pattern.\n\n"
            f"However, the cylinder's access sleeve is ringed with {RED_BLOOD}dozens of inward-facing surgical hypodermic needles{RESET} "
            f"and spring-loaded lancets. Reaching inside bare-handed will shred any limb that enters."
        )

        choices = [
            ("1", "Plunge your bare arm directly into the needle sleeve to extract the glass eye"),
            ("2", "Use your scalpel and copper wire as surgical tools to extract the eye without touching the needles"),
            ("3", "Press your own eye directly against the retinal scanner to attempt a forced override")
        ]
        return text, choices

    def handle_choice(self, choice: str, player: Player) -> Tuple[Optional[str], str]:
        c = choice.strip()

        if c == "1":
            # Bare hand into needle sleeve
            player.take_damage(18, blood_loss=6, pain="Pricked Agony")
            player.inflict_wound(
                "Multiple Hypodermic Punctures & Neurotoxin Contusion",
                dex_loss=15
            )
            player.add_item("formalin_eye", 1)

            return "nitrogen_kiln", (
                f"{RED_BLOOD}[THE NEEDLE SLEEVE]{RESET}\n\n"
                f"You thrust your bare arm down the narrow cylinder opening. Dozens of surgical hypodermic needles bite deep "
                f"into your forearm, wrist, and knuckles (-18% HP, -6% Blood)!\n\n"
                f"Residual neurotoxin coating the needle points burns through your veins like liquid fire. "
                f"Gritting your teeth against the spasms, your bloody fingers clamp around the {YELLOW_AMBER}Glass Prosthetic Eye{RESET} "
                f"and wrench it free from the mannequin's socket!\n\n"
                f"You present the glass eye to the scanner. A green laser traces the iris: {GREEN_ACID}[ACCESS GRANTED]{RESET}!\n"
                f"The magnetic vault door slides open into {RED_BLOOD}Act III: The Crucible{RESET}."
            )

        elif c == "2":
            # Tool extraction
            if "scalpel" in player.inventory and "copper_wire" in player.inventory:
                player.add_item("formalin_eye", 1)
                return "nitrogen_kiln", (
                    f"{GREEN_ACID}[SURGICAL EXTRACTION]{RESET}\n\n"
                    f"You fashion a snare from your {YELLOW_AMBER}copper wire{RESET} and guide it carefully down the sleeve, "
                    f"using the flat edge of your {YELLOW_AMBER}scalpel{RESET} to depress the inward-pointing needle tips.\n\n"
                    f"With millimeter precision, you slip the wire loop behind the glass eye and ease it out of the socket. "
                    f"You slide the preserved iris out of the cylinder without triggering a single lancet!\n\n"
                    f"You hold the prosthetic eye up to the scanner. The beam flashes green: {GREEN_ACID}[IDENTITY CONFIRMED]{RESET}!\n"
                    f"The vault unlatches, admitting you into {RED_BLOOD}Act III: The Crucible{RESET}."
                )
            else:
                player.take_damage(12, pain="Punctured Knuckles")
                player.add_item("formalin_eye", 1)
                return "nitrogen_kiln", (
                    f"Lacking the proper wire snare, you use what tools you have. You manage to extract the eye, "
                    f"but several spring lancets snap into your hand (-12% HP).\n\n"
                    f"You scan the eye, and the vault unlatches into Act III."
                )

        elif c == "3":
            # Scan own eye
            player.flags.add("monocular_vision")
            player.take_damage(28, blood_loss=15, pain="Blinding Agony")
            player.inflict_wound(
                "Enucleation of Right Eye by Scanner Needle",
                permanent_scar="Blinded Right Eye / Monocular Vision",
                per_loss=40,
                bleed_severity=1
            )
            player.inflict_trauma("Agony of the Blinding Needle", sanity_loss=25)

            return "nitrogen_kiln", (
                f"{RED_BLOOD}[THE TOLL OF THE EYE]{RESET}\n\n"
                f"In desperate madness, you press your own right eye directly against the rubber viewing shroud of the scanner.\n\n"
                f"The retinal beam fires crimson: {RED_CRIMSON}[UNAUTHORIZED OCULAR BIOMETRICS]{RESET}!\n\n"
                f"From the center of the optical lens, a four-inch surgical lancet needle {RED_BLOOD}[FIRES FORWARD!]{RESET}\n\n"
                f"THE NEEDLE DRIVES DIRECTLY INTO YOUR RIGHT PUPIL!\n"
                f"An explosion of white, blinding agony shatters your consciousness. Vitreous fluid and blood pour down your cheek "
                f"as the lens retracts the destroyed eye! You collapse to your knees, vomiting in shock, clutching the bloody void "
                f"in your right socket.\n\n"
                f"The terminal chimes softly:\n"
                f"{GRAY_LIGHT}[ANATOMICAL TRIBUTE LOGGED. THRESHOLD SATISFIED BY SACRIFICE.]{RESET}\n\n"
                f"The magnetic doors slide open. Your world is now halved into monocular darkness. "
                f"(-28% HP, -15% Blood, Level 1 Bleed, Permanent Monocular Vision / -40 Perception)"
            )

        return None, f"{GRAY_SLATE}The optical scanner hums, waiting for an eye.{RESET}"
