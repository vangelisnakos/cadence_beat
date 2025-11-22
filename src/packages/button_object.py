import pygame

from packages import config

class Button:
    def __init__(
        self,
        rect: pygame.Rect,
        text: str,
        color: tuple = config.BUTTON_COLOR,
        hover_color: tuple = config.BUTTON_COLOR_HOVER,
        text_color: tuple = config.WHITE,
        border_radius: int = 12,
        font: pygame.font.Font | None = None
    ):
        self.rect = rect
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.font = font or self.get_font()
        self.border_radius = border_radius

        self.clicked = False

    def get_font(self) -> pygame.font.Font:
        from packages import utils

        return utils.get_font_given_rect_and_text(self.rect, self.text)

    def draw_shadow(self, surface):
        shadow_offset = 4
        shadow_rect = self.rect.move(shadow_offset, shadow_offset)
        pygame.draw.rect(surface, config.BLACK, shadow_rect, border_radius=self.border_radius)

    def draw_background(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        current_color = self.hover_color if self.rect.collidepoint(mouse_pos) else self.color
        pygame.draw.rect(surface, current_color, self.rect, border_radius=self.border_radius)

    def draw_edge(self, surface):
        pygame.draw.rect(surface,  config.WHITE, self.rect, width=2, border_radius=self.border_radius)

    def draw_text(self, surface):
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def draw(self, surface):
        self.draw_shadow(surface)
        self.draw_background(surface)
        self.draw_edge(surface)
        self.draw_text(surface)

    def is_clicked(self, app):
        self.clicked = False
        if app.right_click:
            mouse_pos = pygame.mouse.get_pos()
            if self.rect.collidepoint(mouse_pos):
                app.right_click = False
                self.clicked = True
        return self.clicked
