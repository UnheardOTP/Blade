"""
Prologue: The Awakening in the Iron Cistern.
"""

from typing import Tuple, List, Optional
from blade.rooms.base import Room
from blade.player import Player
from blade.audio_tapes import render_tape
from blade.terminal import (
    RESET, BOLD, ITALIC, RED_BLOOD, RED_CRIMSON, RED_RUST, RED_DARK,
    YELLOW_AMBER, YELLOW_WARNING, BLUE_STEEL, GRAY_SLATE, GRAY_LIGHT,
    WHITE_BONE, CISTERN_ART, box_text, GREEN_TOXIC, GREEN_ACID
)


class CisternWakeRoom(Room):
    """The initial awakening trap."""

    def __init__(self):
        super().__init__("cistern_wake", "The Iron Cistern", "Prologue: Awakening")
        self.winch_ticks = 0
        self.max_ticks = 3
        self.awaiting_code = False

    def render(self, player: Player) -> Tuple[str, List[Tuple[str, str]]]:
        if not self.visited:
            self.visited = True
            player.unlock_tape("tape_01")

        text = (
            f"{CISTERN_ART}\n"
            f"You gasp, coughing foul, coppery liquid as consciousness tears through your mind.\n\n"
            f"You are waist-deep in freezing, stagnant embalming fluid inside an iron drainage cistern. "
            f"A heavy forged iron collar is locked around your throat, welded to a tensioned steel chain.\n\n"
            f"Above you, an overhead industrial winch groans: {RED_CRIMSON}{BOLD}[CLACK... CLACK... CLACK...]{RESET}\n"
            f"Every rotation drags your neck four inches closer to a circular steel casing where "
            f"{RED_BLOOD}12-inch rotating serrated shredder blades{RESET} spin with a wet, ravenous hum.\n\n"
            f"To your right, bolted to the concrete lip, is a brass combination lock securing the winch's "
            f"power relay. An old tape player on a rusted bracket has just finished playing {YELLOW_AMBER}Tape #1{RESET}.\n\n"
            f"{GRAY_LIGHT}\"The code is the number of cranial nerves in the human body. "
            f"Or... dislocate your thumb, slip the cuff, and buy your life with immediate trauma.\"{RESET}"
        )

        choices = [
            ("1", "Input the 2-digit combination on the brass lock"),
            ("2", "Grip and forcefully dislocate your left thumb to slip the neck/wrist shackle"),
            ("3", "Thrash with all your strength and attempt to yank the winch bracket from the concrete"),
            ("4", "Submerge into the foul fluid to search the cistern floor for an anchor or tool")
        ]

        if self.awaiting_code:
            text += f"\n\n{YELLOW_WARNING}Enter the 2-digit number of human cranial nerves (or type 'cancel'):{RESET}"

        return text, choices

    def handle_choice(self, choice: str, player: Player) -> Tuple[Optional[str], str]:
        c = choice.strip().lower()

        # Code entry mode
        if self.awaiting_code:
            if c in ["12", "twelve"]:
                self.awaiting_code = False
                player.take_damage(5, pain="Singed Flesh")
                player.flags.add("solved_cranial_code")
                return "cistern_drain", (
                    f"{YELLOW_WARNING}[CLACK-CLICK!]{RESET} The brass tumblers align at {WHITE_BONE}12{RESET}!\n"
                    f"A burst of blue electrical sparks arcs across the casing, scorching your forearm (-5% HP).\n"
                    f"The winch motor cuts out with a dying whine! The electromagnetic neck collar unlatches, "
                    f"dropping you into the freezing pool. You scramble up the drainage ladder to safety!"
                )
            elif c == "cancel":
                self.awaiting_code = False
                return None, f"{GRAY_SLATE}You step back from the combination dial.{RESET}"
            else:
                self.awaiting_code = False
                self.winch_ticks += 1
                player.take_damage(12, blood_loss=5, pain="Throbbing Agony")
                if self.winch_ticks >= self.max_ticks:
                    return "DEATH", (
                        f"{RED_BLOOD}WRONG CODE!{RESET} The lock jams! The winch accelerates with a frantic screech! "
                        f"The chain drags your neck into the rotating shredder blades before you can scream. "
                        f"Steel teeth pulverize your cervical spine."
                    )
                return None, (
                    f"{RED_CRIMSON}[BUZZER]{RESET} Incorrect code! The tumblers seize! "
                    f"The winch jerks violently, dragging you another foot backward. "
                    f"The spinning teeth graze the back of your shoulder, slicing denim and flesh (-12% HP, -5% Blood)! "
                    f"The blades are now inches from your neck!"
                )

        if c == "1":
            self.awaiting_code = True
            return None, f"{YELLOW_AMBER}You grip the cold brass dials with trembling, fluid-soaked fingers.{RESET}"

        elif c == "2":
            # Dislocate thumb
            player.take_damage(18, blood_loss=8, pain="Excruciating Agony")
            player.inflict_wound(
                "Surgically Dislocated & Fractured Left Thumb",
                permanent_scar="Deformed Left Thenar Joint",
                dex_loss=25,
                bleed_severity=1
            )
            player.inflict_trauma("Memory of the Popping Joint", sanity_loss=10)
            player.flags.add("dislocated_thumb")

            return "cistern_drain", (
                f"{RED_BLOOD}[CRACK-POP!]{RESET} You clamp your right fist around your left thumb, grit your teeth until "
                f"enamel fractures, and wrench it savagely backward.\n\n"
                f"A sickening pop resonates through your skull as the joint violently dislocates. Agony explodes up your arm! "
                f"Tears and bile flood your throat as you compress the mangled, flayed hand into a grotesque wedge "
                f"and yank it out of the iron cuff just as the chain snaps taut against the shredder housing!\n\n"
                f"The collar slips from your head. You collapse coughing onto the drainage grating. "
                f"(-18% HP, -8% Blood, Level 1 Bleed, Permanent -25 Dexterity)"
            )

        elif c == "3":
            # Brute force
            self.winch_ticks += 1
            player.take_damage(25, blood_loss=10, pain="Choking Agony")
            player.inflict_wound("Crushed Laryngeal Cartilage", dex_loss=5, mob_loss=5)
            player.inflict_trauma("Near-Strangulation Terror", sanity_loss=15)

            if self.winch_ticks >= self.max_ticks:
                return "DEATH", (
                    f"{RED_BLOOD}The winch does not yield to animal panic.{RESET} The chain pulls taut with relentless torque, "
                    f"crushing your windpipe before dragging your skull backwards into the whirling steel teeth."
                )

            return None, (
                f"{RED_CRIMSON}You roar and yank with animal fury!{RESET} The concrete anchors do not budge a millimeter. "
                f"Instead, the steel collar bites ruthlessly into your throat, bruising your trachea and choking off air. "
                f"The winch motor gears down and pulls you another foot closer to the whirling blades! (-25% HP, -10% Blood)"
            )

        elif c == "4":
            # Submerge and search
            player.take_damage(8, pain="Stinging Eyes")
            player.inflict_wound("Formaldehyde Eye Irritation", per_loss=10)
            player.add_item("copper_wire", 1)

            return None, (
                f"You hold your breath and submerge beneath the burning, stagnant red liquid. "
                f"The chemicals sting your eyes ruthlessly (-10% Perception). "
                f"Your fingers scrape along the rusted floor, wrapping around a spool of {YELLOW_AMBER}copper wire{RESET}!\n"
                f"You burst to the surface gasping—the shredder blades are now inches from your hair!"
            )

        return None, f"{GRAY_SLATE}The winch continues to grind: CLACK... CLACK... Time is running out.{RESET}"


class CisternDrainRoom(Room):
    """The drainage anteroom with first aid and locker."""

    def __init__(self):
        super().__init__("cistern_drain", "The Drainage Conduit", "Prologue: Triage")
        self.looted_locker = False

    def render(self, player: Player) -> Tuple[str, List[Tuple[str, str]]]:
        text = (
            f"You drag yourself across the cold iron grating into a narrow, damp drainage tunnel.\n\n"
            f"The air is thick with ozone and copper. Above, a bare amber bulb swings in a wire cage. "
            f"On the wall hangs a cracked steel mirror smeared with dried rust.\n\n"
            f"Beside it stands an open stainless steel medical locker marked with a red cross: {WHITE_BONE}[TRIAGE]{RESET}.\n"
            f"At the far end of the corridor, a massive iron blast door is sealed with heavy pneumatic bolts. "
            f"A red phosphor monitor glows above the portal: {RED_CRIMSON}[PHASE I: THE FLENSING]{RESET}."
        )

        choices = [
            ("1", "Inspect the TRIAGE medical locker"),
            ("2", "Look into the cracked mirror on the wall"),
            ("3", "Approach the blast door and enter Act I: The Flensing")
        ]
        return text, choices

    def handle_choice(self, choice: str, player: Player) -> Tuple[Optional[str], str]:
        c = choice.strip()

        if c == "1":
            if not self.looted_locker:
                self.looted_locker = True
                player.add_item("tourniquet", 1)
                player.add_item("adrenaline_syringe", 1)
                return None, (
                    f"{GREEN_TOXIC}You open the TRIAGE locker.{RESET}\n"
                    f"Inside, arranged with psychotic neatness on sterile gauze, you find:\n"
                    f"• {YELLOW_AMBER}1x Elastic Tourniquet{RESET} (Use 'USE TOURNIQUET' if bleeding)\n"
                    f"• {YELLOW_AMBER}1x Epinephrine Auto-Injector{RESET} (Emergency adrenaline surge)\n\n"
                    f"You stow the supplies in your damp pockets."
                )
            else:
                return None, f"{GRAY_SLATE}The TRIAGE locker has already been emptied.{RESET}"

        elif c == "2":
            thumb_state = "mangled and swollen" if "dislocated_thumb" in player.flags else "pale and trembling"
            return None, (
                f"{GRAY_SLATE}You step toward the cracked mirror.{RESET}\n\n"
                f"Reflected in the tarnished glass is a face you barely recognize: sunken eyes, lips blue from "
                f"hypothermia, skin stained with red embalming dye. Your hands are {thumb_state}.\n\n"
                f"Carved into the drywall beside the mirror in jagged handwriting is a message:\n"
                f"{RED_DARK}{ITALIC}\"You have barely begun to shed your skin.\"{RESET}"
            )

        elif c == "3":
            return "razor_hallway", (
                f"You grab the heavy iron release lever on the blast door and haul downward.\n"
                f"Hissing hydraulic pistons depress with a mechanical sigh. The steel door slides upward into the ceiling, "
                f"revealing a long, dim hallway filled with crisscrossing shadows.\n"
                f"You step through into {RED_BLOOD}Act I: The Flensing{RESET}."
            )

        return None, f"{GRAY_SLATE}You stand in the cold conduit.{RESET}"
