import logging

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.metrics import dp


from states import create_metronome

class StartMenu(FloatLayout):
    def __init__(self, app):
        FloatLayout.__init__(self, size_hint=(1,1))
        self.app = app

        self.layout = BoxLayout(
            orientation="vertical",
            spacing=dp(50),
            padding=dp(50),
            size_hint=(0.8, None),
            height=dp(240),
            pos_hint={"center_x": 0.5, "center_y": 0.425}
        )

        self.buttons = []
        for text in ["Create Metronome", "Settings", "Quit"]:
            btn = Button(
                text=text,
                size_hint=(1, None),
                height=dp(60)
            )
            btn.bind(on_press=self.on_button_press)
            self.layout.add_widget(btn)
            self.buttons.append(btn)

        self.add_widget(self.layout)

    def on_button_press(self, instance):
        logging.debug("Tapped on '%s'", instance.text)
        if instance.text == "Create Metronome":
            new_state = create_metronome.CreateMetronome(self.app)
            self.app.enter_state(new_state)
        elif instance.text == "Settings":
            print("Settings")
        elif instance.text == "Quit":
            App.get_running_app().stop()
        else:
            logging.error("Unknown button name: %s", instance.text)
