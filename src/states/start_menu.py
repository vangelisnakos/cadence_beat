from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button as KivyButton
from kivy.uix.floatlayout import FloatLayout

from states import state, create_metronome

class StartMenu(state.State, FloatLayout):
    def __init__(self, app):
        # Initialize both parent classes properly
        state.State.__init__(self, app)
        FloatLayout.__init__(self)

        # Vertical layout for the menu buttons
        self.layout = BoxLayout(orientation="vertical", spacing=20, padding=50, size_hint=(1, None))
        self.layout.bind(minimum_height=self.layout.setter('height'))  # adjust height dynamically

        # Create Kivy buttons
        self.buttons = []
        button_texts = ["Create Metronome", "Settings", "Quit"]
        for text in button_texts:
            btn = KivyButton(text=text, size_hint=(1, None), height=60)
            btn.bind(on_press=self.on_button_press)
            self.layout.add_widget(btn)
            self.buttons.append(btn)

        # Add layout to the FloatLayout
        self.add_widget(self.layout)
        # self.app.add_widget(self.layout)

    def on_button_press(self, instance):
        if instance.text == "Create Metronome":
            new_state = create_metronome.CreateMetronome(self.app)
            new_state.enter_state()
        elif instance.text == "Settings":
            print("Settings pressed")
        elif instance.text == "Quit":
            self.app.running = False


    # With Kivy, update/render methods are largely handled by the framework
    # So you can keep update empty or use it for extra logic
    def update(self, variables):
        pass

    def render(self, surface=None):
        pass
