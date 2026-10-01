"""
Core Game Engine, state machine, command dispatcher, and session runner.
"""

import asyncio
from typing import Callable, Awaitable, Optional, Dict

from blade.player import Player
from blade.rooms import create_room_registry
from blade.audio_tapes import render_tape, TAPES
from blade.items import ITEMS
from blade.terminal import (
    RESET, BOLD, ITALIC, RED_BLOOD, RED_CRIMSON, RED_RUST, RED_DARK,
    YELLOW_AMBER, YELLOW_WARNING, BLUE_STEEL, GRAY_SLATE, GRAY_LIGHT,
    WHITE_BONE, GREEN_ACID, GRAY_DIM, LOGO, SKULL_ART, CLEAR_SCREEN, horizontal_rule,
    box_text, corrupt_glitch, center_text
)


class GameSession:
    """Manages an individual player's interactive game session over Telnet/terminal."""

    def __init__(
        self,
        writer: Callable[[str], Awaitable[None]],
        reader: Callable[[], Awaitable[str]]
    ):
        self.writer = writer
        self.reader = reader
        self.player: Player = Player("Subject 7")
        self.rooms = create_room_registry()
        self.current_room_id: str = "cistern_wake"
        self.running: bool = True
        self.game_over: bool = False
        self.clean_screen: bool = True
        self.last_feedback: list = []
        self.view_mode: str = "room"
        self.current_tape_content: str = ""

    async def send(self, text: str):
        """Sends raw text to player connection."""
        await self.writer(text)

    async def send_slow(self, text: str, delay: float = 0.012):
        """Sends text with optional typewriter effect, respecting player's speed setting."""
        if self.player.text_speed == "instant":
            await self.send(text)
            return

        eff_delay = delay if self.player.text_speed == "normal" else 0.003
        for char in text:
            await self.send(char)
            if char in [".", "!", "?", "\n"]:
                await asyncio.sleep(eff_delay * 2)
            else:
                await asyncio.sleep(eff_delay)

    async def prompt(self, prompt_text: str = "\n[BLADE] > ") -> Optional[str]:
        """Sends prompt and awaits input line from reader."""
        await self.send(f"{RED_RUST}{prompt_text}{WHITE_BONE}")
        try:
            line = await self.reader()
            if line is None:
                self.running = False
                return None
            await self.send(RESET)
            return line.strip()
        except (asyncio.CancelledError, Exception):
            self.running = False
            return None

    async def start(self):
        """Launches the game loop."""
        await self.send(CLEAR_SCREEN)
        await self.send(LOGO)
        await self.send(f"\n{center_text('Press [ENTER] to open your eyes...', 76)}\n")
        init_line = await self.reader()
        if init_line is None:
            return

        await self.send(f"\n{RED_RUST}What designation do you whisper into the dark? [Default: Subject 7]: {WHITE_BONE}")
        name_line = await self.reader()
        if name_line is None:
            return
        name_input = name_line.strip()
        if name_input:
            self.player.name = name_input[:20]

        await self.send(f"\n{GRAY_SLATE}The cold fluid rises to your throat. Dr. Locke's timers begin.{RESET}\n\n")
        await asyncio.sleep(1.0)

        # Main gameplay loop
        while self.running and not self.game_over:
            current_room = self.rooms.get(self.current_room_id)
            if not current_room:
                await self.send(f"{RED_BLOOD}Critical error: Room {self.current_room_id} not found.{RESET}\n")
                break

            # 1. Clear terminal between turns if clean_screen mode is enabled
            if self.clean_screen:
                await self.send(CLEAR_SCREEN)

            # 2. Render previous action outcome if any
            if self.last_feedback:
                feedback_str = "\n\n".join(self.last_feedback).strip()
                if feedback_str:
                    await self.send(box_text(feedback_str, title="ACTION OUTCOME", color=RED_RUST, width=78) + "\n\n")
                self.last_feedback.clear()

            # 3. Render current view mode
            if self.view_mode == "status":
                await self.send(self.player.inspect_status() + "\n")
            elif self.view_mode == "inventory":
                await self.send(self.render_inventory() + "\n")
            elif self.view_mode == "help":
                await self.send(self.render_help() + "\n")
            elif self.view_mode == "tape":
                await self.send(self.current_tape_content + "\n")
            else:
                # Default chamber view
                await self.send(current_room.get_header() + "\n\n")
                narrative, choices = current_room.render(self.player)

                # Apply sanity glitch if hallucinating
                if self.player.hallucinating or self.player.sanity < 30:
                    narrative = corrupt_glitch(narrative, (100 - self.player.sanity) / 100.0)

                await self.send(narrative + "\n\n")

                # Render Choices
                await self.send(f"{WHITE_BONE}ACTIONS AVAILABLE:{RESET}\n")
                for cmd, label in choices:
                    await self.send(f"  {YELLOW_AMBER}[{cmd}]{RESET} {GRAY_LIGHT}{label}{RESET}\n")

            # 4. Status Bar & Commands Hint
            await self.send(
                f"\n{GRAY_SLATE}[COMMANDS: STATUS | INVENTORY | USE <item> | TAPE | LOOK | HELP | QUIT | CLEAN]{RESET}\n"
                f"{self.player.status_summary()}\n"
            )
            if self.view_mode != "room":
                await self.send(f"{GRAY_DIM}(Type 'LOOK' to return to chamber view, or select an action directly){RESET}\n")

            # 5. Prompt for user input
            user_input = await self.prompt()
            if not self.running or user_input is None:
                break

            if not user_input:
                continue

            # 6. Check Global Commands
            handled_global = await self.handle_global_command(user_input)
            if handled_global:
                continue

            # User selected an action: switch back to room view
            self.view_mode = "room"

            # Pass choice to Room
            next_room_id, feedback = current_room.handle_choice(user_input, self.player)

            # Store feedback for the next turn
            if feedback:
                self.last_feedback.append(feedback)

            # Process turn ticks (bleeding, sanity, pain)
            tick_events = self.player.tick_turn()
            for ev in tick_events:
                self.last_feedback.append(ev)

            # If clean_screen is disabled (scrolling mode), send feedback immediately
            if not self.clean_screen:
                for fb in self.last_feedback:
                    await self.send(f"{fb}\n")
                self.last_feedback.clear()

            # Check Player Vitals / Death
            if not self.player.is_alive():
                await self.handle_death()
                break

            # Process Room Transitions / Endings
            if next_room_id:
                if next_room_id == "DEATH":
                    await self.handle_death()
                    break
                elif next_room_id.startswith("ENDING_") or next_room_id.startswith("VICTORY"):
                    await self.handle_ending(next_room_id)
                    break
                else:
                    self.current_room_id = next_room_id

        await self.send(f"\n{GRAY_SLATE}Connection to Locke's Death House closed.{RESET}\n")

    async def handle_global_command(self, cmd: str) -> bool:
        """Handles ubiquitous meta-commands."""
        parts = cmd.lower().split()
        if not parts:
            return False
        root = parts[0]

        if root in ["status", "body", "self", "anatomy"]:
            self.view_mode = "status"
            return True

        if root in ["inventory", "inv", "i"]:
            self.view_mode = "inventory"
            return True

        if root in ["look", "l"]:
            self.view_mode = "room"
            return True

        if root in ["tape", "tapes", "listen"]:
            if len(parts) > 1:
                t_num = parts[1].replace("tape", "").replace("#", "")
                t_id = f"tape_0{t_num}" if len(t_num) == 1 else f"tape_{t_num}"
                if t_id in TAPES:
                    self.current_tape_content = render_tape(t_id)
                else:
                    self.current_tape_content = f"{GRAY_SLATE}No cassette found matching '{parts[1]}'.{RESET}\n"
            else:
                if self.player.tapes:
                    latest = self.player.tapes[-1]
                    self.current_tape_content = render_tape(latest)
                else:
                    self.current_tape_content = f"{GRAY_SLATE}You have not collected any cassette tapes yet.{RESET}\n"
            self.view_mode = "tape"
            return True

        if root in ["clean", "cls", "clear"]:
            if len(parts) > 1:
                sub = parts[1].lower()
                if sub in ["off", "disable", "scroll", "false"]:
                    self.clean_screen = False
                    self.last_feedback.append(f"{YELLOW_AMBER}[Screen paging mode: DISABLED (scrolling mode active)]{RESET}")
                elif sub in ["on", "enable", "page", "true"]:
                    self.clean_screen = True
                    self.last_feedback.append(f"{YELLOW_AMBER}[Screen paging mode: ENABLED (clean screen active)]{RESET}")
            else:
                self.view_mode = "room"
                self.last_feedback.clear()
            return True

        if root in ["treat", "bandage", "heal"]:
            succ, msg = self.player.apply_bandage()
            self.last_feedback.append(msg)
            self.last_feedback.extend(self.player.tick_turn())
            self.view_mode = "room"
            if not self.clean_screen:
                for fb in self.last_feedback:
                    await self.send(f"{fb}\n")
                self.last_feedback.clear()
            return True

        if root == "cauterize":
            succ, msg = self.player.cauterize_wound()
            self.last_feedback.append(msg)
            self.last_feedback.extend(self.player.tick_turn())
            self.view_mode = "room"
            if not self.clean_screen:
                for fb in self.last_feedback:
                    await self.send(f"{fb}\n")
                self.last_feedback.clear()
            return True

        if root == "use":
            if len(parts) < 2:
                self.last_feedback.append(f"{GRAY_SLATE}Usage: USE <item> (e.g. USE TOURNIQUET, USE LIGHTER, USE SYRINGE, USE SPLINT){RESET}")
                self.view_mode = "room"
                return True
            target_item = parts[1]
            if target_item in ["tourniquet", "bandage"]:
                succ, msg = self.player.apply_bandage()
                self.last_feedback.append(msg)
            elif target_item in ["lighter", "fire"]:
                succ, msg = self.player.cauterize_wound()
                self.last_feedback.append(msg)
            elif target_item in ["syringe", "adrenaline", "epinephrine"]:
                succ, msg = self.player.use_adrenaline()
                self.last_feedback.append(msg)
            elif target_item in ["splint", "bone_splint"]:
                succ, msg = self.player.apply_splint()
                self.last_feedback.append(msg)
            elif target_item in ["tape", "cassette", "recorder", "cassette_player"]:
                if self.player.tapes:
                    self.current_tape_content = render_tape(self.player.tapes[-1])
                    self.view_mode = "tape"
                    return True
                else:
                    self.last_feedback.append(f"{GRAY_SLATE}No audio tapes recorded.{RESET}")
                    self.view_mode = "room"
                    return True
            else:
                self.last_feedback.append(f"{GRAY_SLATE}You cannot use '{target_item}' right now.{RESET}")

            self.last_feedback.extend(self.player.tick_turn())
            self.view_mode = "room"
            if not self.clean_screen:
                for fb in self.last_feedback:
                    await self.send(f"{fb}\n")
                self.last_feedback.clear()
            return True

        if root == "help" or root == "?":
            self.view_mode = "help"
            return True

        if root == "speed":
            if len(parts) > 1 and parts[1] in ["normal", "fast", "instant"]:
                self.player.text_speed = parts[1]
                self.last_feedback.append(f"{GRAY_SLATE}Text speed set to '{parts[1]}'.{RESET}")
            else:
                self.last_feedback.append(f"{GRAY_SLATE}Text speed options: 'speed normal', 'speed fast', 'speed instant'.{RESET}")
            self.view_mode = "room"
            return True

        if root in ["quit", "exit"]:
            await self.send(f"\n{RED_DARK}You close your eyes and let the darkness claim you. Game exited.{RESET}\n")
            self.running = False
            return True

        return False

    def render_inventory(self) -> str:
        lines = [f"{horizontal_rule('─', RED_RUST, 70)}", f"{WHITE_BONE}{BOLD}INVENTORY & COLLECTED ITEMS:{RESET}"]
        if not self.player.inventory:
            lines.append(f"  {GRAY_SLATE}(Your pockets are empty){RESET}")
        else:
            for item_id, count in self.player.inventory.items():
                meta = ITEMS.get(item_id, {"name": item_id, "desc": ""})
                qty = f" x{count}" if count > 1 else ""
                lines.append(f"  {YELLOW_AMBER}[{item_id.upper()}]{RESET} {meta['name']}{qty}\n    {GRAY_SLATE}{meta['desc']}{RESET}")

        if self.player.tapes:
            lines.append(f"\n{WHITE_BONE}CASSETTE TAPES:{RESET}")
            for t_id in self.player.tapes:
                t = TAPES.get(t_id, {"title": t_id})
                lines.append(f"  {GRAY_LIGHT}• {t['title']} (Type 'TAPE {t_id.replace('tape_', '')}' to play){RESET}")

        lines.append(horizontal_rule('─', RED_RUST, 70))
        return "\n".join(lines)

    def render_help(self) -> str:
        return (
            f"\n{horizontal_rule('═', RED_RUST, 70)}\n"
            f"{WHITE_BONE}{BOLD}SURVIVAL MANUAL & TERMINAL COMMANDS:{RESET}\n"
            f"  {YELLOW_AMBER}1, 2, 3...{RESET}         Execute narrative action choice\n"
            f"  {YELLOW_AMBER}STATUS / BODY{RESET}     View clinical anatomical dissection, wounds, scars, vitals\n"
            f"  {YELLOW_AMBER}INVENTORY / I{RESET}     Inspect tools, medical supplies, and cassette tapes\n"
            f"  {YELLOW_AMBER}USE <item>{RESET}        Use an item (e.g. USE TOURNIQUET, USE LIGHTER, USE SYRINGE)\n"
            f"  {YELLOW_AMBER}CAUTERIZE{RESET}         Burn open wound shut with lighter (stops bleed, causes burn)\n"
            f"  {YELLOW_AMBER}TAPE / LISTEN{RESET}     Replay Dr. Locke's recorded audio logs\n"
            f"  {YELLOW_AMBER}LOOK / L{RESET}          Re-examine current chamber and hazards\n"
            f"  {YELLOW_AMBER}CLEAN [ON/OFF]{RESET}    Toggle auto-clearing screen between turns (Default: ON)\n"
            f"  {YELLOW_AMBER}CLEAR / CLS{RESET}      Instantly refresh and clean the screen\n"
            f"  {YELLOW_AMBER}SPEED <mode>{RESET}      Set text rendering: normal / fast / instant\n"
            f"  {YELLOW_AMBER}QUIT / EXIT{RESET}       Surrender and disconnect\n"
            f"{horizontal_rule('═', RED_RUST, 70)}\n"
        )

    async def handle_death(self):
        """Renders the death sequence and clinical post-mortem."""
        self.game_over = True
        death_reason = self.player.get_death_reason()

        await self.send(f"\n{CLEAR_SCREEN}")
        await self.send(SKULL_ART)
        await self.send(f"\n{RED_BLOOD}{BOLD}{center_text('Y O U   H A V E   P E R I S H E D', 76)}{RESET}\n")
        await self.send(f"{horizontal_rule('═', RED_BLOOD, 76)}\n")

        boxed_eulogy = box_text(
            f"{death_reason}\n\n"
            f"Dr. Locke's recorded voice echoes through the dark pipes above your corpse:\n"
            f"\"The vessel has failed the test. In the end, your attachment to comfort was stronger "
            f"than your will to survive. Discard the remains.\"",
            title="POST-MORTEM BIOPSY",
            color=RED_CRIMSON,
            width=76
        )
        await self.send(boxed_eulogy + "\n\n")

        # Autopsy statistics
        await self.send(f"{WHITE_BONE}FINAL AUTOPSY REPORT:{RESET}\n")
        await self.send(f"  Designation:          {self.player.name}\n")
        await self.send(f"  Chamber of Cessation: {self.current_room_id.upper()}\n")
        await self.send(f"  Physical Mutilations: {len(self.player.scars_physical)}\n")
        for scar in self.player.scars_physical:
            await self.send(f"    {RED_DARK}• {scar}{RESET}\n")
        await self.send(f"  Psychological Scars:  {len(self.player.scars_mental)}\n")
        for scar in self.player.scars_mental:
            await self.send(f"    {BLUE_STEEL}• {scar}{RESET}\n")
        await self.send(f"\n{RED_RUST}═════════════════════════════════════════════════════════════════════════{RESET}\n")

    async def handle_ending(self, ending_id: str):
        """Displays one of the deep narrative endings."""
        self.game_over = True
        await self.send(f"\n{CLEAR_SCREEN}")

        if ending_id == "ENDING_HOLLOW_SURVIVOR" or ending_id == "VICTORY_SURVIVOR":
            title = "ENDING 1: THE HOLLOW SURVIVOR (PYRRHIC VICTORY)"
            text = (
                f"You stagger through the massive vault door into the freezing dawn rain.\n\n"
                f"You fall to your knees on the wet gravel driveway of an abandoned slaughterhouse nestled deep "
                f"in the pine forests. The cold drops wash the crusts of blood, quicklime, and formaldehyde from your face.\n\n"
                f"Behind you, the 10-ton steel vault door swings shut with a final, eternal hydraulic THUD.\n\n"
                f"You look down at your mangled hands, your dislocated thumb, your burned palms, your scarred thighs. "
                f"You survived. You beat every trap, paid every toll, and endured every agony Dr. Locke designed.\n\n"
                f"An hour later, headlights sweep over the trees. A highway patrol car skids to a stop. "
                f"An officer rushes toward you with blankets and shouts into a radio.\n\n"
                f"They take you to a sterile hospital. They stitch what can be stitched, graft what can be grafted, "
                f"and whisper psychological diagnoses behind closed doors. But you know the truth.\n\n"
                f"You did not escape whole. Every night when you close your eyes, you will hear the ticking of the winch. "
                f"Every time you touch another person, you will feel the cold blade. You are alive... but hollowed out forever."
            )
            color = GREEN_ACID

        elif ending_id == "ENDING_FLAYED_HUSK":
            title = "ENDING 2: THE FLAYED HUSK (TRAGIC COLLAPSE)"
            text = (
                f"The vault door unseals. Morning sunlight, bright and golden, pours across the bloodstained tiles.\n\n"
                f"You step over the threshold. The smell of pine needles, wet dirt, and freedom fills your scorched lungs. "
                f"You take one step... two steps... three steps into the green grass.\n\n"
                f"Then, the world turns gray.\n\n"
                f"Your cardiovascular system has run completely dry. Hypovolemic shock claims your brain. "
                f"Your knees buckle, and you collapse face-first into the clover, mere yards from the rural highway.\n\n"
                f"You feel the gentle rain on your bruised neck. You see the dawn sky through your clouded eyes. "
                f"With a faint, bloody breath, your heart beats its final, exhausted stroke.\n\n"
                f"You died a free person. But the house took everything you had to give."
            )
            color = YELLOW_WARNING

        elif ending_id == "ENDING_DISCIPLE" or ending_id == "VICTORY_DISCIPLE":
            title = "ENDING 3: THE DISCIPLE OF THE BLADE (DARK TRANSCENDENCE)"
            text = (
                f"The vault door stands open to the dawn, but you do not step outside.\n\n"
                f"You turn back toward Dr. Locke. He looks at you with dying, reverent eyes. "
                f"\"You understand now,\" he whispers. \"The sheep sleep in their pastures, numb to the slaughter. "
                f"Only the blade wakes them.\"\n\n"
                f"You step up to the dying man. You reach out your glass-shredded, carbon-burned hand and take "
                f"the No. 10 surgical scalpel from his fingers. The weight of the knurled brass handle feels natural. "
                f"Right. True.\n\n"
                f"You turn toward the master control console. You press the red pneumatic switch.\n\n"
                f"The 10-ton vault door closes, sealing the sunlight away.\n\n"
                f"You sit in the observation chair beneath the flickering CRT monitors. You pick up a blank cassette tape, "
                f"press RECORD, and lean into the microphone:\n\n"
                f"\"Greetings. If you are hearing this, the sedative has worn off...\""
            )
            color = RED_BLOOD

        elif ending_id == "ENDING_MARTYR":
            title = "ENDING 4: THE BROKEN MARTYR (REDEMPTION IN BLOOD)"
            text = (
                f"The siren blares: [DUAL OCCUPANCY OVERLOAD - EMERGENCY LOCKDOWN IN 5 SECONDS].\n\n"
                f"Caleb grabs your arm, trying desperately to drag your shattered body across the threshold. "
                f"\"I can't leave you! Come on!\"\n\n"
                f"You look at your crippled limbs, your bleeding chest, your hollowed frame. You know your race is run.\n\n"
                f"With a final surge of strength, you shove Caleb through the doorway onto the grass outside! "
                f"You reach up and pull the manual emergency seal cable from the inside!\n\n"
                f"The 10-ton blast door slams down with an earth-shattering crash! "
                f"Through the reinforced observation glass, Caleb pounds on the steel, weeping in disbelieving agony, "
                f"safe in the dawn sunlight.\n\n"
                f"You turn your back on the glass. You slump against the sealed door, closing your eyes in the silence. "
                f"For the first time since the hit-and-run on Miller Road, the suffocating guilt in your chest is gone. "
                f"You die in the dark, but with peace in your soul."
            )
            color = BLUE_STEEL

        else:  # ENDING_PSYCHOTIC
            title = "ENDING 5: PSYCHOTIC SEVERANCE (MADNESS ETERNAL)"
            text = (
                f"The vault door unseals, but your mind has crossed into the void beyond return.\n\n"
                f"The sunlight burns your eyes like boiling mercury. The trees outside twist into screaming serpents. "
                f"You drop to your knees on the tiles, clawing at your own ears to drown out the deafening roar of phantom voices.\n\n"
                f"\"Cut it off! Cut it away! You're still trapped! You're inside the machine!\"\n\n"
                f"Laughing hysterically, tears of blood streaming down your cheeks, you crawl away from the open doorway, "
                f"retreating back into the comforting, bloody darkness of the house.\n\n"
                f"You curl into a ball beneath the grinding gears of the engine room, laughing into the oil, "
                f"becoming another ghost in Dr. Locke's eternal nightmare."
            )
            color = RED_CRIMSON

        boxed = box_text(text, title=title, color=color, width=76)
        await self.send(f"\n{boxed}\n\n")

        # Summary of Scars
        await self.send(f"{WHITE_BONE}YOUR INDELIBLE MARKS OF SEVERANCE:{RESET}\n")
        await self.send(f"  Physical Mutilations ({len(self.player.scars_physical)}):\n")
        for s in self.player.scars_physical:
            await self.send(f"    {RED_DARK}• {s}{RESET}\n")
        await self.send(f"  Psychological Traumas ({len(self.player.scars_mental)}):\n")
        for s in self.player.scars_mental:
            await self.send(f"    {BLUE_STEEL}• {s}{RESET}\n")

        await self.send(f"\n{RED_RUST}═════════════════════════════════════════════════════════════════════════{RESET}\n")
        await self.send(f"{center_text('THANK YOU FOR PLAYING B L A D E', 76)}\n")
        await self.send(f"{RED_RUST}═════════════════════════════════════════════════════════════════════════{RESET}\n")
