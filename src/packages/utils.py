import logging

from packages import config
from kivy.utils import platform
from pathlib import Path
from kivy.uix.button import Button

# if platform == "android":
#     PROJECT_ROOT = Path(__file__).resolve().parent.parent
# else:
#     PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
#
# def get_directory(subfolder: str=""):
#     """Gets the full directory to the subfolder in data."""
#     data_dir = PROJECT_ROOT / "data"
#     if subfolder:
#         result = data_dir / subfolder
#         logging.debug("Getting directory for %s: %s",
#                       subfolder, result)
#         return result
#     return data_dir

logging.basicConfig(level=logging.DEBUG)

if platform == "android":
    PROJECT_ROOT = Path(__file__).resolve().parent.parent
else:
    PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

def get_directory(subfolder: str = ""):
    """Gets the full directory to the subfolder in data."""
    logging.info(f"Platform: {platform}")
    logging.info(f"__file__: {__file__}")
    logging.info(f"PROJECT_ROOT: {PROJECT_ROOT}")
    logging.info(f"PROJECT_ROOT exists: {PROJECT_ROOT.exists()}")
    logging.info(f"PROJECT_ROOT absolute: {PROJECT_ROOT.absolute()}")

    data_dir = PROJECT_ROOT / "data"
    logging.info(f"data_dir: {data_dir}")
    logging.info(f"data_dir exists: {data_dir.exists()}")

    # Android common paths
    if platform == "android":
        android_paths = [
            Path("/sdcard"),  # External storage
            Path("/storage/emulated/0"),  # Emulated external
            Path(__file__).resolve().parent,  # APK dir
            Path("/data/data/org.test.cadencebeat"),  # App private dir
            Path("/android_asset"),  # APK assets
        ]

        for path in android_paths:
            logging.info(f"Android check '{path}': exists={path.exists()}, abs={path.absolute()}")

    result = data_dir / subfolder if subfolder else data_dir
    logging.debug("Getting directory for %s: %s (exists: %s)", subfolder, result, result.exists())
    return result

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
