from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp

from states import run_metronome
from packages import config


class ReviewMetronome(BoxLayout):
    def __init__(self, app, metronome_values: dict[str, int]):
        super().__init__()
        self.app = app
        self.metronome_values = metronome_values

        # Layout config
        self.orientation = "vertical"
        self.spacing = dp(20)
        self.padding = dp(20)

        parent_width = config.BOARD_WIDTH

        # ---- Display Labels ----
        self.labels = {}

        self.labels["warmup"] = Label(
            text=f"Warm-up: {self.metronome_values['warm-up']}:00",
            size_hint=(1, 1), height=dp(40)
        )
        self.labels["bpm"] = Label(
            text=f"BPM: {self.metronome_values['bpm']}",
            size_hint=(1, 1), height=dp(40)
        )
        self.labels["run"] = Label(
            text=f"Run: {self.metronome_values['run_min']}:{self.format_seconds('run')}",
            size_hint=(1, 1), height=dp(40)
        )
        self.labels["rest"] = Label(
            text=f"Rest: {self.metronome_values['rest_min']}:{self.format_seconds('rest')}",
            size_hint=(1, 1), height=dp(40)
        )
        self.labels["cycles"] = Label(
            text=f"Cycles: {self.metronome_values['cycles']}",
            size_hint=(1, 1), height=dp(40)
        )
        self.labels["cooldown"] = Label(
            text=f"Cooldown: {self.metronome_values['cooldown']}:00",
            size_hint=(1, 1), height=dp(40)
        )

        for lbl in self.labels.values():
            self.add_widget(lbl)

        # ---- Buttons row ----
        button_layout = BoxLayout(
            orientation="horizontal",
            spacing=dp(66.5),
            size_hint=(1, None),
            height=dp(60)
        )

        button_width = dp(120)

        self.back_button = Button(
            text="Back",
            size_hint=(None, None),
            size=(button_width, dp(50))
        )
        self.back_button.bind(on_press=self.on_button_press)

        self.continue_button = Button(
            text="Continue",
            size_hint=(None, None),
            size=(button_width, dp(50))
        )
        self.continue_button.bind(on_press=self.on_button_press)

        button_layout.add_widget(self.back_button)
        button_layout.add_widget(self.continue_button)

        self.add_widget(button_layout)

    # ----------------------
    #   Helper Methods
    # ----------------------

    def format_seconds(self, str_type: str) -> str:
        value = self.metronome_values[f"{str_type}_sec"]
        return f"{value:02d}"  # always 2 digits

    def go_to_run(self):
        new_state = run_metronome.RunMetronome(self.app, self.metronome_values)
        self.app.enter_state(new_state)

    def on_button_press(self, instance):
        if instance.text == "Continue":
            self.go_to_run()
        elif instance.text == "Back":
            self.app.exit_state()
