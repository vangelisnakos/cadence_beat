from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button as KivyButton
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.core.audio import SoundLoader

from states import state
from packages import utils, config


class RunMetronome(state.State):

    def __init__(self, app, metronome_values: dict[str, int]):
        super().__init__(app)
        self.metronome_values = metronome_values
        self.interval = 60.0 / metronome_values["bpm"]

        self.sound = self.load_sound("basic")
        self.countdown_sound = self.load_sound("countdown")
        self.countdown_started = False

        self.phases = self.build_phases(metronome_values)
        self.current_phase_index = 0
        self.start_time = 0
        self.elapsed_time = 0
        self.paused = False

        self.main_layout = BoxLayout(orientation="vertical", spacing=dp(10), padding=dp(20))

        self.phase_label = Label(text="", font_size=dp(35), size_hint=(1, None), height=dp(50))
        self.timer_label = Label(text="0:00", font_size=dp(50), size_hint=(1, None), height=dp(60))
        self.cycle_label = Label(text="", font_size=dp(35), size_hint=(1, None), height=dp(50))

        self.main_layout.add_widget(self.phase_label)
        self.main_layout.add_widget(self.timer_label)
        self.main_layout.add_widget(self.cycle_label)

        self.back_button = utils.get_back_button()
        self.continue_button = utils.get_continue_button()
        self.pause_button = utils.get_pause_button()

        for btn in [self.back_button, self.continue_button, self.pause_button]:
            self.main_layout.add_widget(btn)
            btn.bind(on_press=self.on_button_press)

        app.add_widget(self.main_layout)

        Clock.schedule_interval(self.update, 0.1)

    @staticmethod
    def build_phases(metronome_values):
        phases = []

        if metronome_values["warm-up"] > 0:
            phases.append(("Warm-up", metronome_values["warm-up"] * 60, False))

        run_dur = metronome_values["run_min"] * 60 + metronome_values["run_sec"]
        rest_dur = metronome_values["rest_min"] * 60 + metronome_values["rest_sec"]
        for _ in range(metronome_values["cycles"]):
            phases.append(("Run", run_dur, True))
            phases.append(("Rest", rest_dur, False))

        if metronome_values["cooldown"] > 0:
            phases.append(("Cooldown", metronome_values["cooldown"] * 60, False))

        return phases

    def load_sound(self, name: str):
        base_directory = utils.cut_at_folder()
        sounds_directory = f"{base_directory}/data/sounds"
        return SoundLoader.load(f"{sounds_directory}/{name}.mp3")

    def on_button_press(self, instance):
        if instance == self.back_button:
            self.go_back_phase()
        elif instance == self.continue_button:
            self.advance_phase()
        elif instance == self.pause_button:
            self.paused = not self.paused

    def update(self, dt):
        if self.paused:
            return

        name, duration, ticking = self.phases[self.current_phase_index]
        self.elapsed_time += dt
        remaining = max(0, int(duration - self.elapsed_time))

        if remaining == 5 and not self.countdown_started:
            if self.countdown_sound:
                self.countdown_sound.play()
            self.countdown_started = True

        if ticking and self.elapsed_time >= self.interval:
            if self.sound:
                self.sound.play()
            self.elapsed_time = 0

        self.phase_label.text = f"{name}: {duration//60}:{duration%60:02d}"
        minutes = remaining // 60
        seconds = remaining % 60
        self.timer_label.text = f"{minutes}:{seconds:02d}"

        if name in ["Run", "Rest"]:
            current_cycle = self.get_current_cycle()
            total_cycles = self.metronome_values["cycles"]
            self.cycle_label.text = f"Cycle: {current_cycle}/{total_cycles}"

        if remaining <= 0:
            self.advance_phase()

    def get_current_cycle(self):
        count = 0
        for i, (name, _, _) in enumerate(self.phases):
            if name == "Run" and i <= self.current_phase_index:
                count += 1
        return max(1, min(count, self.metronome_values["cycles"]))

    def reset_phase(self):
        self.elapsed_time = 0
        self.countdown_started = False
        if self.countdown_sound:
            self.countdown_sound.stop()

    def advance_phase(self):
        self.reset_phase()
        self.current_phase_index += 1
        if self.current_phase_index >= len(self.phases):
            self.exit_state()

    def go_back_phase(self):
        if self.current_phase_index > 0:
            self.reset_phase()
            self.current_phase_index -= 1
        else:
            self.exit_state()
