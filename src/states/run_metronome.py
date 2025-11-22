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

        self.warmuping = True
        self.cooldowning = True
        self.interval = 60.0 / metronome_values["bpm"]
        self.warmup = 60 * metronome_values["warm-up"]
        self.cooldown = 60 * metronome_values["cooldown"]
        self.cycles = metronome_values["cycles"]
        self.current_cycle = 1
        self.next_tick = time.time()
        self.start_time = self.next_tick
        self.remaining = metronome_values["run_min"] * 60 + metronome_values["run_sec"]

        self.running = False
        self.run_duration = self.remaining
        self.run_timer_rect = pygame.Rect(config.BOARD_WIDTH // 4, config.BOARD_HEIGHT // 2, config.BOARD_WIDTH // 2, config.BOARD_HEIGHT)
        self.run_timer_font = utils.get_font_given_rect_and_text(self.run_timer_rect, self.get_elapsed_run_time())

        self.resting = False
        self.rest_duration = metronome_values["rest_min"] * 60 + metronome_values["rest_sec"]

        self.back_button = utils.get_back_button()

    def update(self, variables):
        if self.warmuping:
            self.play("warmup", self.warmup)
        elif self.running:
            self.play("run", self.run_duration)
        elif self.resting:
            self.play("rest", self.rest_duration)
        if self.current_cycle > self.cycles:
            self.resting = False
            self.running = False
            self.play("cooldown", self.cooldown)

        if self.back_button.is_clicked(self.app) or not self.cooldowning:
            self.running = False
            self.exit_state()
            self.exit_state()

    def render(self, surface):
        if self.running:
            surface.blit(self.run_image)
        elif self.resting:
            surface.blit(self.rest_image)
        text_surface = self.run_timer_font.render(self.get_elapsed_run_time(), True, config.WHITE)
        surface.blit(text_surface, self.run_timer_rect)

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

    def play(self, timer_type: str, duration: int):
        now = time.time()
        self.update_timer(duration, now)
        self.advance_phase(timer_type, now)
        self.play_tick_non_blocking(now)

    def update_timer(self, duration: int, now: float):
        elapsed = now - self.start_time
        self.remaining = max(0, int(duration - elapsed))

    def advance_phase(self, timer_type: str, now: float):
        if self.remaining > 0:
            return

        self.start_time = now
        self.next_tick = now

        if timer_type == "warmup":
            self.running = True
            self.warmuping = False
        elif timer_type == "run":
            self.running = False
            self.resting = True
        elif timer_type == "rest":
            self.running = True
            self.resting = False
            self.current_cycle += 1
        else:
            self.cooldowning = False

    def play_tick_non_blocking(self, now):
        if now >= self.next_tick:
            if self.running:
                self.sound.play()

            self.next_tick += self.interval
