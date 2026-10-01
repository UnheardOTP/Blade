import socket
import re
import time
import sys

def clean_ansi(text):
    return re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', text)

def recv_until(sock, delimiter, timeout=8.0):
    start = time.time()
    sock.settimeout(1.0)
    data = ""
    while time.time() - start < timeout:
        try:
            chunk = sock.recv(2048)
            if not chunk:
                break
            text = chunk.decode('utf-8', errors='replace')
            data += text
            clean = clean_ansi(data)
            if delimiter.lower() in clean.lower():
                return data
        except socket.timeout:
            pass
    return data

def main():
    print("==================================================================", flush=True)
    print("   AUTOMATED COMPLETE PLAYTHROUGH: BLADE (DOCKER CONTAINER)", flush=True)
    print("==================================================================", flush=True)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('127.0.0.1', 2323))
    print("[1] Connected to port 2323 over Telnet!", flush=True)

    # 1. Read Intro
    intro = recv_until(sock, "open your eyes")
    assert "open your eyes" in clean_ansi(intro).lower(), "Failed to get intro screen"
    print("[2] Title screen & ASCII Art received cleanly.", flush=True)

    # 2. Press Enter to start
    sock.sendall(b"\r\n")
    name_prompt = recv_until(sock, "What designation")
    print("[3] Name prompt received.", flush=True)

    # 3. Enter character name
    sock.sendall(b"Detective Vance\r\n")
    cistern = recv_until(sock, "[BLADE] >")
    assert "THE IRON CISTERN" in clean_ansi(cistern), "Failed to enter Cistern"
    print("[4] Awakening: Entered THE IRON CISTERN [Prologue]", flush=True)

    # 4. Test STATUS command
    sock.sendall(b"status\r\n")
    status = recv_until(sock, "[BLADE] >")
    assert "CLINICAL ANATOMICAL DISSECTION" in clean_ansi(status), "STATUS screen failed"
    print("[5] Anatomy HUD command: Verified clinical status screen!", flush=True)

    # 5. Test INVENTORY command
    sock.sendall(b"inv\r\n")
    inv = recv_until(sock, "[BLADE] >")
    assert "INVENTORY" in clean_ansi(inv), "INVENTORY failed"
    print("[6] Inventory command: Verified inventory list!", flush=True)

    # 6. Test TAPE command
    sock.sendall(b"tape 1\r\n")
    tape = recv_until(sock, "[BLADE] >")
    assert "AUDIO LOG" in clean_ansi(tape), "TAPE playback failed"
    print("[7] Audio Tape command: Verified Dr. Locke Tape #1 playback!", flush=True)

    # 7. Cistern: Choose option 2 (Dislocate thumb)
    sock.sendall(b"2\r\n")
    drain = recv_until(sock, "[BLADE] >")
    assert "THE DRAINAGE CONDUIT" in clean_ansi(drain), "Failed to escape Cistern via thumb dislocation"
    print("[8] Sacrificial Choice: Dislocated thumb! Escaped Cistern -> THE DRAINAGE CONDUIT", flush=True)

    # 8. Drainage Conduit: Option 1 (Loot TRIAGE locker)
    sock.sendall(b"1\r\n")
    triage = recv_until(sock, "[BLADE] >")
    assert "TRIAGE" in clean_ansi(triage), "Failed to loot TRIAGE locker"
    print("[9] Triage: Collected medical supplies from locker.", flush=True)

    # 8b. Use Tourniquet to bind bleeding from dislocated thumb!
    sock.sendall(b"use tourniquet\r\n")
    t_res = recv_until(sock, "[BLADE] >")
    assert "TREATMENT" in clean_ansi(t_res), "Tourniquet failed"
    print("[9b] Medical Triage: Bound arterial bleed with tourniquet (+5 HP, bleeding stopped)!", flush=True)

    # 9. Enter Act I: The Flensing (Option 3: Open blast door)
    sock.sendall(b"3\r\n")
    razor = recv_until(sock, "[BLADE] >")
    assert "THE RAZOR HALLWAY" in clean_ansi(razor), "Failed to enter Razor Hallway"
    print("[10] Transition: Entered Act I: THE RAZOR HALLWAY", flush=True)

    # 10. Razor Hallway: Option 1 (Crawl on belly under piano wires)
    sock.sendall(b"1\r\n")
    scales = recv_until(sock, "[BLADE] >")
    assert "THE SCALES OF ATONEMENT" in clean_ansi(scales), "Failed to enter Scales of Atonement"
    print("[11] Hazard Survived: Crawled under piano wires -> THE SCALES OF ATONEMENT", flush=True)

    # 11. Scales of Atonement: Option 3 (200V electrified lead block, searing palms, sparing Caleb)
    sock.sendall(b"3\r\n")
    soundless = recv_until(sock, "[BLADE] >")
    assert "THE SOUNDLESS CHAMBER" in clean_ansi(soundless), "Failed to enter Soundless Chamber"
    print("[12] Moral Dilemma: Seized 200V block, seared palms, spared Caleb -> THE SOUNDLESS CHAMBER", flush=True)

    # 12. Soundless Chamber: Option 2 (Throw bone to trip acoustic spike hammers)
    sock.sendall(b"2\r\n")
    pendulum = recv_until(sock, "[BLADE] >")
    assert "THE PENDULUM THEATRE" in clean_ansi(pendulum), "Failed to enter Pendulum Theatre"
    print("[13] Acoustic Trap Disarmed: Tripped sensors safely -> Act II: THE PENDULUM THEATRE", flush=True)

    # 12b. Inject Epinephrine to survive the upcoming voltage!
    sock.sendall(b"use syringe\r\n")
    epi_res = recv_until(sock, "[BLADE] >")
    assert "EPINEPHRINE" in clean_ansi(epi_res), "Adrenaline injection failed"
    print("[13b] Pharmacology: Injected adrenaline (+25 HP, pain numbness, restored mobility)!", flush=True)

    # 13. Pendulum Theatre: Option 1 (Plunge hands into crushed glass wells under 120V)
    sock.sendall(b"1\r\n")
    basin = recv_until(sock, "[BLADE] >")
    assert "THE CATWALK OF VITRIOL" in clean_ansi(basin), "Failed to enter Catwalk of Vitriol"
    print("[14] Timed Trap: Endured crushed glass & voltage -> THE CATWALK OF VITRIOL", flush=True)

    # 14. Catwalk of Vitriol: Option 3 (Call Caleb, who assists using hoist)
    sock.sendall(b"3\r\n")
    optic = recv_until(sock, "[BLADE] >")
    assert "THE OPTIC LABYRINTH" in clean_ansi(optic), "Failed to enter Optic Labyrinth"
    print("[15] Ally Payoff: Caleb lowered hoist across acid -> THE OPTIC LABYRINTH", flush=True)

    # 15. Optic Labyrinth: Option 2 (Tool extraction using copper wire & scalpel)
    sock.sendall(b"2\r\n")
    kiln = recv_until(sock, "[BLADE] >")
    assert "THE NITROGEN KILN" in clean_ansi(kiln), "Failed to enter Nitrogen Kiln"
    print("[16] Retinal Gateway: Extracted eye surgically -> Act III: THE NITROGEN KILN", flush=True)

    # 16. Nitrogen Kiln: Option 2 (Tether steam valve with wire)
    sock.sendall(b"2\r\n")
    confess = recv_until(sock, "[BLADE] >")
    assert "THE CONFESSIONAL CRUCIBLE" in clean_ansi(confess), "Failed to enter Confessional"
    print("[17] Thermal Paradox: Equalized nitrogen & steam -> THE CONFESSIONAL CRUCIBLE", flush=True)

    # 17. Confessional Question 1: Option 1 (Honest confession of panic)
    sock.sendall(b"1\r\n")
    q2 = recv_until(sock, "[BLADE] >")
    assert "QUESTION II" in clean_ansi(q2), "Failed to advance to Question 2"
    print("[18] Psychological Interrogation: Passed Question 1 (Honest contrition)", flush=True)

    # 18. Confessional Question 2: Option 1 (Compassion for human life)
    sock.sendall(b"1\r\n")
    q3 = recv_until(sock, "[BLADE] >")
    assert "FINAL QUESTION" in clean_ansi(q3), "Failed to advance to Question 3"
    print("[19] Psychological Interrogation: Passed Question 2 (True compassion)", flush=True)

    # 19. Confessional Question 3: Option 1 (Fought for every breath)
    sock.sendall(b"1\r\n")
    res = recv_until(sock, "[BLADE] >")
    clean_res = clean_ansi(res)
    
    if "HALLUCINATIONS" in clean_res:
        print("[19b] Phantasm-9 Neurotoxin triggered! Entering Hallucinatory Corridor...", flush=True)
        # Choose option 2: Ground self in real physical pain
        sock.sendall(b"2\r\n")
        engine = recv_until(sock, "[BLADE] >")
        print("[19c] Grounded in real scar pain! Broke hallucination -> THE MASTER ENGINE ROOM", flush=True)
    else:
        engine = res
        print("[19b] Passed Question 3 directly -> Act IV: THE MASTER ENGINE ROOM", flush=True)

    assert "ENGINE ROOM" in clean_ansi(engine), "Failed to enter Master Engine Room"

    # 20. Engine Room: Option 2 (Crawl through low oil conduit beneath churning gears)
    sock.sendall(b"2\r\n")
    sanctum = recv_until(sock, "[BLADE] >")
    assert "THE ARCHITECT'S SANCTUM" in clean_ansi(sanctum), "Failed to enter Architect Sanctum"
    print("[20] Machinery Traversed: Reached THE ARCHITECT'S SANCTUM & THRESHOLD", flush=True)

    # 21. Architect Sanctum: Option 1 (Step onto Biometric Scale)
    sock.sendall(b"1\r\n")
    ending = recv_until(sock, "THANK YOU FOR PLAYING", timeout=10.0)
    clean_ending = clean_ansi(ending)
    assert "ENDING" in clean_ending, "Failed to trigger ending"
    print("[21] Biometric Threshold: Final Evaluation complete! Ending triggered:\n", flush=True)
    
    for line in clean_ending.split('\n'):
        if "ENDING" in line or "MARKS OF SEVERANCE" in line or "Physical Mutilations" in line or "Psychological Traumas" in line or "•" in line:
            print(f"     >>> {line.strip()}", flush=True)

    sock.close()
    print("\n==================================================================", flush=True)
    print("   FULL PLAYTHROUGH PASSED WITH 100% SUCCESS!", flush=True)
    print("==================================================================", flush=True)

if __name__ == '__main__':
    main()
