from states import state, create_metronome
from packages import  utils


class StartMenu(state.State):

    def __init__(self, app):
        state.State.__init__(self, app)
        self.buttons = utils.assign_buttons_to_space(self.app.screen.get_rect(),
                                                     ["Create Metronome", "Settings", "Quit"])

    def update(self, variables):
        for button in self.buttons:
            if button.is_clicked(self.app):
                if button.text == "Create Metronome":
                    new_state = create_metronome.CreateMetronome(self.app)
                    new_state.enter_state()
                elif button.text == "Settings":
                    print("set")
                elif button.text == "Quit":
                    self.app.running = False

    def render(self, surface):
        for button in self.buttons:
            button.draw(surface)
