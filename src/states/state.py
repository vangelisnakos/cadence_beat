from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget


class State(FloatLayout):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app

    def enter_state(self):
        if self.app.current_state is not None:
            self.app.remove_widget(self.app.current_state)
        self.app.add_widget(self)
        self.app.current_state = self

    def exit_state(self):
        self.app.remove_widget(self)
