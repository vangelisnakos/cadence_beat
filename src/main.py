import os
from kivy.app import App
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from pathlib import Path

KV_PATH = Path(__file__).parent / "packages" / "label.kv"
Builder.load_file(str(KV_PATH))
KV_PATH2 = Path(__file__).parent / "packages" / "button.kv"
Builder.load_file(str(KV_PATH2))

from states import start_menu
from packages import config, utils


class MainWidget(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tap_detected = False
        self.back_pressed = False
        self.bg_image = None
        self.states_stack = []

        self.create_window()
        self.create_main_background()

        start_menu_state = start_menu.StartMenu(self)
        self.enter_state(start_menu_state)

    def on_key_down(self, window, key, scancode, codepoint, modifiers):
        if key == 27:
            self.back_pressed = True
            return True
        return False

    def on_touch_down(self, touch):
        self.tap_detected = True
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        self.tap_detected = False
        return super().on_touch_up(touch)

    def create_window(self):
        Window.size = (config.BOARD_WIDTH, config.BOARD_HEIGHT)
        Window.title = "CadenceBeat"
        Window.bind(on_key_down=self.on_key_down)

    def create_main_background(self):
        image_directory = utils.get_directory("images") / "menu_background.png"
        self.bg_image = Image(source=str(image_directory), allow_stretch=True, keep_ratio=False)
        self.add_widget(self.bg_image, index=0)

    def enter_state(self, new_state):
        for state in self.states_stack:
            if state in self.children:
                self.remove_widget(state)
        self.add_widget(new_state)
        self.states_stack.append(new_state)

    def exit_state(self):
        for state in self.states_stack:
            if state in self.children:
                self.remove_widget(state)
        self.states_stack.pop()
        new_state = self.add_widget(self.states_stack[-1])
        if new_state is not None:
            self.add_widget(new_state)

class CadenceApp(App):
    def build(self):
        return MainWidget()


if __name__ == "__main__":
    CadenceApp().run()
