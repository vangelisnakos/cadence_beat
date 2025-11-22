import os
import time
import pygame

from states import state
from packages import  utils, config


class RunMetronome(state.State):

    def __init__(self, app, metronome_values: dict[str, int]):
        state.State.__init__(self, app)
        self.metronome_values = metronome_values

        run_image_directory = os.path.join(utils.get_directory("images"), "run_background.png")
        self.run_image = pygame.image.load(run_image_directory)
        rest_image_directory = os.path.join(utils.get_directory("images"), "rest_background.png")
        self.rest_image = pygame.image.load(rest_image_directory)

        pygame.mixer.init()
        self.sound = self.load_sound()

        self.interval = 60.0 / metronome_values["bpm"]
        self.next_tick = time.time()
        self.start_time = self.next_tick
        self.next_print = self.start_time + 1
        self.remaining = metronome_values["run_min"] * 60 + metronome_values["run_sec"]

        self.running = True
        self.run_duration = self.remaining
        self.run_timer_rect = pygame.Rect(0, config.BOARD_HEIGHT // 3, config.BOARD_WIDTH // 3, config.BOARD_HEIGHT)
        self.run_timer_font = utils.get_font_given_rect_and_text(self.run_timer_rect, self.get_elapsed_run_time())

        self.resting = False
        self.rest_duration = metronome_values["rest_min"] * 60 + metronome_values["rest_sec"]
        self.rest_timer_rect = pygame.Rect(0, 2 * config.BOARD_HEIGHT // 3, config.BOARD_WIDTH // 3, config.BOARD_HEIGHT)
        self.rest_timer_font = utils.get_font_given_rect_and_text(self.run_timer_rect, self.get_elapsed_run_time())

        self.back_button = utils.get_back_button()

    def update(self, variables):
        if self.running:
            self.play("run")
        elif self.resting:
            self.play("rest")

        if self.back_button.is_clicked(self.app.right_click):
            self.running = False
            self.exit_state()

    def render(self, surface):
        if self.running:
            surface.blit(self.run_image)
            text_surface = self.run_timer_font.render(self.get_elapsed_run_time(), True, config.WHITE)
            surface.blit(text_surface, self.run_timer_rect)
        elif self.resting:
            surface.blit(self.rest_image)
            text_surface = self.rest_timer_font.render(self.get_elapsed_run_time(), True, config.WHITE)
            surface.blit(text_surface, self.rest_timer_rect)

        self.back_button.draw(surface)

    @staticmethod
    def load_sound(sound_name: str = "basic"):
        base_directory = utils.cut_at_folder()
        sounds_directory = os.path.join(base_directory, "data\sounds")
        sound = pygame.mixer.Sound(os.path.join(sounds_directory, sound_name + ".mp3"))
        return sound

    def get_elapsed_run_time(self):
        minutes = self.remaining // 60
        seconds = self.remaining % 60
        if seconds < 10:
            seconds = f"0{int(seconds)}"
        return f"{int(minutes)}:{seconds}"

    def play(self, timer_type: str):
        now = time.time()
        self.update_timer(timer_type, now)
        self.advance_phase(timer_type, now)
        self.play_tick(timer_type, now)

    def update_timer(self, timer_type: str, now: float):
        elapsed = now - self.start_time
        duration = self.run_duration if timer_type == "run" else self.rest_duration
        self.remaining = max(0, int(duration - elapsed))

    def advance_phase(self, timer_type: str, now: float):
        if self.remaining > 0:
            return

        self.start_time = now
        self.next_tick = now

        if timer_type == "run":
            self.running = False
            self.resting = True
        else:
            self.running = True
            self.resting = False

    def play_tick(self, timer_type: str, now: float):
        if now >= self.next_print:
            self.next_print += 1

        if timer_type == "run":
            self.sound.play()

        self.next_tick += self.interval
        sleep_time = self.next_tick - time.time()
        if sleep_time > 0:
            time.sleep(sleep_time)

