import logging
import sys
import os
from kivy.core.audio import SoundLoader
from time import sleep
import android  # noqa
android.log("SERVICE STARTED: top of file")
from packages import metronome_generator, utils
android.log("SERVICE STARTED: mid of file")


def load_sound(name):
    base = utils.get_directory("sounds")
    sound = os.path.join(base, f"{name}.wav")
    return SoundLoader.load(sound)

def main():
    sound_list = sys.argv[1].split("|")
    sound_name = sound_list[0]
    logging.debug("Using Android Service with input: %s", sound_list)

    if sound_name == "beat":
        if len(sound_list) > 1:
            bpm = int(sound_list[1])
            duration = float(sound_list[2])
            audio = metronome_generator.generate_metronome_audio(bpm, duration)
            if audio:
                audio.play()
            else:
                logging.error("Couldn't load the beat audio!")
        else:
            logging.error("Sound list is too short to load beat audio!")
    elif sound_name == "countdown":
        countdown_sound = load_sound(sound_name)
        countdown_sound.play()
    elif sound_name == "end":
        end_sound = load_sound(sound_name)
        end_sound.play()
    else:
        logging.error("Couldn't recognise sound name '%s'!", sound_name)

    while True:
        sleep(1)


if __name__ == "__main__":
    main()
