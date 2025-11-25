from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle
from kivy.core.text import Label as CoreLabel
from kivy.properties import NumericProperty, StringProperty
from packages import config


class NumberStepper(Widget):
    value = NumericProperty(0)
    name = StringProperty("")

    def __init__(
        self,
        pos,
        size,
        min_value: int,
        max_value: int,
        step: int = 1,
        bg_color: tuple = config.BUTTON_COLOR_HOVER,
        text_color: tuple = config.WHITE,
        border_color: tuple = config.BUTTON_COLOR,
        border_radius: int = 8,
        name: str = "",
        **kwargs
    ):
        super().__init__(**kwargs)
        self.pos = pos
        self.size = size
        self.min_value = min_value
        self.max_value = max_value
        self.step = step
        self.bg_color = bg_color
        self.text_color = text_color
        self.border_color = border_color
        self.border_radius = border_radius
        self.name = name
        self.value = min_value

        # Calculate button sizes
        w, h = size
        free_space = 0.05 * h
        y = pos[1] + free_space
        btn_size = h - 2 * free_space
        self.minus_pos = (pos[0] + free_space, y)
        self.plus_pos = (pos[0] + w - btn_size - free_space, y)
        self.btn_size = btn_size
        self.text_pos = (pos[0] + btn_size, y)
        self.text_size = (w - 2 * btn_size, btn_size)

        # Graphics
        with self.canvas:
            self.bg_color_inst = Color(*self.bg_color)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[self.border_radius])
            self.border_color_inst = Color(*self.border_color)
            self.border_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[self.border_radius])

            # Buttons
            self.minus_color_inst = Color(*self.border_color)
            self.minus_rect = RoundedRectangle(pos=self.minus_pos, size=(btn_size, btn_size), radius=[self.border_radius])
            self.plus_color_inst = Color(*self.border_color)
            self.plus_rect = RoundedRectangle(pos=self.plus_pos, size=(btn_size, btn_size), radius=[self.border_radius])

            # Labels
            self.value_label = CoreLabel(text=str(self.value), font_size=20)
            self.value_label.refresh()
            self.value_rect = RoundedRectangle(
                texture=self.value_label.texture,
                pos=(self.text_pos[0] + (self.text_size[0] - self.value_label.texture.size[0])/2,
                     self.text_pos[1] + (self.text_size[1] - self.value_label.texture.size[1])/2),
                size=self.value_label.texture.size
            )

            self.name_label = CoreLabel(text=self.name, font_size=16)
            self.name_label.refresh()
            self.name_rect = RoundedRectangle(
                texture=self.name_label.texture,
                pos=(pos[0] + (w - self.name_label.texture.size[0])/2, pos[1] + h + 5),
                size=self.name_label.texture.size
            )

        self.bind(pos=self._update_graphics, size=self._update_graphics, value=self._update_value_label)

    def _update_graphics(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        self.border_rect.pos = self.pos
        self.border_rect.size = self.size

        self.minus_rect.pos = self.minus_pos
        self.plus_rect.pos = self.plus_pos
        self.minus_rect.size = (self.btn_size, self.btn_size)
        self.plus_rect.size = (self.btn_size, self.btn_size)

        self._update_value_label()

    def _update_value_label(self, *args):
        self.value_label.text = str(self.value)
        self.value_label.refresh()
        self.value_rect.texture = self.value_label.texture
        self.value_rect.pos = (
            self.text_pos[0] + (self.text_size[0] - self.value_label.texture.size[0])/2,
            self.text_pos[1] + (self.text_size[1] - self.value_label.texture.size[1])/2
        )
        self.value_rect.size = self.value_label.texture.size

    def on_touch_down(self, touch):
        if self._touch_in_rect(touch.pos, self.minus_pos, self.btn_size):
            self.value = max(self.min_value, self.value - self.step)
            return True
        elif self._touch_in_rect(touch.pos, self.plus_pos, self.btn_size):
            self.value = min(self.max_value, self.value + self.step)
            return True
        return super().on_touch_down(touch)

    @staticmethod
    def _touch_in_rect(pos, rect_pos, size):
        x, y = pos
        rx, ry = rect_pos
        return rx <= x <= rx + size and ry <= y <= ry + size
