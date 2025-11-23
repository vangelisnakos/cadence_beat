import os
import pygame

from packages import config, button_object


def get_default_font(
    size: int = config.DEFAULT_FONT_SIZE,
    font_type: str = config.DEFAULT_FONT_TYPE
) -> pygame.font.Font:
    return pygame.font.SysFont(font_type, size)

def get_font_given_rect_and_text(rect: pygame.Rect, text: str) -> pygame.font.Font:
    """Returns font with a size such that text fits in the rect."""
    font_size = 200
    font = None
    while font_size > 1:
        font = get_default_font(size=font_size)
        text_width, text_height = font.size(text)
        if text_width + 5 <= rect.width and text_height + 5 <= rect.height:
            return font
        font_size -= 1
    return font

def get_blit_text(rect: pygame.Rect, text: str, font: pygame.font.Font | None = None):
    """Draws text in the rect."""
    text_font = font or get_font_given_rect_and_text(rect, text)
    text_surf = text_font.render(text, True, config.WHITE)
    text_rect = text_surf.get_rect(center=rect.center)
    return text_surf, text_rect


def cut_at_folder():
    norm = os.path.normpath(os.getcwd())
    parts = norm.split(os.sep)
    idx = parts.index("cadence_beat")
    return os.sep.join(parts[:idx + 1])


def get_directory(directory_name: str = ""):
    base_directory = cut_at_folder()
    if not directory_name:
        return base_directory
    else:
        return os.path.join(base_directory, f"data\\{directory_name}")

def align_button_font_size(*buttons: button_object.Button):
    """Sets the font size of all buttons equal to the lowest."""
    min_size = min(button.font.point_size for button in buttons)
    for button in buttons:
        button.font.point_size = min_size


def assign_buttons_to_space(
    space_rect: pygame.Rect,
    button_names: list[str],
    x_division: int = 3,
) -> list:
    """Returns Buttons given some space."""
    width, height = space_rect.width // x_division, space_rect.height // (2 * len(button_names) + 2)
    space_rect.x += (space_rect.width - width) / 2
    space_rect.y -= 0.5 * height
    space_rect.width = width
    space_rect.height = height
    buttons = []
    for i, button_text in enumerate(sorted(button_names, key=len, reverse=True)):
        space_rect = space_rect.copy()
        space_rect.y += 2 * height
        buttons.append(button_object.Button(space_rect, button_text))
    align_button_font_size(*buttons)
    return buttons


def get_back_button() -> button_object.Button:
    """Returns the back button in the right-bottom corner."""
    width = config.BOARD_WIDTH // 5
    height = 50
    free_corner_space = 0.05 * config.BOARD_WIDTH
    x = config.BOARD_WIDTH - free_corner_space - width
    y = config.BOARD_HEIGHT - free_corner_space - height
    button_rect = pygame.Rect(x, y, width, height)
    return button_object.Button(button_rect, "Back")


def get_continue_button() -> button_object.Button:
    """Returns the continue button in the left-bottom corner."""
    width = config.BOARD_WIDTH // 5 + 25
    height = 50
    free_corner_space = 0.05 * config.BOARD_WIDTH
    x = free_corner_space
    y = config.BOARD_HEIGHT - free_corner_space - height
    button_rect = pygame.Rect(x, y, width, height)
    return button_object.Button(button_rect, "Continue")


def get_pause_button() -> button_object.Button:
    """Returns the pause button in the right-top corner."""
    width = config.BOARD_WIDTH // 5 + 10
    height = 50
    free_corner_space = 0.05 * config.BOARD_WIDTH
    x = config.BOARD_WIDTH - free_corner_space - width
    y = free_corner_space
    button_rect = pygame.Rect(x, y, width, height)
    return button_object.Button(button_rect, "Pause")