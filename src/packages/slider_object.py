from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.slider import Slider as KivySlider

class LabeledSlider(BoxLayout):
    def __init__(self, min_value=0, max_value=100, value=None, step=1,
                 label_text="", pos=None, **kwargs):
        kwargs.setdefault('size_hint', (None, None))
        super().__init__(orientation="vertical", spacing=5, padding=10, **kwargs)

        self.min = min_value
        self.max = max_value
        self.step = step
        self.value = value if value is not None else self.min
        self.label_text = label_text

        # Top label with centered text
        self.slider_label = Label(
            text=f"{self.label_text}: {int(self.value)}",
            size_hint=(1, None),
            height=dp(25),
            halign="center",
            valign="bottom",
            font_size=20,
            bold=True
        )
        self.slider_label.bind(size=self.slider_label.setter('text_size'))
        self.add_widget(self.slider_label)

        # Slider with bigger cursor
        self.slider = KivySlider(
            min=self.min,
            max=self.max,
            value=self.value,
            step=self.step,
            size_hint=(1, None),
            height=dp(50),
            cursor_size=(dp(30), dp(30))
        )
        self.slider.bind(value=self.on_slider_value)
        self.add_widget(self.slider)

        if pos:
            self.pos = pos

        if 'width' in kwargs:
            self.width = kwargs['width']
        if 'height' in kwargs:
            self.height = kwargs['height']

    def on_slider_value(self, instance, value):
        self.slider_label.text = f"{self.label_text}: {int(value)}"
        self.value = value

    def get_value(self):
        return self.slider.value

    def set_value(self, value):
        if self.min <= value <= self.max:
            self.slider.value = value
