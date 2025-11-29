from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp

class Stepper(BoxLayout):
    def __init__(self, min_value=0, max_value=10, step=1, start_value=None,
                 label_name="", size_hint=(None, None), width=200, height=100, **kwargs):
        super().__init__(orientation="vertical", spacing=5, size_hint=size_hint, **kwargs)
        self.min_value = min_value
        self.max_value = max_value
        self.step = step
        self.value = start_value if start_value is not None else self.min_value
        self.label_name = label_name

        self.top_label = Label(
            text=self.label_name,
            size_hint=(None, None),
            width=width,
            height=20
        )
        self.add_widget(self.top_label)

        self.middle_layout = BoxLayout(orientation="horizontal", spacing=5, size_hint=(None, None),
                                       width=width, height=50)

        self.btn_up = Button(text="+", size_hint=(None, 1), width=dp(40))
        self.btn_up.bind(on_press=self.increment)
        self.middle_layout.add_widget(self.btn_up)

        self.value_label = Label(
            text=str(self.value),
            size_hint=(None, 1),
            width=dp(60)
        )
        self.middle_layout.add_widget(self.value_label)

        self.btn_down = Button(text="-", size_hint=(None, 1), width=dp(40))
        self.btn_down.bind(on_press=self.decrement)
        self.middle_layout.add_widget(self.btn_down)
        self.add_widget(self.middle_layout)

        self.width = width
        self.height = height

    def increment(self, instance):
        self.value = min(self.max_value, self.value + self.step)
        self.value_label.text = str(self.value)

    def decrement(self, instance):
        self.value = max(self.min_value, self.value - self.step)
        self.value_label.text = str(self.value)
