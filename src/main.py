import os
import pygame

from states import start_menu
from packages import config, utils

class Main:

    def __init__(
        self,
    ):
        pygame.init()
        area = (config.BOARD_WIDTH, config.BOARD_HEIGHT)
        self.screen = pygame.display.set_mode(area)
        pygame.display.set_caption("CadenceBeat")
        self.timer = pygame.time.Clock()

        self.running = True
        self.state_stack = []
        self.start_screen = None

        self.load_states()

        image_directory = os.path.join(utils.get_directory("images"), "menu_background.png")
        self.image = pygame.image.load(image_directory)

        self.right_click = False
        self.esc_pressed = False

    def game_loop(self):
        while self.running:
            self.timer.tick(config.FPS)
            self.get_events()
            self.render()
            self.update()

        pygame.quit()

    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.right_click = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.right_click = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.esc_pressed = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.esc_pressed = False

    def update(self):
        self.state_stack[-1].update(None)
        pygame.display.flip()

    def render(self):
        self.draw_background()
        self.state_stack[-1].render(self.screen)

    def load_states(self):
        self.start_screen = start_menu.StartMenu(self)
        self.state_stack.append(self.start_screen)

    def draw_background(self):
        self.screen.blit(self.image)



if __name__ == "__main__":
    game = Main()
    game.game_loop()
