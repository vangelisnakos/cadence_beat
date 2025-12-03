from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp

class Stepper(BoxLayout):
    def __init__(self, min_value: int=0, max_value: int=10, step: int=1, start_value=None,
                 label_name: str="", size_hint=(None, None), width=dp(200), height=dp(100), **kwargs):
        super().__init__(orientation="vertical", spacing=dp(10), size_hint=size_hint, **kwargs)
        self.min_value = min_value
        self.max_value = max_value
        self.step = step
        self.value = start_value if start_value is not None else self.min_value
        self.label_name = label_name

        # Top label with center alignment
        self.top_label = Label(
            text=self.label_name,
            size_hint=(1, None),
            height=dp(30),
            halign="center",
            valign="middle",
            font_size=18,
            bold=True
        )
        self.top_label.bind(size=self.top_label.setter('text_size'))
        self.add_widget(self.top_label)

        # Middle layout with buttons and value
        self.middle_layout = BoxLayout(
            orientation="horizontal",
            spacing=dp(10),
            size_hint=(1, None),
            height=dp(50)
        )

        # Decrement button (on the left)
        self.btn_down = Button(
            text="-",
            size_hint=(None, 1),
            width=dp(50),
            font_size=24
        )
        self.btn_down.bind(on_press=self.decrement)
        self.middle_layout.add_widget(self.btn_down)

        # Value label in the center
        self.value_label = Label(
            text=str(self.value),
            size_hint=(None, 1),
            width=dp(40),
            halign="center",
            valign="middle",
            font_size=22,
            bold=True
        )
        self.value_label.bind(size=self.value_label.setter('text_size'))
        self.middle_layout.add_widget(self.value_label)

        # Increment button (on the right)
        self.btn_up = Button(
            text="+",
            size_hint=(None, 1),
            width=dp(50),
            font_size=24
        )
        self.btn_up.bind(on_press=self.increment)
        self.middle_layout.add_widget(self.btn_up)

        self.add_widget(self.middle_layout)

        self.width = width
        self.height = height

    def increment(self, instance):
        if self.value < self.max_value:
            self.value = min(self.max_value, self.value + self.step)
            self.value_label.text = str(self.value)

    def decrement(self, instance):
        if self.value > self.min_value:
            self.value = max(self.min_value, self.value - self.step)
            self.value_label.text = str(self.value)
