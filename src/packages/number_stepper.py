import pygame

from packages import config, utils

class NumberStepper:
    def __init__(
        self,
        rect: pygame.Rect,
        min_value: int,
        max_value: int,
        step: int = 1,
        bg_color: tuple = config.BUTTON_COLOR_HOVER,
        text_color: tuple = config.WHITE,
        border_color: tuple = config.BUTTON_COLOR,
        border_radius: int = 8,
        font: pygame.font.Font | None = None,
        name: str = ""
    ):
        self.rect = rect
        self.min_value = min_value
        self.max_value = max_value
        self.step = step
        self.value = 0
        self.font = font or utils.get_default_font(size=config.DEFAULT_FONT_SIZE - 2)
        self.name = name
        self.name_font = utils.get_font_given_rect_and_text(self.rect, self.name)

        w = rect.width
        h = rect.height
        free_space = 0.05 * h
        y = rect.y + free_space
        self.btn_size = h - 2 * free_space
        self.minus_rect = pygame.Rect(rect.x + free_space, y, self.btn_size, self.btn_size)
        self.plus_rect = pygame.Rect(rect.right - self.btn_size - free_space, y, self.btn_size, self.btn_size)
        self.text_rect = pygame.Rect(rect.x + self.btn_size, y, w - 2*self.btn_size, self.btn_size)

        self.bg_color = bg_color
        self.text_color = text_color
        self.border_color = border_color
        self.border_radius = border_radius

        self._held_button = None

    def change_value(self, delta):
        self.value = max(self.min_value, min(self.max_value, self.value + delta))

    def draw_shadow(self, surface):
        shadow_offset = 4
        shadow_rect = self.rect.move(shadow_offset, shadow_offset)
        pygame.draw.rect(surface, config.BLACK, shadow_rect, border_radius=self.border_radius)

    def draw_background(self, surface):
        pygame.draw.rect(surface, self.bg_color, self.rect, border_radius=self.border_radius)

    def draw_edge(self, surface):
        pygame.draw.rect(surface,  config.WHITE, self.rect, width=2, border_radius=self.border_radius)

    def draw_button(self, surface, button: str):
        if button == "-":
            rect = self.minus_rect
        else:
            rect = self.plus_rect
        pygame.draw.rect(surface, self.border_color, rect, border_radius=self.border_radius)
        minus_surf = self.font.render(button, True, self.text_color)
        surface.blit(
            minus_surf,
            minus_surf.get_rect(center=rect.center)
        )

    def draw_value(self, surface):
        val_surf = self.font.render(str(self.value), True, self.text_color)
        surface.blit(
            val_surf,
            val_surf.get_rect(center=self.text_rect.center)
        )

    def draw_name(self, surface):
        text_surf = self.name_font.render(self.name, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        text_rect.y -= self.rect.height
        surface.blit(text_surf, text_rect)

    def draw(self, surface, font):
        self.draw_shadow(surface)
        self.draw_background(surface)
        self.draw_edge(surface)

        self.draw_button(surface, "-")
        self.draw_button(surface, "+")

        self.draw_value(surface)
        self.draw_name(surface)

    def update(self, app):
        mx, my = pygame.mouse.get_pos()

        if app.right_click:
            if self.minus_rect.collidepoint(mx, my):
                self._held_button = "minus"
                self.change_value(-self.step)
                app.right_click = False
            elif self.plus_rect.collidepoint(mx, my):
                self._held_button = "plus"
                self.change_value(self.step)
                app.right_click = False
        else:
            self._held_button = None
