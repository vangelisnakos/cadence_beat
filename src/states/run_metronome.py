import os
import time
import pygame

from states import state
from packages import  utils, config


class RunMetronome(state.State):

    def __init__(self, app, metronome_values: dict[str, int]):
        state.State.__init__(self, app)
        self.metronome_values = metronome_values
        self.interval = 60.0 / metronome_values["bpm"]

        self.images = {
            "run": pygame.image.load(os.path.join(utils.get_directory("images"), "run_background.png")),
            "rest": pygame.image.load(os.path.join(utils.get_directory("images"), "rest_background.png")),
        }
        pygame.mixer.init()
        self.sound = self.load_sound()
        self.countdown_sound = self.load_sound(sound_name="countdown")
        self.countdown_started  = False

        self.phases = self.build_phases(metronome_values)
        self.current_phase_index = 0
        self.start_time = time.time()
        self.next_tick = self.start_time

        self.back_button = utils.get_back_button()
        self.continue_button = utils.get_continue_button()
        self.pause_button = utils.get_pause_button()

        self.paused = False
        self.pause_start = None
        self.accumulated_pause = 0

        self.font = utils.get_default_font(size=35)
        self.run_timer_rect = pygame.Rect(
            config.BOARD_WIDTH // 8, config.BOARD_HEIGHT // 10,
            3 * config.BOARD_WIDTH // 4, config.BOARD_HEIGHT // 3
        )
        self.time_font = utils.get_font_given_rect_and_text(self.run_timer_rect, "0:00")
        self.current_phase_rect = pygame.Rect(
            config.BOARD_WIDTH // 8, config.BOARD_HEIGHT // 2,
            3 * config.BOARD_WIDTH // 4, config.BOARD_HEIGHT // 5
        )
        self.next_phase_rect = pygame.Rect(
            config.BOARD_WIDTH // 8, 3 * config.BOARD_HEIGHT // 5,
            3 * config.BOARD_WIDTH // 4, config.BOARD_HEIGHT // 5
        )
        self.cycles_rect = pygame.Rect(
            config.BOARD_WIDTH // 8, 7 * config.BOARD_HEIGHT // 10,
            3 * config.BOARD_WIDTH // 4, config.BOARD_HEIGHT // 5
        )

    @staticmethod
    def build_phases(metronome_values):
        phases = []

        if metronome_values["warm-up"] > 0:
            phases.append(("Warm-up", metronome_values["warm-up"] * 60, False))

        run_dur = metronome_values["run_min"] * 60 + metronome_values["run_sec"]
        rest_dur = metronome_values["rest_min"] * 60 + metronome_values["rest_sec"]
        for _ in range(metronome_values["cycles"]):
            phases.append(("Run", run_dur, True))
            phases.append(("Rest", rest_dur, False))

        if metronome_values["cooldown"] > 0:
            phases.append(("Cooldown", metronome_values["cooldown"] * 60, False))

        return phases

    def update(self, variables):
        now = time.time()

        if self.pause_button.is_clicked(self.app):
            self.toggle_pause(now)

        if self.paused:
            return

        phase_name, duration, ticking = self.phases[self.current_phase_index]

        remaining = self.get_remaining_time(now)

        if remaining == 5 and not self.countdown_started:
            self.countdown_sound.play()
            self.countdown_started = True

        if remaining == 0:
            self.advance_phase(now)
            return

        if ticking and now >= self.next_tick:
            self.sound.play()
            self.next_tick += self.interval

        if self.back_button.is_clicked(self.app):
            self.go_back_phase(now)

        if self.continue_button.is_clicked(self.app):
            if self.paused:
                self.toggle_pause(now)  # resume
            else:
                self.advance_phase(now)

        if self.app.esc_pressed:
            self.exit_state()
            self.exit_state()


    def render(self, surface):
        name, duration, _ = self.phases[self.current_phase_index]
        remaining = self.get_remaining_time()

        if name.lower() in self.images:
            surface.blit(self.images[name.lower()])

        minutes = remaining // 60
        seconds = remaining % 60
        time_str = f"{minutes}:{seconds:02d}"
        text_surface = self.time_font.render(time_str, True, config.WHITE)
        surface.blit(text_surface, self.run_timer_rect)

        phase_str = f"{name}: {duration//60}:{duration%60:02d}"
        text_surface = self.font.render(phase_str, True, config.WHITE)
        surface.blit(text_surface, self.current_phase_rect)

        if self.current_phase_index + 1 < len(self.phases):
            next_name, duration, _ = self.phases[self.current_phase_index + 1]
            next_phase_str = f"{next_name}: {duration//60}:{duration%60:02d}"
            text_surface = self.font.render(next_phase_str, True, config.WHITE)
            surface.blit(text_surface, self.next_phase_rect)

        if name in ["Run", "Rest"]:
            current_cycle = self.get_current_cycle()
            total_cycles = self.metronome_values["cycles"]
            cycle_str = f"Cycle: {current_cycle}/{total_cycles}"
            text_surface = self.font.render(cycle_str, True, config.WHITE)
            surface.blit(text_surface, self.cycles_rect)

        self.back_button.draw(surface)
        self.continue_button.draw(surface)
        self.pause_button.draw(surface)

    def get_remaining_time(self, now=None):
        if now is None:
            now = time.time()

        phase_name, duration, _ = self.phases[self.current_phase_index]

        if self.paused:
            elapsed = (self.pause_start - self.start_time) - self.accumulated_pause
        else:
            elapsed = (now - self.start_time) - self.accumulated_pause

        remaining = max(0, int(duration - elapsed))
        return remaining

    @staticmethod
    def load_sound(sound_name: str = "basic"):
        base_directory = utils.cut_at_folder()
        sounds_directory = os.path.join(base_directory, "data\sounds")
        sound = pygame.mixer.Sound(os.path.join(sounds_directory, sound_name + ".mp3"))
        return sound

    def get_current_cycle(self):
        count = 0
        for i, (name, _, _) in enumerate(self.phases):
            if name == "Run" and i <= self.current_phase_index:
                count += 1
        return max(1, min(count, self.metronome_values["cycles"]))

    def reset_phase(self, now):
        self.start_time = now
        self.next_tick = now
        self.accumulated_pause = 0
        self.countdown_started = False
        self.countdown_sound.stop()

    def advance_phase(self, now):
        self.reset_phase(now)
        self.current_phase_index += 1

        if self.current_phase_index >= len(self.phases):
            self.exit_state()
            self.exit_state()

    def toggle_pause(self, now):
        if not self.paused:
            self.paused = True
            self.pause_start = now
        else:
            paused_for = now - self.pause_start
            self.accumulated_pause += paused_for
            self.paused = False
            self.pause_start = None

    def go_back_phase(self, now):
        if self.current_phase_index > 0:
            self.reset_phase(now)
            self.current_phase_index -= 1
        else:
            self.exit_state()
            self.exit_state()
