from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button as KivyButton
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp

from states import state, run_metronome
from packages import utils, config


class ReviewMetronome(state.State):
    def __init__(self, app, metronome_values: dict[str, int]):
        super().__init__(app)
        self.metronome_values = metronome_values

        # Layout for displaying metronome values
        self.main_layout = BoxLayout(orientation="vertical", spacing=dp(10), padding=dp(20))

        # Labels for each value
        self.labels = {}
        self.labels["warmup"] = Label(text=f"Warm-up: {self.metronome_values['warm-up']}:00", size_hint=(1, None), height=dp(40))
        self.labels["bpm"] = Label(text=f"BPM: {self.metronome_values['bpm']}", size_hint=(1, None), height=dp(40))
        self.labels["run"] = Label(text=f"Run: {self.metronome_values['run_min']}:{self.format_seconds('run')}", size_hint=(1, None), height=dp(40))
        self.labels["rest"] = Label(text=f"Rest: {self.metronome_values['rest_min']}:{self.format_seconds('rest')}", size_hint=(1, None), height=dp(40))
        self.labels["cycles"] = Label(text=f"Cycles: {self.metronome_values['cycles']}", size_hint=(1, None), height=dp(40))
        self.labels["cooldown"] = Label(text=f"Cooldown: {self.metronome_values['cooldown']}:00", size_hint=(1, None), height=dp(40))

        for lbl in self.labels.values():
            self.main_layout.add_widget(lbl)

        # Buttons
        self.back_button = utils.get_back_button()
        self.continue_button = utils.get_continue_button()
        self.main_layout.add_widget(self.continue_button)
        self.main_layout.add_widget(self.back_button)

        # Add to app's root
        app.add_widget(self.main_layout)

        # Bind buttons
        self.back_button.bind(on_press=lambda *_: self.exit_state())
        self.continue_button.bind(on_press=lambda *_: self.go_to_run())

    def format_seconds(self, str_type: str) -> str:
        value = self.metronome_values[f"{str_type}_sec"]
        return f"0{value}" if value < 10 else str(value)

    def go_to_run(self):
        new_state = run_metronome.RunMetronome(self.app, self.metronome_values)
        new_state.enter_state()
