# 🩸 B L A D E : The House of Severance

> *"Survival is not a gift. It is an amputation."* — Dr. Gabriel Locke

**BLADE** is an immersive, atmospheric terminal-based psychological horror text adventure inspired by the *Saw* franchise. You are trapped inside an elaborate, mouse-trap-style death house engineered by **Dr. Gabriel Locke** ("The Architect"), a disgraced neurosurgeon obsessed with excising human apathy through visceral suffering.

Every room, corridor, and junction contains sadistic mechanical traps, ethical ultimatums, and excruciating choices. Most players will not survive; those who do will be irrevocably transformed—physically, biologically, and mentally.

---

## ⚡ Quick Start: Running in Docker

Ensure Docker is installed and running, then navigate to this directory:

```bash
# Build and launch the containerized server in the background
docker compose up --build -d
```

To view server logs in real time:
```bash
docker compose logs -f
```

To stop the server:
```bash
docker compose down
```

---

## 🎮 How to Connect Over Telnet

Once the container is running on port `2323`, connect using any terminal or Telnet client:

### 1. From Linux or macOS:
```bash
telnet localhost 2323
# Or using netcat:
nc localhost 2323
```

### 2. From Windows (PowerShell or Command Prompt):
If the Windows Telnet client is enabled:
```powershell
telnet localhost 2323
```
Alternatively, connect with **PuTTY**:
- **Host Name**: `localhost` (or WSL IP `127.0.0.1`)
- **Port**: `2323`
- **Connection type**: `Telnet` or `Raw`

---

## 🩸 Core Gameplay & Physiological Systems

### 1. Physiological Vitals & The Anatomy Map
Type `STATUS` or `BODY` at any time to inspect your clinical diagnosis:
* **Health / Integrity (HP)**: Physical damage from blades, blunt trauma, or shocks.
* **Blood Volume**: Drops precipitously if active hemorrhaging is left untreated. Hypovolemic shock sets in below 30%; death occurs at 10%.
* **Active Hemorrhage**: Level 1 (minor trickle), Level 2 (pulsing arterial bleed), or Level 3 (catastrophic). Must be staunched with `USE TOURNIQUET` or seared with `CAUTERIZE`.
* **Sanity / Cohesion**: Psychological trauma from torture, guilt, and sensory horror. Low sanity triggers creeping hallucinations, whispers, corrupted text, and distorted choices.
* **Manual Dexterity**: Impaired by broken thumbs, severed fingers, crushed palms, or third-degree burns. Affects tool usage and delicate disarms.
* **Lower Mobility**: Impaired by severed tendons, flayed quads, and fractures. Affects dodge, leap, and crawl checks.
* **Sensory Perception**: Damaged by blinding needles, sonic blasts, or chemical fumes.

### 2. Permanent Scars & Mutilations
Choices in the house carry permanent consequences. You will accumulate indelible marks such as:
* *Surgically Dislocated Thumb*
* *Flayed Quadriceps & Four-Finger Left Hand*
* *Third-Degree Carbon-Charred Palms*
* *Ruptured Left Eardrum & Severe Tinnitus*
* *Enucleated Right Eye (Monocular Vision)*
* *Executioner's Guilt / Caleb's Screams*

---

## ⌨️ Command Cheat Sheet

At the `[BLADE] > ` prompt, enter numbers for room decisions, or any of the following global commands:

| Command | Action |
| :--- | :--- |
| `1`, `2`, `3`, `4` | Execute a numbered choice or action |
| `STATUS` / `BODY` / `SELF` | Display complete clinical anatomical and psychological diagnosis |
| `INVENTORY` / `INV` / `I` | Display inventory items and unlocked audio cassettes |
| `USE <item>` | Use an item (`USE TOURNIQUET`, `USE LIGHTER`, `USE SYRINGE`, `USE SPLINT`) |
| `CAUTERIZE` | Burn open wounds shut with your lighter (causes severe pain, stops arterial bleed) |
| `TAPE` / `LISTEN` | Replay Dr. Locke's collected cassette tapes |
| `LOOK` / `L` | Re-examine the current room and active hazards |
| `CLEAN [ON/OFF]` | Toggle auto-clearing screen between turns (Default: ON) |
| `CLEAR` / `CLS` | Instantly refresh and clean the terminal screen |
| `SPEED <mode>` | Adjust text pacing (`SPEED normal`, `SPEED fast`, `SPEED instant`) |
| `HELP` / `?` | Display survival guide and commands |
| `QUIT` / `EXIT` | Surrender to the house and disconnect |

---

## 🏛️ Acts of the Death House

1. **Prologue: The Iron Cistern** — Awakening chained in freezing embalming fluid, pulled toward a motorized rotary shredder.
2. **Act I: The Flensing** — The Razor-Wire Corridor, the 2.5kg flesh toll at the Scales of Atonement, and the 15dB Soundless Chamber.
3. **Act II: The Mechanism** — The oscillating Pendulum Scythe & Crushed Glass Wells, the Catwalk of Vitriol over sulfuric acid, and the Optic Labyrinth retinal scanner.
4. **Act III: The Crucible** — The Nitrogen Kiln thermal paradox, the psychological Confessional interrogation, and the Phantasm-9 Hallucinatory Corridor.
5. **Act IV: The Sanctum & The Threshold** — The Master Clockwork Engine Room, Dr. Locke's observation sanctuary, the Biometric Vault Door, and multiple branching endings.

---

## 🏆 Multiple Endings

Depending on your physical scars, blood loss, sanity, moral choices with other victims (Caleb), and philosophical understanding, five unique endings can unfold:
1. **The Hollow Survivor** (Pyrrhic Victory) — Escaped into the dawn rain, permanently maimed and haunted forever.
2. **The Flayed Husk** (Tragic Collapse) — Unlocked the final door, took three steps into the grass, and bled out yards from the road.
3. **The Disciple of the Blade** (Dark Transcendence) — Embraced Locke's ideology and took up the scalpel as the next Architect.
4. **The Broken Martyr** (Redemption in Blood) — Sacrificed your broken vessel to seal Caleb safely into the sunlight.
5. **Psychotic Severance** (Madness Eternal) — Zero sanity; lost inside your own screaming mind in the labyrinth.
