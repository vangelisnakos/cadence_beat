import pygame

from states import state, run_metronome
from packages import  utils, config


class ReviewMetronome(state.State):

    def __init__(self, app, metronome_values: dict[str, int]):
        state.State.__init__(self, app)
        self.metronome_values = metronome_values

        horizontal_space = config.BOARD_WIDTH / 3
        vertical_space = (config.BOARD_HEIGHT - 100) / 7
        self.bpm_rect = pygame.Rect(horizontal_space, vertical_space, horizontal_space, vertical_space)
        self.run_rect = pygame.Rect(horizontal_space, 3 * vertical_space, horizontal_space, vertical_space)
        self.rest_rect = pygame.Rect(horizontal_space, 5 * vertical_space, horizontal_space, vertical_space)

        bpm_text = f"BPM: {self.metronome_values['bpm']}"
        self.bpm_text_details = utils.get_blit_text(self.bpm_rect, bpm_text)
        run_text = f"Run: {self.metronome_values['run_min']}:{self.get_seconds("run")}"
        self.run_text_details = utils.get_blit_text(self.run_rect, run_text)
        rest_text = f"Rest: {self.metronome_values['rest_min']}:{self.get_seconds("rest")}"
        self.rest_text_details = utils.get_blit_text(self.rest_rect, rest_text)

        self.back_button = utils.get_back_button()
        self.continue_button = utils.get_continue_button()
        utils.align_button_font_size(self.back_button, self.continue_button)

    def update(self, variables):
        if self.continue_button.is_clicked(self.app.right_click):
            new_state = run_metronome.RunMetronome(self.app, self.metronome_values)
            new_state.enter_state()
        if self.back_button.is_clicked(self.app.right_click):
            self.exit_state()

    def render(self, surface):
        surface.blit(*self.bpm_text_details)
        surface.blit(*self.run_text_details)
        surface.blit(*self.rest_text_details)

        self.continue_button.draw(surface)
        self.back_button.draw(surface)

    def get_seconds(self, str_type: str) -> str:
        value = self.metronome_values[f'{str_type}_sec']
        if value < 10:
            return f"0{value}"
        return str(value)
