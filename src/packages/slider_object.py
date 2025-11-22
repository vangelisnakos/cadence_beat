import pygame

from packages import config, utils

class Slider:
    def __init__(
        self,
        rect: pygame.Rect,
        min_value: int,
        max_value: int,
        bar_color: tuple = config.BUTTON_COLOR_HOVER,
        handle_color: tuple = config.BUTTON_COLOR,
        border_radius: int = 8,
    ):
        self.rect = rect
        self.min_value = min_value
        self.max_value = max_value
        self.value = min_value
        self.bar_color = bar_color
        self.handle_color = handle_color
        self.border_radius = border_radius
        self.ball_radius = self.rect.height // 8
        self.padding = self.ball_radius * 2

    def handle_pos(self):
        padded_width = self.rect.width - 2 * self.padding
        ratio = (self.value - self.min_value) / (self.max_value - self.min_value)
        x = self.rect.x + self.padding + ratio * padded_width
        y = self.rect.y + self.rect.height // 2
        return int(x), int(y)

    def draw_shadow(self, surface):
        shadow_offset = 4
        shadow_rect = self.rect.move(shadow_offset, shadow_offset)
        pygame.draw.rect(surface, config.BLACK, shadow_rect, border_radius=self.border_radius)

    def draw_background(self, surface):
        pygame.draw.rect(surface, self.bar_color, self.rect, border_radius=self.border_radius)

    def draw_edge(self, surface):
        pygame.draw.rect(surface,  config.WHITE, self.rect, width=2, border_radius=self.border_radius)

    def draw_line(self, surface):
        line_y = self.rect.y + self.rect.height // 2
        start_pos = (self.rect.x + self.padding, line_y)
        end_pos = (self.rect.x + self.rect.width - self.padding, line_y)
        line_color = config.GREY
        pygame.draw.line(surface, line_color, start_pos, end_pos, 3)

    def draw_ball(self, surface):
        hx, hy = self.handle_pos()
        pygame.draw.circle(surface, self.handle_color, (hx, hy), self.ball_radius)

    def draw_value(self, surface):
        font = utils.get_default_font()
        value_surf = font.render(str(self.value), True, self.handle_color)
        surface.blit(value_surf, (self.rect.right * 1.01, self.rect.y + self.rect.height // 2 - font.get_height() // 2))

    def draw(self, surface):
        pygame.draw.rect(surface, self.bar_color, self.rect, border_radius=self.border_radius)

        self.draw_shadow(surface)
        self.draw_background(surface)
        self.draw_edge(surface)

        self.draw_line(surface)
        self.draw_ball(surface)
        self.draw_value(surface)

    def update(self, is_right_click: bool):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        padded_width = self.rect.width - 2 * self.padding
        ratio = max(0, min(1, (mouse_x - (self.rect.x + self.padding)) / padded_width))
        is_mouse_on_slider = (mouse_x - self.handle_pos()[0]) ** 2 + (mouse_y - self.handle_pos()[1]) ** 2 <= (
                    self.rect.height // 2 + 2) ** 2
        dragging = is_right_click and is_mouse_on_slider
        if dragging:
            self.value = int(ratio * (self.max_value - self.min_value) + self.min_value)
