import pygame

from states import state, review_metronome
from packages import  slider_object, utils, number_stepper, config


class CreateMetronome(state.State):
    slider_width = 200
    slider_height = 60

    stepper_width = 125
    stepper_height = 40

    def __init__(self, app):
        state.State.__init__(self, app)
        slider_x = (config.BOARD_WIDTH - self.slider_width) // 2
        slider_rect = pygame.Rect(slider_x, 75, self.slider_width, self.slider_height)
        self.slider = slider_object.Slider(slider_rect, 150, 220, name="BPM")

        stepper_horizontal_space = (config.BOARD_WIDTH - 2 * self.stepper_width) // 3
        minutes_x = 0.8 * stepper_horizontal_space
        seconds_x = 2 * stepper_horizontal_space + self.stepper_width
        self.font = utils.get_default_font()

        self.cycles_title_rect = pygame.Rect(minutes_x, 160, seconds_x - minutes_x, self.stepper_height)
        self.cycles_text_details = utils.get_blit_text(self.cycles_title_rect, "Cycles: ")
        cycles_stepper_rect = pygame.Rect(seconds_x, 160, self.stepper_width, self.stepper_height)
        self.cycles_stepper = number_stepper.NumberStepper(cycles_stepper_rect, 1, 20)

        self.run_title_rect = pygame.Rect(minutes_x, 215, seconds_x + self.stepper_width - minutes_x, 50)
        self.run_text_details = utils.get_blit_text(self.run_title_rect, "- Run Time -")
        run_minutes_stepper_rect = pygame.Rect(minutes_x, 300, self.stepper_width, self.stepper_height)
        self.run_minutes_stepper = number_stepper.NumberStepper(run_minutes_stepper_rect, 0, 20, name="minutes")
        run_seconds_stepper_rect = pygame.Rect(seconds_x, 300, self.stepper_width, self.stepper_height)
        self.run_seconds_stepper = number_stepper.NumberStepper(run_seconds_stepper_rect, 0, 60, name="seconds", step=10)

        self.rest_title_rect = pygame.Rect(minutes_x, 365, seconds_x + self.stepper_width - minutes_x, 50)
        self.rest_text_details = utils.get_blit_text(self.rest_title_rect, "- Rest Time -")
        rest_minutes_stepper_rect = pygame.Rect(minutes_x, 450, self.stepper_width, self.stepper_height)
        self.rest_minutes_stepper = number_stepper.NumberStepper(rest_minutes_stepper_rect, 0, 20, name="minutes")
        rest_seconds_stepper_rect = pygame.Rect(seconds_x, 450, self.stepper_width, self.stepper_height)
        self.rest_seconds_stepper = number_stepper.NumberStepper(rest_seconds_stepper_rect, 0, 60, name="seconds", step=10)

        self.prepare_title_rect = pygame.Rect(minutes_x, 515, seconds_x + self.stepper_width - minutes_x, 50)
        self.prepare_text_details = utils.get_blit_text(self.prepare_title_rect, "- Prepare -")
        warmup_stepper_rect = pygame.Rect(minutes_x, 600, self.stepper_width, self.stepper_height)
        self.warmup_stepper = number_stepper.NumberStepper(warmup_stepper_rect, 0, 20, name="warm-up")
        cooldown_stepper_rect = pygame.Rect(seconds_x, 600, self.stepper_width, self.stepper_height)
        self.cooldown_stepper = number_stepper.NumberStepper(cooldown_stepper_rect, 0, 20, name="cooldown")

        self.back_button = utils.get_back_button()
        self.continue_button = utils.get_continue_button()
        utils.align_button_font_size(self.back_button, self.continue_button)

    def update(self, variables):
        self.slider.update(self.app.right_click)
        self.run_minutes_stepper.update(self.app)
        self.run_seconds_stepper.update(self.app)
        self.rest_minutes_stepper.update(self.app)
        self.rest_seconds_stepper.update(self.app)
        self.warmup_stepper.update(self.app)
        self.cooldown_stepper.update(self.app)
        self.cycles_stepper.update(self.app)

        if self.continue_button.is_clicked(self.app):
            new_state = review_metronome.ReviewMetronome(self.app, self.get_values())
            new_state.enter_state()
        if self.back_button.is_clicked(self.app):
            self.exit_state()

    def render(self, surface):
        self.slider.draw(self.app.screen)

        surface.blit(*self.cycles_text_details)
        self.cycles_stepper.draw(self.app.screen, self.font)

        surface.blit(*self.run_text_details)
        self.run_minutes_stepper.draw(self.app.screen, self.font)
        self.run_seconds_stepper.draw(self.app.screen, self.font)

        surface.blit(*self.rest_text_details)
        self.rest_minutes_stepper.draw(self.app.screen, self.font)
        self.rest_seconds_stepper.draw(self.app.screen, self.font)

        surface.blit(*self.prepare_text_details)
        self.warmup_stepper.draw(self.app.screen, self.font)
        self.cooldown_stepper.draw(self.app.screen, self.font)

        self.continue_button.draw(surface)
        self.back_button.draw(surface)

    def get_values(self):
        return {
            "bpm": self.slider.value,
            "warm-up": self.warmup_stepper.value,
            "run_min": self.run_minutes_stepper.value,
            "run_sec": self.run_seconds_stepper.value,
            "rest_min": self.rest_minutes_stepper.value,
            "rest_sec": self.rest_seconds_stepper.value,
            "cycles": self.cycles_stepper.value,
            "cooldown": self.cooldown_stepper.value,
        }
