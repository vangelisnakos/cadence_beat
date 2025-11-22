import os
import pygame
import time

def cut_at_folder():
    norm = os.path.normpath(os.getcwd())
    parts = norm.split(os.sep)
    idx = parts.index("cadence_beat")
    return os.sep.join(parts[:idx + 1])

BASE_DIR = cut_at_folder()
SOUNDS_DIR = os.path.join(BASE_DIR, "data\sounds")

def metronome(sound_file: str, bpm: int):
    sound_path = os.path.join(SOUNDS_DIR, sound_file)
    pygame.mixer.init()
    sound = pygame.mixer.Sound(sound_path)

    interval = 60.0 / bpm
    next_tick = time.time()

    print(f"Metronome started at {bpm} BPM. Press Ctrl+C to stop.")

    try:
        while True:
            sound.play()
            next_tick += interval
            sleep_time = next_tick - time.time()
            if sleep_time > 0:
                time.sleep(sleep_time)
    except KeyboardInterrupt:
        print("\nMetronome stopped.")
        pygame.mixer.quit()

# Example
metronome("basic.mp3", 100)
