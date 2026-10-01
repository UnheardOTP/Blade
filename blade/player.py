"""
Player state model, vitals, wounds, medical treatment, and psychological trauma.
"""

from typing import List, Dict, Set, Optional, Tuple
import random

from blade.terminal import (
    RESET, BOLD, DIM, ITALIC, RED_BLOOD, RED_CRIMSON, RED_RUST, RED_DARK,
    YELLOW_AMBER, YELLOW_WARNING, GREEN_ACID, GREEN_TOXIC, BLUE_FROST, BLUE_STEEL,
    GRAY_ASH, GRAY_LIGHT, GRAY_SLATE, GRAY_DIM, WHITE_BONE, meter_bar,
    corrupt_glitch, box_text, BODY_OUTLINE
)
from blade.items import ITEMS


class Player:
    """Manages the player's physiological and psychological condition."""

    def __init__(self, name: str = "Subject 7"):
        self.name: str = name
        self.hp: int = 100
        self.max_hp: int = 100

        self.blood: int = 100
        self.max_blood: int = 100
        self.bleeding: int = 0  # 0=none, 1=minor (-2%), 2=arterial (-5%), 3=catastrophic (-10%)

        self.sanity: int = 100
        self.max_sanity: int = 100

        self.mobility: int = 100      # Leg/foot integrity
        self.dexterity: int = 100     # Hand/finger precision
        self.perception: int = 100    # Eyesight/hearing

        self.pain: str = "None"
        self.wounds: List[str] = []
        self.scars_physical: List[str] = []
        self.scars_mental: List[str] = []

        self.inventory: Dict[str, int] = {
            "tourniquet": 1,
            "scalpel": 1,
            "lighter": 1,
            "cassette_player": 1
        }
        self.tapes: List[str] = []
        self.flags: Set[str] = set()

        self.text_speed: str = "normal"  # "normal", "fast", "instant"
        self.adrenaline_active: bool = False
        self.hallucinating: bool = False

    def is_alive(self) -> bool:
        return self.hp > 0 and self.blood > 10 and self.sanity > 0

    def get_death_reason(self) -> str:
        if self.blood <= 10:
            return (
                "HYPOVOLEMIC SHOCK (EXSANGUINATION)\n"
                "Your heart fluttered erratically before running dry. Cold darkness swallowed you "
                "as your blood soaked into Dr. Locke's drainage grates. You died empty."
            )
        if self.sanity <= 0:
            return (
                "IRREVERSIBLE PSYCHOTIC DISSOCIATION\n"
                "Your mind shattered under the weight of agony and terror. You tore at your own flesh "
                "screaming at phantom voices until your heart seized. The house absorbed your madness."
            )
        if self.hp <= 0:
            return (
                "FATAL TRAUMATIC CARDIAC ARREST\n"
                "Your physical vessel could endure no further mutilation. Pain overload triggered a massive "
                "vagal collapse. You collapsed into the gears, discarded."
            )
        return "UNKNOWN BIOLOGICAL CESSATION"

    def take_damage(self, hp_loss: int, blood_loss: int = 0, pain: Optional[str] = None):
        """Reduces HP and Blood, updates pain status."""
        self.hp = max(0, self.hp - hp_loss)
        if blood_loss > 0:
            self.blood = max(0, self.blood - blood_loss)
        if pain:
            self.pain = pain
        elif hp_loss > 30:
            self.pain = "Searing Agony"
        elif hp_loss > 15:
            self.pain = "Throbbing Agony"
        elif hp_loss > 5:
            self.pain = "Dull Ache"

    def inflict_wound(
        self,
        wound_desc: str,
        permanent_scar: Optional[str] = None,
        dex_loss: int = 0,
        mob_loss: int = 0,
        per_loss: int = 0,
        bleed_severity: int = 0
    ):
        """Adds a physical wound and permanent alterations."""
        if wound_desc not in self.wounds:
            self.wounds.append(wound_desc)
        if permanent_scar and permanent_scar not in self.scars_physical:
            self.scars_physical.append(permanent_scar)

        self.dexterity = max(10, self.dexterity - dex_loss)
        self.mobility = max(10, self.mobility - mob_loss)
        self.perception = max(10, self.perception - per_loss)

        if bleed_severity > self.bleeding:
            self.bleeding = bleed_severity

    def inflict_trauma(self, mental_scar: str, sanity_loss: int = 0):
        """Adds psychological scars and reduces sanity."""
        if mental_scar not in self.scars_mental:
            self.scars_mental.append(mental_scar)
        self.sanity = max(0, self.sanity - sanity_loss)
        if self.sanity < 40:
            self.hallucinating = True

    def tick_turn(self) -> List[str]:
        """Processes turn-based physiological changes (bleeding, hallucinations, etc.)."""
        events = []

        # Bleeding progression
        if self.bleeding > 0:
            loss_map = {1: 2, 2: 5, 3: 10}
            loss = loss_map.get(self.bleeding, 3)
            self.blood = max(0, self.blood - loss)
            severity_str = {1: "minor trickle", 2: "pulsing arterial flow", 3: "catastrophic hemorrhage"}[self.bleeding]
            events.append(f"{RED_BLOOD}[BLEEDING] A {severity_str} drains your warmth (-{loss}% Blood).{RESET}")

            if self.blood <= 30 and self.blood > 10:
                events.append(f"{YELLOW_WARNING}[HYPOVOLEMIA] Your vision tunnels into gray static. Your pulse thumps weakly.{RESET}")

        # Sanity degradation
        if self.hallucinating or self.sanity < 35:
            if random.random() < 0.4:
                whispers = [
                    "A voice behind the wallpaper whispers your real name.",
                    "The floor beneath your feet feels wet and spongy, like lung tissue.",
                    "You feel invisible needles piercing the back of your neck.",
                    "You catch a glimpse of yourself in a dark pipe—your eyes are hollow holes."
                ]
                events.append(f"{ITALIC}{RED_CRIMSON}[HALLUCINATION] {random.choice(whispers)}{RESET}")

        # Adrenaline fade
        if self.adrenaline_active:
            if random.random() < 0.3:
                self.adrenaline_active = False
                events.append(f"{GRAY_SLATE}[EPINEPHRINE CRASH] The adrenaline surge drains away, leaving your limbs trembling with raw exhaustion.{RESET}")

        return events

    def apply_bandage(self) -> Tuple[bool, str]:
        """Stanches bleeding with tourniquet/bandage."""
        if self.inventory.get("tourniquet", 0) <= 0:
            return False, f"{GRAY_SLATE}You have no tourniquet or clean bandages left in your inventory.{RESET}"

        if self.bleeding == 0:
            return False, f"{GRAY_SLATE}You have no active arterial bleeding to bind right now.{RESET}"

        self.inventory["tourniquet"] -= 1
        if self.inventory["tourniquet"] <= 0:
            del self.inventory["tourniquet"]

        old_bleed = self.bleeding
        self.bleeding = 0
        self.hp = min(100, self.hp + 5)
        return True, (
            f"{GREEN_TOXIC}[TREATMENT] You bind the tourniquet tightly above the lacerations. "
            f"The arterial spray slows, clots, and stops. (+5% HP, Bleeding Halted){RESET}"
        )

    def cauterize_wound(self) -> Tuple[bool, str]:
        """Burns an open wound shut with the lighter flame."""
        if self.inventory.get("lighter", 0) <= 0:
            return False, f"{GRAY_SLATE}You do not have a flame source to cauterize wounds.{RESET}"

        if self.bleeding == 0:
            return False, f"{GRAY_SLATE}You do not have an active hemorrhage requiring extreme cauterization.{RESET}"

        self.bleeding = 0
        self.hp = max(1, self.hp - 8)
        self.sanity = max(5, self.sanity - 8)
        self.pain = "Searing Agony"
        self.inflict_wound(
            "Charred Third-Degree Cauterization Burn",
            permanent_scar="Charred Flesh of the Self-Brand",
            dex_loss=5
        )
        return True, (
            f"{RED_BLOOD}[CAUTERIZATION] You click the lighter flame and press the red-hot metal casing directly "
            f"into the torn arterial flesh. The hiss of boiling blood and stench of burning adipose tissue "
            f"nearly blacks you out. The bleeding is sealed shut, but the searing agony is absolute. (-8% HP, -8% Sanity, Bleeding Halted){RESET}"
        )

    def use_adrenaline(self) -> Tuple[bool, str]:
        """Injects epinephrine syringe."""
        if self.inventory.get("adrenaline_syringe", 0) <= 0:
            return False, f"{GRAY_SLATE}You have no epinephrine auto-injectors remaining.{RESET}"

        self.inventory["adrenaline_syringe"] -= 1
        if self.inventory["adrenaline_syringe"] <= 0:
            del self.inventory["adrenaline_syringe"]

        self.adrenaline_active = True
        self.hp = min(100, self.hp + 25)
        self.mobility = max(self.mobility, 85)
        self.sanity = max(5, self.sanity - 12)
        self.pain = "Numb Vibrations"

        return True, (
            f"{YELLOW_WARNING}[EPINEPHRINE] You slam the auto-injector needle through your denim into your thigh. "
            f"A violent chemical fire surges into your bloodstream! Your heart hammers at 180 BPM, "
            f"pain receptors short-circuit into numbness, and your crippled legs lock with rigid synthetic vigor. (+25% HP, Mobility Restored, -12% Sanity){RESET}"
        )

    def apply_splint(self) -> Tuple[bool, str]:
        """Uses bone splint to brace broken limbs."""
        if self.inventory.get("bone_splint", 0) <= 0:
            return False, f"{GRAY_SLATE}You have no splints available.{RESET}"

        self.inventory["bone_splint"] -= 1
        if self.inventory["bone_splint"] <= 0:
            del self.inventory["bone_splint"]

        self.mobility = min(100, self.mobility + 30)
        return True, (
            f"{GREEN_TOXIC}[BONE SPLINT] You bind the rigid bone shard against your fractured joint with gauze. "
            f"The grinding agony subsides into a stable throb. (+30% Mobility){RESET}"
        )

    def add_item(self, item_id: str, count: int = 1):
        self.inventory[item_id] = self.inventory.get(item_id, 0) + count

    def remove_item(self, item_id: str, count: int = 1) -> bool:
        if self.inventory.get(item_id, 0) >= count:
            self.inventory[item_id] -= count
            if self.inventory[item_id] <= 0:
                del self.inventory[item_id]
            return True
        return False

    def unlock_tape(self, tape_id: str):
        if tape_id not in self.tapes:
            self.tapes.append(tape_id)

    def status_summary(self) -> str:
        """One-line status HUD string."""
        bleed_tag = f"{RED_BLOOD}[BLEEDING: L{self.bleeding}]{RESET}" if self.bleeding > 0 else f"{GRAY_SLATE}[BLEEDING: NONE]{RESET}"
        return (
            f"{WHITE_BONE}[HP: {meter_bar(self.hp, 100, 8, RED_BLOOD)}] "
            f"[BLOOD: {meter_bar(self.blood, 100, 8, RED_CRIMSON)}] "
            f"[SANITY: {meter_bar(self.sanity, 100, 8, BLUE_STEEL)}] "
            f"{bleed_tag} "
            f"[PAIN: {YELLOW_AMBER}{self.pain}{RESET}]"
        )

    def inspect_status(self) -> str:
        """Returns the full anatomical diagnosis report."""
        lines = []
        lines.append(f"{RED_RUST}═════════════════════════════════════════════════════════════════════════{RESET}")
        lines.append(f"{WHITE_BONE}{BOLD}        CLINICAL ANATOMICAL DISSECTION & PSYCHOLOGICAL DIAGNOSIS{RESET}")
        lines.append(f"{GRAY_SLATE}        Subject Designation: {WHITE_BONE}{self.name}{GRAY_SLATE} | Overseer: Dr. Gabriel Locke{RESET}")
        lines.append(f"{RED_RUST}═════════════════════════════════════════════════════════════════════════{RESET}\n")

        # Vital Meters
        lines.append(f"  {WHITE_BONE}PHYSIOLOGICAL VITALS:{RESET}")
        lines.append(f"    Health / Integrity: {meter_bar(self.hp, 100, 16, RED_BLOOD)}")
        lines.append(f"    Blood Volume:       {meter_bar(self.blood, 100, 16, RED_CRIMSON)}")
        lines.append(f"    Sanity / Cohesion:  {meter_bar(self.sanity, 100, 16, BLUE_STEEL)}")
        lines.append(f"    Manual Dexterity:   {meter_bar(self.dexterity, 100, 16, YELLOW_AMBER)}")
        lines.append(f"    Lower Mobility:     {meter_bar(self.mobility, 100, 16, YELLOW_WARNING)}")
        lines.append(f"    Sensory Perception: {meter_bar(self.perception, 100, 16, GREEN_ACID)}\n")

        # Active Hemorrhage
        if self.bleeding > 0:
            b_desc = {1: "Slow capillary seepage", 2: "Pulsing arterial laceration", 3: "Catastrophic arterial rupture"}[self.bleeding]
            lines.append(f"  {RED_BLOOD}[!] ACTIVE HEMORRHAGE: Level {self.bleeding} ({b_desc}){RESET}")
            lines.append(f"      {GRAY_LIGHT}Treatment needed: Use 'USE TOURNIQUET' or 'USE LIGHTER' to cauterize.{RESET}\n")

        # Pain Level
        lines.append(f"  {WHITE_BONE}NEUROLOGICAL PAIN STATE:{RESET} {YELLOW_AMBER}{self.pain}{RESET}\n")

        # Wounds
        lines.append(f"  {WHITE_BONE}ACTIVE TRAUMA & WOUNDS:{RESET}")
        if self.wounds:
            for w in self.wounds:
                lines.append(f"    {RED_CRIMSON}• {w}{RESET}")
        else:
            lines.append(f"    {GRAY_SLATE}(No acute flesh wounds registered yet){RESET}")
        lines.append("")

        # Permanent Physical Scars
        lines.append(f"  {WHITE_BONE}PERMANENT PHYSICAL MUTILATIONS:{RESET}")
        if self.scars_physical:
            for s in self.scars_physical:
                lines.append(f"    {RED_DARK}• {BOLD}{s}{RESET}")
        else:
            lines.append(f"    {GRAY_SLATE}(The vessel remains physically intact... for now){RESET}")
        lines.append("")

        # Mental Trauma
        lines.append(f"  {WHITE_BONE}PSYCHOLOGICAL LESIONS & NEUROSES:{RESET}")
        if self.scars_mental:
            for m in self.scars_mental:
                lines.append(f"    {BLUE_STEEL}• {ITALIC}{m}{RESET}")
        else:
            lines.append(f"    {GRAY_SLATE}(Rational consciousness is still clinging to reality){RESET}")
        lines.append("")

        # Inventory
        lines.append(f"  {WHITE_BONE}INVENTORY & SURGICAL TOOLS:{RESET}")
        if self.inventory:
            for i_id, count in self.inventory.items():
                meta = ITEMS.get(i_id, {"name": i_id, "desc": ""})
                qty_str = f" x{count}" if count > 1 else ""
                lines.append(f"    {YELLOW_AMBER}[{i_id.upper()}]{RESET} {meta['name']}{qty_str} - {GRAY_LIGHT}{meta['desc']}{RESET}")
        else:
            lines.append(f"    {GRAY_SLATE}(Your pockets are empty){RESET}")
        lines.append("")

        # Recorded Tapes
        lines.append(f"  {WHITE_BONE}DR. LOCKE'S RECOVERED TAPES:{RESET}")
        if self.tapes:
            for t_id in self.tapes:
                lines.append(f"    {GRAY_SLATE}• {t_id.upper()} (Type 'TAPE {t_id.replace('tape_', '')}' or 'TAPE' to replay){RESET}")
        else:
            lines.append(f"    {GRAY_SLATE}(No cassette tapes collected yet){RESET}")

        lines.append(f"\n{RED_RUST}═════════════════════════════════════════════════════════════════════════{RESET}")
        return "\n".join(lines)
