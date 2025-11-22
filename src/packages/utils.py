import os
import pygame

from packages import config, button_object


def get_default_font(
    size: int = config.DEFAULT_FONT_SIZE,
    font_type: str = config.DEFAULT_FONT_TYPE
) -> pygame.font.Font:
    return pygame.font.SysFont(font_type, size)


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
    font = None
    for i, button_text in enumerate(sorted(button_names, key=len, reverse=True)):
        space_rect = space_rect.copy()
        space_rect.y += 2 * height
        buttons.append(button_object.Button(space_rect, button_text, font=font))
        if i == 0:
            font = buttons[-1].font
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