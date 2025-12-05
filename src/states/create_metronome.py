from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button

from packages import config, number_stepper, slider_object, utils
from states import review_metronome


class CreateMetronome(FloatLayout):
    def __init__(self, app):
        FloatLayout.__init__(self)
        self.app = app

        self.orientation = "vertical"
        self.spacing = dp(25)
        self.padding = dp(20)

        # --- BPM Slider ---
        self.bpm_slider = slider_object.LabeledSlider(
            min_value=60,
            max_value=220,
            value=180,
            step=1,
            label_text="BPM",
            size_hint=(0.9, None),
            height=dp(100),
            pos_hint={'center_x': 0.5, 'y': 0.85}
        )
        self.add_widget(self.bpm_slider)

        # --- Stepper sizing ---
        stepper_width = dp(100)
        stepper_height = dp(30) # Might need this

        # --- Stepper instances ---
        self.warmup_stepper = number_stepper.Stepper(
            0, 20, start_value=0, label_name="Warm-up"
        )
        self.cooldown_stepper = number_stepper.Stepper(
            0, 20, start_value=0, label_name="Cooldown"
        )
        self.run_minutes_stepper = number_stepper.Stepper(
            0, 20, start_value=0, label_name="Minutes"
        )
        self.run_seconds_stepper = number_stepper.Stepper(
            0,
            60,
            step=10,
            start_value=0,
            label_name="Seconds",
        )
        self.rest_minutes_stepper = number_stepper.Stepper(
            0, 20, start_value=0, label_name="Minutes"
        )
        self.rest_seconds_stepper = number_stepper.Stepper(
            0,
            60,
            step=10,
            start_value=0,
            label_name="Seconds",
        )
        self.cycles_stepper = number_stepper.Stepper(
            1, 20, start_value=1, label_name="Cycles"
        )

        # --- Helper for horizontal pairs ---
        def pair(left, right):
            h = BoxLayout(
                orientation="horizontal",
                spacing=dp(20),
                size_hint=(1, None),
                height=stepper_height,
                padding=[dp(20), 0, dp(20), 0],
            )
            left.size_hint_x = 0.5
            right.size_hint_x = 0.5
            h.add_widget(left)
            h.add_widget(right)
            return h

        # --- Vertical positioning ---
        # Warmup / Cooldown row
        pair1 = pair(self.warmup_stepper, self.cooldown_stepper)
        pair1.pos_hint={'center_x': 0.5, 'y': 0.7}
        self.add_widget(pair1)

        # Run minutes / Run seconds
        pair2 = pair(self.run_minutes_stepper, self.run_seconds_stepper)
        pair2.pos_hint={'center_x': 0.5, 'y': 0.55}
        self.add_widget(pair2)

        # Rest minutes / Rest seconds
        pair3 = pair(self.rest_minutes_stepper, self.rest_seconds_stepper)
        pair3.pos_hint={'center_x': 0.5, 'y': 0.4}
        self.add_widget(pair3)

        # Cycles stepper centered
        self.cycles_stepper.pos_hint={'center_x': 0.5, 'y': 0.25}
        self.add_widget(self.cycles_stepper)

        # --- Buttons ---
        self.back_button = utils.get_back_button()
        self.back_button.bind(on_press=self.on_button_press)

        self.continue_button = utils.get_continue_button()
        self.continue_button.bind(on_press=self.on_button_press)

        self.add_widget(self.back_button)
        self.add_widget(self.continue_button)


    def get_values(self):
        return {
            "bpm": int(self.bpm_slider.get_value()),
            "warm-up": self.warmup_stepper.value,
            "run_min": self.run_minutes_stepper.value,
            "run_sec": self.run_seconds_stepper.value,
            "rest_min": self.rest_minutes_stepper.value,
            "rest_sec": self.rest_seconds_stepper.value,
            "cycles": self.cycles_stepper.value,
            "cooldown": self.cooldown_stepper.value,
        }

    def go_to_review(self):
        values = self.get_values()
        new_state = review_metronome.ReviewMetronome(self.app, values)
        self.app.enter_state(new_state)

    def on_button_press(self, instance):
        if instance.text == "Continue":
            self.go_to_review()
        elif instance.text == "Back":
            self.app.exit_state()
