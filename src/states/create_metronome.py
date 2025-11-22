import pygame

from states import state
from packages import  slider_object, utils, number_stepper, config


class CreateMetronome(state.State):
    slider_width = 250
    slider_height = 75

    stepper_width = 150
    stepper_height = 50

    def __init__(self, app):
        state.State.__init__(self, app)
        slider_x = config.BOARD_WIDTH - 3 * self.slider_width // 2
        slider_rect = pygame.Rect(slider_x, 100, self.slider_width, self.slider_height)
        self.slider = slider_object.Slider(slider_rect, 100, 200, name="BPM")

        stepper_horizontal_space = (config.BOARD_WIDTH - 2 * self.stepper_width) // 3
        minutes_x = stepper_horizontal_space
        seconds_x = 2 * stepper_horizontal_space + self.stepper_width

        self.run_title_rect = pygame.Rect(minutes_x, 215, seconds_x + self.stepper_width - minutes_x, 50)
        run_minutes_stepper_rect = pygame.Rect(minutes_x, 300, self.stepper_width, self.stepper_height)
        self.run_minutes_stepper = number_stepper.NumberStepper(run_minutes_stepper_rect, 0, 20, name="minutes")
        run_seconds_stepper_rect = pygame.Rect(seconds_x, 300, self.stepper_width, self.stepper_height)
        self.run_seconds_stepper = number_stepper.NumberStepper(run_seconds_stepper_rect, 0, 20, name="seconds")

        self.rest_title_rect = pygame.Rect(minutes_x, 365, seconds_x + self.stepper_width - minutes_x, 50)
        rest_minutes_stepper_rect = pygame.Rect(minutes_x, 450, self.stepper_width, self.stepper_height)
        self.rest_minutes_stepper = number_stepper.NumberStepper(rest_minutes_stepper_rect, 0, 20, name="minutes")
        rest_seconds_stepper_rect = pygame.Rect(seconds_x, 450, self.stepper_width, self.stepper_height)
        self.rest_seconds_stepper = number_stepper.NumberStepper(rest_seconds_stepper_rect, 0, 20, name="seconds")

        self.back_button = utils.get_back_button()
        self.continue_button = utils.get_continue_button()
        utils.align_button_font_size(self.back_button, self.continue_button)

    def update(self, variables):
        self.slider.update(self.app.right_click)
        self.run_minutes_stepper.update(self.app)
        self.run_seconds_stepper.update(self.app)
        self.rest_minutes_stepper.update(self.app)
        self.rest_seconds_stepper.update(self.app)

        if self.continue_button.is_clicked(self.app.right_click):
            print(self.get_values())
        if self.back_button.is_clicked(self.app.right_click):
            self.exit_state()

    def render(self, surface):
        self.slider.draw(self.app.screen)

        utils.blit_text(self.run_title_rect, "-Run Time-", surface)
        self.run_minutes_stepper.draw(self.app.screen, utils.get_default_font())
        self.run_seconds_stepper.draw(self.app.screen, utils.get_default_font())

        utils.blit_text(self.rest_title_rect, "-Rest Time-", surface)
        self.rest_minutes_stepper.draw(self.app.screen, utils.get_default_font())
        self.rest_seconds_stepper.draw(self.app.screen, utils.get_default_font())

        self.continue_button.draw(surface)
        self.back_button.draw(surface)

    def get_values(self):
        return {
            "bpm": self.slider.value,
            "run_min": self.run_minutes_stepper.value,
            "run_sec": self.run_seconds_stepper.value,
            "rest_min": self.rest_minutes_stepper.value,
            "rest_sec": self.rest_seconds_stepper.value,
        }
