from kivy.metrics import dp

FPS = 60

BOARD_WIDTH = 346
BOARD_HEIGHT = 750

BUTTON_WIDTH = dp(120)
BUTTON_HEIGHT = dp(50)
BUTTON_X_PAD = 0.05
BUTTON_Y_PAD = 0.02

DEFAULT_FONT_SIZE = 40
DEFAULT_FONT_TYPE = "arialblack"
SEC_IN_MIN = 60

def rgb(c):
    return tuple(v / 255 for v in c)

WHITE = rgb((255, 255, 255))
BLACK = rgb((0, 0, 0))
GREY  = rgb((200, 200, 200))
BUTTON_COLOR = rgb((180, 150, 20))
BUTTON_COLOR_HOVER = rgb((220, 190, 40))
