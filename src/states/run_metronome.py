# states/run_metronome.py
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.core.audio import SoundLoader

from packages import utils, config

class RunMetronome(BoxLayout):
    def __init__(self, app, metronome_values: dict[str, int], **kwargs):
        # initialize parents: State manages app reference, BoxLayout manages UI
        BoxLayout.__init__(self, orientation="vertical", spacing=dp(10), padding=dp(20), **kwargs)
        self.app = app

        # ensure it fills the screen and anchored to top
        self.size_hint = (1, 1)
        self.pos_hint = {"top": 1}

        self.metronome_values = metronome_values
        self.interval = 60.0 / max(1, metronome_values.get("bpm", 120))

        self.sound = self.load_sound("basic")
        self.countdown_sound = self.load_sound("countdown")
        self.countdown_started = False

        self.phases = self.build_phases(metronome_values)
        self.current_phase_index = 0
        self.elapsed_time = 0.0
        self.paused = False

        # UI
        self.phase_label = Label(text="", font_size=dp(28), size_hint=(1, None), height=dp(50))
        self.timer_label = Label(text="0:00", font_size=dp(44), size_hint=(1, None), height=dp(80))
        self.cycle_label = Label(text="", font_size=dp(24), size_hint=(1, None), height=dp(40))

        # top row: pause at top right -> put in horizontal layout
        top_row = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(40))
        spacer = Label(size_hint=(1, 1), text="")
        self.pause_button = Button(text="Pause", size_hint=(None, None), size=(dp(80), dp(36)))
        self.pause_button.bind(on_press=self.on_pause)
        top_row.add_widget(spacer)
        top_row.add_widget(self.pause_button)

        self.add_widget(top_row)
        self.add_widget(self.phase_label)
        self.add_widget(self.timer_label)
        self.add_widget(self.cycle_label)

        # bottom buttons: Back / Continue
        bottom_row = BoxLayout(orientation="horizontal", size_hint=(1, None), height=dp(60), spacing=dp(10), padding=[dp(10), 0, dp(10), 0])
        self.back_button = Button(text="Back", size_hint=(None, None), size=(dp(120), dp(50)))
        self.continue_button = Button(text="Continue", size_hint=(None, None), size=(dp(120), dp(50)))
        self.back_button.bind(on_press=self.on_back)
        self.continue_button.bind(on_press=self.on_continue)
        bottom_row.add_widget(self.back_button)
        bottom_row.add_widget(Label())  # spacer
        bottom_row.add_widget(self.continue_button)

        self.add_widget(bottom_row)

        # schedule timer update
        Clock.schedule_interval(self._tick, 0.1)

    # UI callbacks
    def on_pause(self, instance):
        self.paused = not self.paused
        self.pause_button.text = "Resume" if self.paused else "Pause"

    def on_back(self, instance):
        self.go_back_phase()

    def on_continue(self, instance):
        self.advance_phase()

    # timer and phase logic
    def _tick(self, dt):
        if self.paused or self.current_phase_index >= len(self.phases):
            return
        name, duration, ticking = self.phases[self.current_phase_index]
        self.elapsed_time += dt
        remaining = max(0, int(duration - self.elapsed_time))

        if remaining == 5 and not self.countdown_started:
            if self.countdown_sound:
                self.countdown_sound.play()
            self.countdown_started = True

        # play tick on interval
        if ticking and self.elapsed_time >= self.interval:
            if self.sound:
                self.sound.play()
            # subtract interval from elapsed so smaller drift
            self.elapsed_time -= self.interval

        # update UI
        self.phase_label.text = f"{name}: {duration//60}:{duration%60:02d}"
        minutes = remaining // 60
        seconds = remaining % 60
        self.timer_label.text = f"{minutes}:{seconds:02d}"

        if name in ["Run", "Rest"]:
            current_cycle = self.get_current_cycle()
            total_cycles = self.metronome_values["cycles"]
            self.cycle_label.text = f"Cycle: {current_cycle}/{total_cycles}"
        else:
            self.cycle_label.text = ""

        if remaining <= 0:
            self.advance_phase()

    # helpers
    @staticmethod
    def build_phases(metronome_values):
        phases = []
        if metronome_values.get("warm-up", 0) > 0:
            phases.append(("Warm-up", metronome_values["warm-up"] * 60, False))
        run_dur = metronome_values.get("run_min", 0) * 60 + metronome_values.get("run_sec", 0)
        rest_dur = metronome_values.get("rest_min", 0) * 60 + metronome_values.get("rest_sec", 0)
        for _ in range(metronome_values.get("cycles", 1)):
            phases.append(("Run", run_dur, True))
            phases.append(("Rest", rest_dur, False))
        if metronome_values.get("cooldown", 0) > 0:
            phases.append(("Cooldown", metronome_values["cooldown"] * 60, False))
        return phases

    def get_current_cycle(self):
        count = 0
        for i, (name, _, _) in enumerate(self.phases):
            if name == "Run" and i <= self.current_phase_index:
                count += 1
        return max(1, min(count, self.metronome_values.get("cycles", 1)))

    def load_sound(self, name):
        base = utils.cut_at_folder()
        sounds_dir = f"{base}/data/sounds"
        s = SoundLoader.load(f"{sounds_dir}/{name}.mp3")
        return s

    def advance_phase(self):
        self.reset_phase()
        self.current_phase_index += 1
        if self.current_phase_index >= len(self.phases):
            # end: pop this state
            self.app.exit_state()

    def go_back_phase(self):
        if self.current_phase_index > 0:
            self.reset_phase()
            self.current_phase_index -= 1
        else:
            self.app.exit_state()

    def reset_phase(self):
        self.elapsed_time = 0.0
        self.countdown_started = False
        if self.countdown_sound:
            self.countdown_sound.stop()
