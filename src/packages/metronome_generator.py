import wave
import tempfile
import os
import io

from kivy.core.audio import SoundLoader
from packages import utils, config


def generate_metronome_audio(bpm, duration_sec):
    """Generate a WAV in memory containing perfectly spaced ticks."""

    tick = SoundLoader.load(utils.cut_at_folder() + "/data/sounds/basic.wav")
    if not tick:
        print("ERROR: tick sound missing")
        return None

    # Read original tick WAV file
    with wave.open(tick.source, "rb") as tick_file:
        tick_frames = tick_file.readframes(tick_file.getnframes())
        tick_params = tick_file.getparams()

    channels = tick_params.nchannels
    sampwidth = tick_params.sampwidth
    framerate = tick_params.framerate

    total_samples = int(duration_sec * framerate)
    bytes_per_sample = channels * sampwidth

    final = bytearray(total_samples * bytes_per_sample)

    samples_per_tick = int((config.SEC_IN_MIN / bpm) * framerate)

    # Insert tick at correct sample positions
    tick_sample_count = len(tick_frames) // bytes_per_sample

    for start_sample in range(0, total_samples, samples_per_tick):
        end_sample = start_sample + tick_sample_count
        if end_sample >= total_samples:
            break

        start_byte = start_sample * bytes_per_sample
        final[start_byte:start_byte + len(tick_frames)] = tick_frames

    # Build WAV in memory
    memfile = io.BytesIO()
    with wave.open(memfile, "wb") as w:
        w.setparams(tick_params)
        w.writeframes(final)

    memfile.seek(0)

    # Save full WAV (NOT raw PCM)
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    tmp.write(memfile.getvalue())  # ✅ full WAV including header
    tmp.close()

    return SoundLoader.load(tmp.name)
