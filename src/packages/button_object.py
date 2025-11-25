from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.label import Label
from kivy.core.text import Label as CoreLabel
from kivy.properties import BooleanProperty
from packages import config


class Button(Widget):
    clicked = BooleanProperty(False)

    def __init__(
        self,
        pos,
        size,
        text: str,
        color: tuple = config.BUTTON_COLOR,
        hover_color: tuple = config.BUTTON_COLOR_HOVER,
        text_color: tuple = config.WHITE,
        border_radius: int = 12,
        **kwargs
    ):
        super().__init__(**kwargs)
        self.pos = pos
        self.size = size
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.border_radius = border_radius

        self._touch_down = False

        # Draw the button
        with self.canvas:
            self.bg_color = Color(*self.color)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[self.border_radius])
            self.label_color = Color(*self.text_color)
            self.label = CoreLabel(text=self.text, font_size=20)
            self.label.refresh()
            texture = self.label.texture
            self.label_rect = RoundedRectangle(
                texture=texture,
                pos=(self.pos[0] + (self.size[0] - texture.size[0]) / 2,
                     self.pos[1] + (self.size[1] - texture.size[1]) / 2),
                size=texture.size
            )

        # Bind pos/size changes to update graphics
        self.bind(pos=self._update_graphics, size=self._update_graphics)

    def _update_graphics(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        self.label.refresh()
        texture = self.label.texture
        self.label_rect.texture = texture
        self.label_rect.pos = (
            self.pos[0] + (self.size[0] - texture.size[0]) / 2,
            self.pos[1] + (self.size[1] - texture.size[1]) / 2
        )
        self.label_rect.size = texture.size

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self._touch_down = True
            self.bg_color.rgb = self.hover_color[:3]
            return True
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if self._touch_down and self.collide_point(*touch.pos):
            self.clicked = True
        self._touch_down = False
        self.bg_color.rgb = self.color[:3]
        return super().on_touch_up(touch)

    def is_clicked(self):
        if self.clicked:
            self.clicked = False
            return True
        return False
