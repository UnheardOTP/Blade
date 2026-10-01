"""
Audio cassette tape logs recorded by Dr. Gabriel Locke ("The Architect").
"""

from blade.terminal import (
    TAPE_ART, RED_CRIMSON, GRAY_SLATE, GRAY_LIGHT, WHITE_BONE, 
    ITALIC, BOLD, RESET, box_text, RED_DARK
)

TAPES = {
    "tape_01": {
        "id": "tape_01",
        "title": "TAPE #1: The Anatomy of Apathy",
        "room": "The Iron Cistern",
        "speaker": "Dr. Gabriel Locke",
        "transcript": (
            "Greetings, subject. If you are hearing this, the sedative has worn off, "
            "and the cold reality of your predicament is dawning in your veins.\n\n"
            "You lived your life behind layers of insulation—ignoring the cries of those "
            "you crushed under the wheels of your convenience. You believed life was an "
            "entitlement, free of charge. Here, in my house, every breath has a currency. "
            "And the exchange rate is paid in bone, nerve, and blood.\n\n"
            "You are chained inside a drainage cistern. Above you, an industrial winch is "
            "reeling you toward rotating shredder teeth. You have very little time before "
            "your neck is severed. To your right is a combination lock. The sequence is the "
            "number of cranial nerves in the human body.\n\n"
            "Or... you can forcefully dislocate your own thumb, slip the iron shackle, and "
            "buy your life with immediate orthopedic trauma.\n\n"
            "Decide quickly. Suffer to live, or die in comfort. Let the cutting begin."
        )
    },
    "tape_02": {
        "id": "tape_02",
        "title": "TAPE #2: The Arithmetic of Flesh",
        "room": "The Scales of Atonement",
        "speaker": "Dr. Gabriel Locke",
        "transcript": (
            "Compassion is cheap when it costs nothing. But what is the true weight of mercy?\n\n"
            "Before you is Caleb. He was an accomplice to your negligence. He sleeps soundly, "
            "numb to the horror. The blast door requires 2.5 kilograms on the brass scale. "
            "A butcher's toll.\n\n"
            "A bone saw and scalpel lie ready. Will you sever a piece of this sleeping man's "
            "leg to buy your passage? Or will you carve into your own thigh and sever your own "
            "fingers to reach the weight?\n\n"
            "Or perhaps you will grasp the electrified block, melting the flesh of both your palms "
            "under 200 volts in exchange for both your lives?\n\n"
            "Show me who you truly are when the blade is in your hand."
        )
    },
    "tape_03": {
        "id": "tape_03",
        "title": "TAPE #3: The Static of the Mind",
        "room": "The Soundless Chamber",
        "speaker": "Dr. Gabriel Locke",
        "transcript": (
            "Silence. Pure, absolute silence. Modern humanity abhors it. You scream, you distract, "
            "you drown out your own rotting conscience with ceaseless noise.\n\n"
            "In this chamber, noise is death. The acoustic transducers on these walls are tuned "
            "to 15 decibels. If you scream, if you weep, if you clatter on this floor of broken glass "
            "and dried bone, the spring-loaded spike hammers will shatter your chest.\n\n"
            "Move with precision. Control your breathing. Suppress your agony. The key is in the bell jar."
        )
    },
    "tape_04": {
        "id": "tape_04",
        "title": "TAPE #4: The Crucible of Extremes",
        "room": "The Nitrogen Kiln",
        "speaker": "Dr. Gabriel Locke",
        "transcript": (
            "Nerve endings are treacherous liars. Severe cold burns, and boiling heat freezes.\n\n"
            "You have made it past flesh and bone; now we test your endurance against thermal paradox. "
            "Sub-zero nitrogen on your left; superheated steam on your right. To unlock the pressure "
            "valves, you must balance both extremes.\n\n"
            "Will you blister, or will you freeze? Or will your will transcend the limits of your skin?"
        )
    },
    "tape_05": {
        "id": "tape_05",
        "title": "TAPE #5: The Final Incision",
        "room": "The Architect's Sanctum",
        "speaker": "Dr. Gabriel Locke",
        "transcript": (
            "You stand before the final vault door. Look behind you at the blood trail you left "
            "through my corridors. Look down at your hands, your limbs, your scars.\n\n"
            "The person who walked into this house was a parasite, hollow and blind. What stands "
            "before the threshold now is something raw, something carved into purpose.\n\n"
            "The biometric door does not read an identification card. It measures biological "
            "sacrifice. Only those who have shed their excess may walk into the dawn.\n\n"
            "Step onto the biometric scale. Let us see what remains of you."
        )
    }
}


def render_tape(tape_id: str) -> str:
    """Formats a cassette tape playback sequence."""
    tape = TAPES.get(tape_id)
    if not tape:
        return f"{RED_CRIMSON}Tape not found or corrupted.{RESET}"

    header = f"{WHITE_BONE}{BOLD}{tape['title']}{RESET}\n{GRAY_SLATE}Location: {tape['room']} | Voice: {tape['speaker']}{RESET}"
    content = f"{ITALIC}{GRAY_LIGHT}\"{tape['transcript']}\"{RESET}"
    boxed = box_text(content, title=tape["title"], color=RED_DARK, width=76)

    return f"\n{TAPE_ART}\n{boxed}\n"
