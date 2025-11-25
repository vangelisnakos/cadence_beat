from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Ellipse
from kivy.properties import NumericProperty, StringProperty
from packages import config
from kivy.core.text import Label as CoreLabel


class Slider(Widget):
    value = NumericProperty(0)
    name = StringProperty("")

    def __init__(
        self,
        pos,
        size,
        min_value: int,
        max_value: int,
        bar_color: tuple = config.BUTTON_COLOR_HOVER,
        handle_color: tuple = config.BUTTON_COLOR,
        text_color: tuple = config.WHITE,
        border_radius: int = 8,
        name: str = "",
        **kwargs
    ):
        super().__init__(**kwargs)
        self.pos = pos
        self.size = size
        self.min_value = min_value
        self.max_value = max_value
        self.value = min_value
        self.name = name
        self.bar_color = bar_color
        self.handle_color = handle_color
        self.text_color = text_color
        self.border_radius = border_radius
        self.ball_radius = self.size[1] // 8
        self.padding = self.ball_radius * 2

        # Graphics
        with self.canvas:
            self.bg_color_inst = Color(*self.bar_color)
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)

            self.line_color_inst = Color(*config.GREY)
            self.line_rect = Rectangle(pos=(self.pos[0]+self.padding, self.pos[1]+self.size[1]/2 - 1),
                                       size=(self.size[0]-2*self.padding, 3))

            self.handle_color_inst = Color(*self.handle_color)
            hx, hy = self._handle_pos()
            self.handle = Ellipse(pos=(hx - self.ball_radius, hy - self.ball_radius),
                                  size=(self.ball_radius*2, self.ball_radius*2))

            self.value_label = CoreLabel(text=f"{self.name}: {self.value}", font_size=16)
            self.value_label.refresh()
            self.value_rect = Rectangle(
                texture=self.value_label.texture,
                pos=(self.pos[0] + (self.size[0]-self.value_label.texture.size[0])/2,
                     self.pos[1] + self.size[1] + 5),
                size=self.value_label.texture.size
            )

        self.bind(pos=self._update_graphics, size=self._update_graphics, value=self._update_value_label)

    def _handle_pos(self):
        padded_width = self.size[0] - 2 * self.padding
        ratio = (self.value - self.min_value) / (self.max_value - self.min_value)
        x = self.pos[0] + self.padding + ratio * padded_width
        y = self.pos[1] + self.size[1] / 2
        return int(x), int(y)

    def _update_graphics(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        self.line_rect.pos = (self.pos[0]+self.padding, self.pos[1]+self.size[1]/2 - 1)
        self.line_rect.size = (self.size[0]-2*self.padding, 3)
        self._update_handle()
        self._update_value_label()

    def _update_handle(self):
        hx, hy = self._handle_pos()
        self.handle.pos = (hx - self.ball_radius, hy - self.ball_radius)
        self.handle.size = (self.ball_radius*2, self.ball_radius*2)

    def _update_value_label(self, *args):
        self.value_label.text = f"{self.name}: {self.value}"
        self.value_label.refresh()
        self.value_rect.texture = self.value_label.texture
        self.value_rect.pos = (self.pos[0] + (self.size[0]-self.value_label.texture.size[0])/2,
                               self.pos[1] + self.size[1] + 5)
        self.value_rect.size = self.value_label.texture.size

    def on_touch_down(self, touch):
        if self._touch_on_handle(touch.pos):
            self._update_value_from_touch(touch.x)
            return True
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if self._touch_on_handle(touch.pos) or self._touch_on_line(touch.pos):
            self._update_value_from_touch(touch.x)
            return True
        return super().on_touch_move(touch)

    def _update_value_from_touch(self, touch_x):
        padded_width = self.size[0] - 2 * self.padding
        ratio = max(0, min(1, (touch_x - (self.pos[0] + self.padding)) / padded_width))
        self.value = int(ratio * (self.max_value - self.min_value) + self.min_value)

    def _touch_on_handle(self, touch_pos):
        hx, hy = self._handle_pos()
        x, y = touch_pos
        return (hx - x)**2 + (hy - y)**2 <= self.ball_radius**2

    def _touch_on_line(self, touch_pos):
        x, y = touch_pos
        return (self.pos[1] <= y <= self.pos[1] + self.size[1] and
                self.pos[0] <= x <= self.pos[0] + self.size[0])
