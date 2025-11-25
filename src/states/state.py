class State:
    def __init__(self, app):
        self.app = app
        self.prev_state = None
        self.widgets = []

    def update(self, variables):
        pass

    def render(self, surface=None):
        pass

    def enter_state(self):
        if len(self.app.state_stack) > 0:
            self.prev_state = self.app.state_stack[-1]
        self.app.state_stack.append(self)
        for widget in getattr(self, "widgets", []):
            self.app.root.add_widget(widget)

    def exit_state(self):
        self.app.state_stack.pop()
        for widget in getattr(self, "widgets", []):
            if widget.parent:
                self.app.root.remove_widget(widget)
