"""
ANSI Terminal styling, ASCII art, colors, typewriter pacing, and screen manipulation.
"""

import asyncio
import random
import re

# ANSI Color & Formatting Constants
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
ITALIC = "\033[3m"
UNDERLINE = "\033[4m"
BLINK = "\033[5m"
REVERSE = "\033[7m"

# Blood & Rust Palette (256-color)
RED_BLOOD = "\033[38;5;196m"
RED_CRIMSON = "\033[38;5;160m"
RED_RUST = "\033[38;5;124m"
RED_DARK = "\033[38;5;88m"
RED_MAROON = "\033[38;5;52m"

YELLOW_AMBER = "\033[38;5;214m"
YELLOW_WARNING = "\033[38;5;220m"
YELLOW_SICKLY = "\033[38;5;178m"

GREEN_ACID = "\033[38;5;118m"
GREEN_TOXIC = "\033[38;5;112m"
GREEN_BILE = "\033[38;5;100m"

BLUE_FROST = "\033[38;5;123m"
BLUE_STEEL = "\033[38;5;67m"
BLUE_ICE = "\033[38;5;81m"

GRAY_ASH = "\033[38;5;252m"
GRAY_LIGHT = "\033[38;5;248m"
GRAY_SLATE = "\033[38;5;244m"
GRAY_DIM = "\033[38;5;238m"
GRAY_DARK = "\033[38;5;234m"
WHITE_BONE = "\033[38;5;255m"

BG_BLACK = "\033[48;5;232m"
BG_RED_DARK = "\033[48;5;52m"
BG_RUST = "\033[48;5;88m"

CLEAR_SCREEN = "\033[2J\033[H"
CLEAR_LINE = "\033[2K\r"
BELL = "\a"

LOGO = rf"""{RED_BLOOD}
  ██████╗ ██╗      █████╗ ██████╗ ███████╗
  ██╔══██╗██║     ██╔══██╗██╔══██╗██╔════╝
  ██████╔╝██║     ███████║██║  ██║█████╗  
  ██╔══██╗██║     ██╔══██║██║  ██║██╔══╝  
  ██████╔╝███████╗██║  ██║██████╔╝███████╗
  ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═════╝ ╚══════╝{RESET}
 {RED_RUST}═════════════════════════════════════════════════════════════════════════{RESET}
  {GRAY_SLATE}T H E   H O U S E   O F   S E V E R A N C E{RESET}
 {RED_DARK}"Survival is not a gift. It is an amputation." — Dr. Gabriel Locke{RESET}
"""

TAPE_ART = rf"""{GRAY_SLATE}
      .------------------------------------------.
     /  [==]  AUDIO LOG - DR. GABRIEL LOCKE  [==] \
    |  .----------------------------------------. |
    |  |  (O)  ======================  (O)      | |
    |  |        CASSETTE TAPE PLAYBACK           | |
    |  '----------------------------------------' |
     \__________________________________________/
{RESET}"""

SKULL_ART = rf"""{RED_DARK}
                  .---.
                 /     \
                | () () |
                 \  ^  /
                  |||||
                  '---'
{RESET}"""

PENDULUM_ART = rf"""{RED_RUST}
                 |
                 |
                 |
                / \
               /   \
          ____/_____\____
         (_______________)
            \         /
             \_______/
               ( _ )
                '-'
{RESET}"""

CISTERN_ART = rf"""{BLUE_STEEL}
     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    ( ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ )
    ( ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ )
     |  |                     |  |
     |  |====[ CHAIN WINCH ]==|  |
     |                           |
{RESET}"""

BODY_OUTLINE = rf"""{GRAY_SLATE}
           .-'"'-.
          / # #   \      [ HEAD & SENSES ]
         |   ^     |     Eyes, Ears, Speech, Sanity
          \  '-'  /
           '-...-'
          /|  |  |\
         / |  |  | \     [ TORSO & VITALS ]
        /  |  |  |  \    Lungs, Heart, Ribs, Blood
       (   |  |  |   )   
       |   |  |  |   |
       |   |  |  |   |   [ ARMS & HANDS ]
       *   |  |  |   *   Fingers, Grip, Dexterity
          /   |   \
         /    |    \
        |     |     |    [ LEGS & SINEW ]
        |     |     |    Tendons, Knees, Mobility
        |     |     |
       (_/   \_)
{RESET}"""


def strip_ansi(text: str) -> str:
    """Remove ANSI escape codes from string for calculating visual width."""
    return re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', text)


def center_text(text: str, width: int = 76) -> str:
    """Center a string while respecting ANSI color sequences."""
    lines = text.split('\n')
    centered = []
    for line in lines:
        clean = strip_ansi(line)
        padding = max(0, (width - len(clean)) // 2)
        centered.append(' ' * padding + line)
    return '\n'.join(centered)


def horizontal_rule(char: str = "═", color: str = RED_RUST, width: int = 76) -> str:
    return f"{color}{char * width}{RESET}"


def box_text(content: str, title: str = "", color: str = GRAY_SLATE, width: int = 76) -> str:
    """Wraps content in a styled ANSI bordered box."""
    res = []
    if title:
        title_str = f"[ {title} ]"
        rem = max(0, width - 4 - len(title_str))
        res.append(f"{color}┌─{WHITE_BONE}{title_str}{color}{'─' * rem}┐{RESET}")
    else:
        res.append(f"{color}┌{'─' * (width - 2)}┐{RESET}")

    for raw_line in content.split('\n'):
        # wrap long lines
        words = raw_line.split(' ')
        current_line = ""
        for w in words:
            test_line = current_line + (" " if current_line else "") + w
            if len(strip_ansi(test_line)) > width - 4:
                pad = max(0, (width - 4) - len(strip_ansi(current_line)))
                res.append(f"{color}│ {RESET}{current_line}{' ' * pad} {color}│{RESET}")
                current_line = w
            else:
                current_line = test_line
        pad = max(0, (width - 4) - len(strip_ansi(current_line)))
        res.append(f"{color}│ {RESET}{current_line}{' ' * pad} {color}│{RESET}")

    res.append(f"{color}└{'─' * (width - 2)}┘{RESET}")
    return '\n'.join(res)


def meter_bar(current: int, maximum: int = 100, length: int = 14, fill_color: str = RED_BLOOD) -> str:
    """Generates an ANSI block health/meter bar."""
    pct = max(0.0, min(1.0, current / maximum))
    filled = int(round(length * pct))
    empty = length - filled
    return f"{fill_color}{'█' * filled}{GRAY_DIM}{'░' * empty}{RESET} {current}%"


def corrupt_glitch(text: str, severity: float = 0.3) -> str:
    """Injects glitch characters and whispers for low sanity."""
    whispers = [
        " ...it hurts... ",
        " ...cut it away... ",
        " ...he is watching from the wall... ",
        " ...flesh will fail you... ",
        " ...listen to the gears... ",
        " ...no one escapes whole... "
    ]
    glitch_chars = ["$", "@", "&", "#", "%", "!", "?", "/", "§", "‡"]
    chars = list(text)
    for i in range(len(chars)):
        if chars[i].isalpha() and random.random() < severity * 0.12:
            chars[i] = random.choice(glitch_chars)
    result = "".join(chars)
    if random.random() < severity * 0.4:
        idx = random.randint(0, len(result))
        result = result[:idx] + f"{RED_CRIMSON}{ITALIC}{random.choice(whispers)}{RESET}" + result[idx:]
    return result
