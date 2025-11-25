from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.slider import Slider as KivySlider
from kivy.uix.button import Button as KivyButton
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp

from states import state, review_metronome
from packages import utils, config


class NumberStepper(BoxLayout):
    """Kivy-adapted number stepper."""
    value = 0

    def __init__(self, min_value, max_value, step=1, name="", **kwargs):
        super().__init__(orientation="horizontal", spacing=dp(5), **kwargs)
        self.min_value = min_value
        self.max_value = max_value
        self.step = step
        self.value = min_value
        self.name = name

        self.minus_btn = KivyButton(text="-", size_hint=(0.3, 1))
        self.minus_btn.bind(on_press=lambda _: self.change_value(-self.step))
        self.plus_btn = KivyButton(text="+", size_hint=(0.3, 1))
        self.plus_btn.bind(on_press=lambda _: self.change_value(self.step))
        self.label = Label(text=f"{self.name}: {self.value}", size_hint=(0.4, 1))

        self.add_widget(self.minus_btn)
        self.add_widget(self.label)
        self.add_widget(self.plus_btn)

    def change_value(self, delta):
        self.value = max(self.min_value, min(self.max_value, self.value + delta))
        self.label.text = f"{self.name}: {self.value}"


class CreateMetronome(state.State):
    def __init__(self, app):
        super().__init__(app)

        # BPM Slider
        self.slider = KivySlider(min=150, max=220, value=150, size_hint=(None, None),
                                 size=(dp(200), dp(60)), pos=(dp((config.BOARD_WIDTH - 200)//2), dp(75)))

        # Steppers
        self.cycles_stepper = NumberStepper(1, 20, name="Cycles", size_hint=(None, None),
                                            size=(dp(125), dp(40)), pos=(dp(50), dp(160)))
        self.run_minutes_stepper = NumberStepper(0, 20, name="Minutes", size_hint=(None, None),
                                                 size=(dp(125), dp(40)), pos=(dp(50), dp(300)))
        self.run_seconds_stepper = NumberStepper(0, 60, step=10, name="Seconds", size_hint=(None, None),
                                                 size=(dp(125), dp(40)), pos=(dp(200), dp(300)))
        self.rest_minutes_stepper = NumberStepper(0, 20, name="Minutes", size_hint=(None, None),
                                                  size=(dp(125), dp(40)), pos=(dp(50), dp(450)))
        self.rest_seconds_stepper = NumberStepper(0, 60, step=10, name="Seconds", size_hint=(None, None),
                                                  size=(dp(125), dp(40)), pos=(dp(200), dp(450)))
        self.warmup_stepper = NumberStepper(0, 20, name="Warm-up", size_hint=(None, None),
                                            size=(dp(125), dp(40)), pos=(dp(50), dp(600)))
        self.cooldown_stepper = NumberStepper(0, 20, name="Cooldown", size_hint=(None, None),
                                              size=(dp(125), dp(40)), pos=(dp(200), dp(600)))

        # Buttons
        self.back_button = utils.get_back_button()
        self.continue_button = utils.get_continue_button()

        # Add widgets to app's layout
        app.root.add_widget(self.slider)
        for stepper in [self.cycles_stepper, self.run_minutes_stepper, self.run_seconds_stepper,
                        self.rest_minutes_stepper, self.rest_seconds_stepper,
                        self.warmup_stepper, self.cooldown_stepper]:
            app.root.add_widget(stepper)
        app.root.add_widget(self.back_button)
        app.root.add_widget(self.continue_button)

        # Bind buttons
        self.back_button.bind(on_press=lambda *_: self.exit_state())
        self.continue_button.bind(on_press=lambda *_: self.go_to_review())

    def go_to_review(self):
        values = self.get_values()
        new_state = review_metronome.ReviewMetronome(self.app, values)
        new_state.enter_state()

    def get_values(self):
        return {
            "bpm": int(self.slider.value),
            "warm-up": self.warmup_stepper.value,
            "run_min": self.run_minutes_stepper.value,
            "run_sec": self.run_seconds_stepper.value,
            "rest_min": self.rest_minutes_stepper.value,
            "rest_sec": self.rest_seconds_stepper.value,
            "cycles": self.cycles_stepper.value,
            "cooldown": self.cooldown_stepper.value,
        }
