import os
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.base import EventLoop

from states import start_menu
from packages import config, utils


class MainWidget(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.size = (config.BOARD_WIDTH, config.BOARD_HEIGHT)
        Window.title = "CadenceBeat"

        self.state_stack = []
        self.start_screen = None
        self.tap_detected = False
        self.back_pressed = False

        self.load_states()

        # Load background image
        image_directory = os.path.join(utils.get_directory("images"), "menu_background.png")
        self.bg_image = Image(source=image_directory, allow_stretch=True, keep_ratio=False)
        self.add_widget(self.bg_image)

        # Schedule update loop
        Clock.schedule_interval(self.update, 1.0 / config.FPS)

        # Keyboard/back button events
        Window.bind(on_key_down=self.on_key_down)

    def load_states(self):
        self.start_screen = start_menu.StartMenu(self)
        self.state_stack.append(self.start_screen)

    # Back button handler
    def on_key_down(self, window, key, scancode, codepoint, modifiers):
        if key == 27:  # Android back button
            self.back_pressed = True
            # Optional: override default behavior
            return True
        return False

    # Touch events (tap detection)
    def on_touch_down(self, touch):
        self.tap_detected = True
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        self.tap_detected = False
        return super().on_touch_up(touch)

    def update(self, dt):
        # Call the current state's update
        if self.state_stack:
            self.state_stack[-1].update(dt)

    def render(self):
        # Kivy auto-updates UI, just call state's render if needed
        if self.state_stack:
            self.state_stack[-1].render(self)


class CadenceApp(App):
    def build(self):
        return MainWidget()


if __name__ == "__main__":
    CadenceApp().run()
