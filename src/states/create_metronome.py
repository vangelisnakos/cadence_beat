import pygame

from states import state
from packages import  slider_object, utils


class CreateMetronome(state.State):

    def __init__(self, app):
        state.State.__init__(self, app)
        slider_rect = pygame.Rect(75, 150, 250, 75)
        self.slider = slider_object.Slider(slider_rect, 100, 200)
        self.back_button = utils.get_back_button()
        self.continue_button = 0

    def update(self, variables):
        self.slider.update(self.app.right_click)
        if self.back_button.is_clicked(self.app.right_click):
            self.exit_state()

    def render(self, surface):
        self.slider.draw(self.app.screen)
        self.back_button.draw(surface)
