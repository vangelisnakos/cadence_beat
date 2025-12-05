import logging
from packages import config
from pathlib import Path
from kivy.uix.button import Button


PROJECT_ROOT = Path(__file__).resolve().parent.parent

def get_directory(subfolder: str=""):
    """Gets the full directory to the subfolder in data."""
    data_dir = PROJECT_ROOT / "data"
    if subfolder:
        result = data_dir / subfolder
        logging.debug("Getting directory for %s: %s",
                      subfolder, result)
        return result
    return data_dir


def get_back_button() -> Button:
    """Returns positioned back Button."""
    return Button(
        text="Back",
        size_hint=(None, None),
        size=(config.BUTTON_WIDTH, config.BUTTON_HEIGHT),
        pos_hint={"x": config.BUTTON_X_PAD, "y": config.BUTTON_Y_PAD}
    )


def get_continue_button() -> Button:
    """Returns positioned continue Button."""
    return Button(
        text="Continue",
        size_hint=(None, None),
        size=(config.BUTTON_WIDTH, config.BUTTON_HEIGHT),
        pos_hint={"right": 1 - config.BUTTON_X_PAD, "y": config.BUTTON_Y_PAD}
    )
