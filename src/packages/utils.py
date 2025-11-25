import os
from kivy.uix.button import Button as KivyButton
from kivy.core.text import Label as CoreLabel
from kivy.metrics import dp
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty

from packages import config


def get_directory(directory_name: str = ""):
    """Return the path to the data directory within the project."""
    base_directory = cut_at_folder()
    if not directory_name:
        return base_directory
    else:
        return os.path.join(base_directory, f"data/{directory_name}")


def cut_at_folder():
    """Returns the absolute path up to the 'cadence_beat' folder."""
    norm = os.path.normpath(os.getcwd())
    parts = norm.split(os.sep)
    idx = parts.index("cadence_beat")
    return os.sep.join(parts[:idx + 1])


def assign_buttons_to_space(space_widget: Widget, button_names: list[str], x_division: int = 3):
    """
    Returns Kivy Buttons arranged inside a Widget's space.
    """
    width = space_widget.width / x_division
    height = space_widget.height / (2 * len(button_names) + 2)
    x = (space_widget.width - width) / 2
    y = space_widget.y + 0.5 * height
    buttons = []
    for i, button_text in enumerate(sorted(button_names, key=len, reverse=True)):
        btn = KivyButton(
            text=button_text,
            size=(width, height),
            pos=(x, y + i * 2 * height)
        )
        buttons.append(btn)
    return buttons


def get_back_button():
    """Returns the back button in the right-bottom corner."""
    width = config.BOARD_WIDTH // 5
    height = dp(50)
    free_corner_space = config.BOARD_WIDTH * 0.05
    x = config.BOARD_WIDTH - free_corner_space - width
    y = free_corner_space
    return KivyButton(text="Back", size=(width, height), pos=(x, y))


def get_continue_button():
    """Returns the continue button in the left-bottom corner."""
    width = config.BOARD_WIDTH // 5 + 25
    height = dp(50)
    free_corner_space = config.BOARD_WIDTH * 0.05
    x = free_corner_space
    y = free_corner_space
    return KivyButton(text="Continue", size=(width, height), pos=(x, y))


def get_pause_button():
    """Returns the pause button in the right-top corner."""
    width = config.BOARD_WIDTH // 5 + 10
    height = dp(50)
    free_corner_space = config.BOARD_WIDTH * 0.05
    x = config.BOARD_WIDTH - free_corner_space - width
    y = config.BOARD_HEIGHT - free_corner_space - height
    return KivyButton(text="Pause", size=(width, height), pos=(x, y))


def get_font_given_size(text: str, max_width: float, max_height: float, font_name: str = config.DEFAULT_FONT_TYPE):
    """
    Returns a CoreLabel with a font size such that text fits within given dimensions.
    """
    font_size = 200
    label = None
    while font_size > 1:
        label = CoreLabel(text=text, font_size=font_size, font_name=font_name)
        label.refresh()
        if label.texture.size[0] <= max_width and label.texture.size[1] <= max_height:
            return label
        font_size -= 1
    return label
