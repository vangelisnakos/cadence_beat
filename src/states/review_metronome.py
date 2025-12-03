from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp

from packages import config
from states import run_metronome


class ReviewMetronome(BoxLayout):
    def __init__(self, app, metronome_values: dict[str, int]):
        super().__init__()
        self.app = app
        self.metronome_values = metronome_values

        self.orientation = "vertical"
        self.spacing = dp(25)
        self.padding = dp(20)

        # ---- Display Labels ----
        self.labels = {"warmup": Label(
            text=f"Warm-up: {self.metronome_values['warm-up']}:00",
            size_hint=(1, None), height=dp(40),
            halign="center", valign="middle"
        ), "bpm": Label(
            text=f"BPM: {self.metronome_values['bpm']}",
            size_hint=(1, None), height=dp(40),
            halign="center", valign="middle"
        ), "run": Label(
            text=f"Run: {self.metronome_values['run_min']}:{self.format_seconds('run')}",
            size_hint=(1, None), height=dp(40),
            halign="center", valign="middle"
        ), "rest": Label(
            text=f"Rest: {self.metronome_values['rest_min']}:{self.format_seconds('rest')}",
            size_hint=(1, None), height=dp(40),
            halign="center", valign="middle"
        ), "cycles": Label(
            text=f"Cycles: {self.metronome_values['cycles']}",
            size_hint=(1, None), height=dp(40),
            halign="center", valign="middle"
        ), "cooldown": Label(
            text=f"Cooldown: {self.metronome_values['cooldown']}:00",
            size_hint=(1, None), height=dp(40),
            halign="center", valign="middle"
        )}

        for lbl in self.labels.values():
            lbl.bind(size=lbl.setter('text_size'))
            self.add_widget(lbl)

        # Add spacer to push buttons to bottom
        self.add_widget(BoxLayout(size_hint=(1, 1)))

        # ---- Buttons row ----
        button_layout = BoxLayout(
            orientation="horizontal",
            spacing=dp(20),
            size_hint=(1, None),
            height=dp(60)
        )

        self.back_button = Button(
            text="Back",
            size_hint=(None, None),
            size=(config.BUTTON_WIDTH, config.BUTTON_HEIGHT)
        )
        self.back_button.bind(on_press=self.on_button_press)

        self.continue_button = Button(
            text="Continue",
            size_hint=(None, None),
            size=(config.BUTTON_WIDTH, config.BUTTON_HEIGHT)
        )
        self.continue_button.bind(on_press=self.on_button_press)

        button_layout.add_widget(self.back_button)
        button_layout.add_widget(BoxLayout(size_hint=(1, 1)))  # Spacer between buttons
        button_layout.add_widget(self.continue_button)

        self.add_widget(button_layout)

    def format_seconds(self, str_type: str) -> str:
        value = self.metronome_values[f"{str_type}_sec"]
        return f"{value:02d}"

    def on_button_press(self, instance):
        if instance.text == "Continue":
            new_state = run_metronome.RunMetronome(self.app, self.metronome_values)
            self.app.enter_state(new_state)
        elif instance.text == "Back":
            self.app.exit_state()
