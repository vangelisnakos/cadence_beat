from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.base import EventLoop
from kivy.uix.image import Image
EventLoop.idle()

from packages import utils, config, metronome_generator


class RunMetronome(FloatLayout):
    def __init__(self, app, metronome_values: dict[str, int], **kwargs):
        FloatLayout.__init__(self, **kwargs)
        self.app = app
        self.metronome_values = metronome_values
        self.interval = config.SEC_IN_MIN / metronome_values["bpm"]

        # --- Background ---
        self.bg_image = Image(
            source=utils.get_directory("images") + "/menu_background.png",
            allow_stretch=True,
            keep_ratio=False,
            size_hint=(1, 1),
            pos_hint={"x": 0, "y": 0}
        )
        self.add_widget(self.bg_image)

        # --- Labels ---
        self.phase_label = Label(
            text="",
            font_size=dp(28),
            size_hint=(1, None),
            height=dp(50),
            pos_hint={"top": 0.95}
        )
        self.add_widget(self.phase_label)

        self.timer_label = Label(
            text="0:00",
            font_size=dp(44),
            size_hint=(1, None),
            height=dp(80),
            pos_hint={"center_x": 0.5, "center_y": 0.6}
        )
        self.add_widget(self.timer_label)

        self.cycle_label = Label(
            text="",
            font_size=dp(24),
            size_hint=(1, None),
            height=dp(40),
            pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        self.add_widget(self.cycle_label)

        # --- Top Row: Pause button ---
        self.pause_button = Button(
            text="Pause",
            size_hint=(None, None),
            size=(dp(80), dp(36)),
            pos_hint={"right": 0.98, "top": 0.98}
        )
        self.pause_button.bind(on_press=self.on_pause)
        self.add_widget(self.pause_button)

        # --- Bottom Row: Back / Continue ---
        self.back_button = Button(
            text="Back",
            size_hint=(None, None),
            size=(dp(120), dp(50)),
            pos_hint={"x": 0.05, "y": 0.02}
        )
        self.continue_button = Button(
            text="Continue",
            size_hint=(None, None),
            size=(dp(120), dp(50)),
            pos_hint={"right": 0.95, "y": 0.02}
        )
        self.back_button.bind(on_press=self.on_back)
        self.continue_button.bind(on_press=self.on_continue)
        self.add_widget(self.back_button)
        self.add_widget(self.continue_button)

        # --- Audio ---
        self.sound = None
        self.countdown_sound = None
        self.countdown_started = False
        self.phases = self.build_phases(metronome_values)
        self.current_phase_index = 0
        self.elapsed_time = 0.0
        self.paused = False

        # Start the first phase's audio
        self.start_phase_audio()

        # Schedule UI updates
        Clock.schedule_interval(self.update_ui, 1 / config.FPS)

    def on_pause(self, instance):
        self.paused = not self.paused
        self.pause_button.text = "Resume" if self.paused else "Pause"

    def on_back(self, instance):
        self.go_back_phase()

    def on_continue(self, instance):
        self.advance_phase()

    def update_ui(self, dt):
        if self.paused or self.current_phase_index >= len(self.phases):
            return

        name, duration, ticking = self.phases[self.current_phase_index]
        self.elapsed_time += dt
        remaining = max(0, int(duration - self.elapsed_time))

        # update background
        self.update_background(name)

        if remaining == 5 and not self.countdown_started:
            if self.countdown_sound:
                self.countdown_sound.play()
            self.countdown_started = True

        self.phase_label.text = f"{name}: {duration // config.SEC_IN_MIN}:{duration % config.SEC_IN_MIN:02d}"
        minutes = remaining // config.SEC_IN_MIN
        seconds = remaining % config.SEC_IN_MIN
        self.timer_label.text = f"{minutes}:{seconds:02d}"

        if name in ["Run", "Rest"]:
            current_cycle = self.get_current_cycle()
            total_cycles = self.metronome_values["cycles"]
            self.cycle_label.text = f"Cycle: {current_cycle}/{total_cycles}"
        else:
            self.cycle_label.text = ""

        if remaining <= 0:
            self.advance_phase()

    def update_background(self, phase_name):
        if phase_name == "Run":
            self.bg_image.source = utils.get_directory("images") + "/run_background.png"
        elif phase_name == "Rest":
            self.bg_image.source = utils.get_directory("images") + "/rest_background.png"
        else:
            self.bg_image.source = utils.get_directory("images") + "/menu_background.png"

        self.bg_image.reload()

    @staticmethod
    def build_phases(metronome_values):
        phases = []
        if metronome_values.get("warm-up", 0) > 0:
            phases.append(("Warm-up", metronome_values["warm-up"] * config.SEC_IN_MIN, False))
        run_dur = metronome_values.get("run_min", 0) * config.SEC_IN_MIN + metronome_values.get("run_sec", 0)
        rest_dur = metronome_values.get("rest_min", 0) * config.SEC_IN_MIN + metronome_values.get("rest_sec", 0)
        for _ in range(metronome_values.get("cycles", 1)):
            phases.append(("Run", run_dur, True))
            phases.append(("Rest", rest_dur, False))
        if metronome_values.get("cooldown", 0) > 0:
            phases.append(("Cooldown", metronome_values["cooldown"] * config.SEC_IN_MIN, False))
        return phases

    def get_current_cycle(self):
        count = 0
        for i, (name, _, _) in enumerate(self.phases):
            if name == "Run" and i <= self.current_phase_index:
                count += 1
        return max(1, min(count, self.metronome_values.get("cycles", 1)))

    @staticmethod
    def load_sound(name):
        base = utils.cut_at_folder()
        sounds_dir = f"{base}/data/sounds"
        s = SoundLoader.load(f"{sounds_dir}/{name}.wav")
        return s

    def start_phase_audio(self):
        name, duration, ticking = self.phases[self.current_phase_index]

        if self.sound:
            self.sound.stop()

        if ticking:
            audio = metronome_generator.generate_metronome_audio(self.metronome_values["bpm"], duration)

            if audio:
                self.sound = audio
                self.sound.play()
        else:
            if self.sound:
                self.sound.stop()

    def advance_phase(self):
        self.reset_phase()
        self.current_phase_index += 1
        if self.current_phase_index >= len(self.phases):
            self.exit_state()
        self.start_phase_audio()

    def go_back_phase(self):
        self.reset_phase()
        if self.current_phase_index > 0:
            self.current_phase_index -= 1
            self.start_phase_audio()
        else:
            self.exit_state()

    def reset_phase(self):
        self.elapsed_time = 0.0
        self.countdown_started = False
        if self.countdown_sound:
            self.countdown_sound.stop()

    def stop(self):
        if self.sound:
            self.sound.stop()
        if self.countdown_sound:
            self.countdown_sound.stop()

    def exit_state(self):
        self.stop()
        self.app.exit_state()
