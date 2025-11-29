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

        parent_width = config.BOARD_WIDTH
        parent_height = config.BOARD_HEIGHT

        # --- BPM Slider ---
        slider_width = parent_width * 0.75
        self.bpm_slider = slider_object.LabeledSlider(
            min_value=60,
            max_value=220,
            value=180,
            step=1,
            label_text="BPM",
            width=slider_width,
            height=dp(100),
            pos=((parent_width - slider_width) / 2, dp(650)),
        )
        self.add_widget(self.bpm_slider)

        # --- Stepper sizing ---
        scale = 0.8
        stepper_width = dp(125) * scale
        stepper_height = dp(40) * scale

        # --- Stepper instances ---
        self.warmup_stepper = number_stepper.Stepper(
            0, 20, start_value=0, label_name="Warm-up", width=stepper_width, height=stepper_height
        )
        self.cooldown_stepper = number_stepper.Stepper(
            0, 20, start_value=0, label_name="Cooldown", width=stepper_width, height=stepper_height
        )
        self.run_minutes_stepper = number_stepper.Stepper(
            0, 20, start_value=0, label_name="Minutes", width=stepper_width, height=stepper_height
        )
        self.run_seconds_stepper = number_stepper.Stepper(
            0,
            60,
            step=10,
            start_value=0,
            label_name="Seconds",
            width=stepper_width,
            height=stepper_height,
        )
        self.rest_minutes_stepper = number_stepper.Stepper(
            0, 20, start_value=0, label_name="Minutes", width=stepper_width, height=stepper_height
        )
        self.rest_seconds_stepper = number_stepper.Stepper(
            0,
            60,
            step=10,
            start_value=0,
            label_name="Seconds",
            width=stepper_width,
            height=stepper_height,
        )
        self.cycles_stepper = number_stepper.Stepper(
            1, 20, start_value=1, label_name="Cycles", width=stepper_width, height=stepper_height
        )

        # --- Helper for horizontal pairs ---
        def pair(left, right):
            h = BoxLayout(
                orientation="horizontal",
                spacing=dp(20),
                size_hint=(None, None),
                width=parent_width,
                height=stepper_height,
                padding=[dp(20), 0, dp(20), 0],
            )
            left.size_hint_x = 0.5
            right.size_hint_x = 0.5
            h.add_widget(left)
            h.add_widget(right)
            return h

        # --- Vertical positioning ---
        vertical_start = dp(550)
        vertical_spacing = dp(100)

        # Warmup / Cooldown row
        pair1 = pair(self.warmup_stepper, self.cooldown_stepper)
        pair1.pos = (0, vertical_start)
        self.add_widget(pair1)

        # Run minutes / Run seconds
        pair2 = pair(self.run_minutes_stepper, self.run_seconds_stepper)
        pair2.pos = (0, vertical_start - vertical_spacing)
        self.add_widget(pair2)

        # Rest minutes / Rest seconds
        pair3 = pair(self.rest_minutes_stepper, self.rest_seconds_stepper)
        pair3.pos = (0, vertical_start - vertical_spacing * 2)
        self.add_widget(pair3)

        # Cycles stepper centered
        self.cycles_stepper.pos = (
            (parent_width - 1.5*stepper_width) / 2,
            vertical_start - vertical_spacing * 3,
        )
        self.add_widget(self.cycles_stepper)

        # --- Buttons ---
        button_width = dp(120)
        button_height = dp(50)

        self.back_button = Button(
            text="Back",
            size_hint=(None, None),
            size=(button_width, button_height),
            pos=(dp(20), dp(20)),
        )
        self.back_button.bind(on_press=self.on_button_press)

        self.continue_button = Button(
            text="Continue",
            size_hint=(None, None),
            size=(button_width, button_height),
            pos=(parent_width - button_width - dp(20), dp(20)),
        )
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
