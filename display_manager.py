import displayio
import terminalio
from adafruit_display_text import label
import i2cdisplaybus
import adafruit_displayio_ssd1306
import config

class DisplayManager:

    def __init__(self, i2c):
        # Initialize OLED display
        displayio.release_displays()
        bus = i2cdisplaybus.I2CDisplayBus(i2c, device_address=0x3C)

        self.display = adafruit_displayio_ssd1306.SSD1306(
            bus, width=128, height=64
        )
        self.root = displayio.Group()
        self.display.root_group = self.root

    # ----------- MENU SCREEN -----------
    def show_menu(self, diffs, index):
        g = displayio.Group()
        self.display.root_group = g

        g.append(label.Label(terminalio.FONT, text="SELECT", x=4, y=10))
        for i, d in enumerate(diffs):
            prefix = ">" if i == index else " "
            g.append(label.Label(terminalio.FONT, text=f"{prefix} {d['name']}", x=4, y=24 + 12*i))

    # ----------- GAME STEP DISPLAY -----------
    def show_level(self, level, step, total, action, text):
        g = displayio.Group()
        self.display.root_group = g

        g.append(label.Label(terminalio.FONT, text=f"L{level} {step+1}/{total}", x=4, y=10))

        x, y = self._place(action)
        g.append(label.Label(terminalio.FONT, text=text, scale=2, x=x, y=y))

    def _place(self, action):
        # Position text depending on action type
        if action == config.ACTION_TILT_FORWARD:
            return 48, 22
        if action == config.ACTION_TILT_BACKWARD:
            return 40, 54
        if action in (config.ACTION_TILT_LEFT, config.ACTION_PRESS):
            return 0, 36
        if action in (config.ACTION_TILT_RIGHT, config.ACTION_ROTATE):
            return 68, 36
        return 40, 36

    # ----------- GAME OVER SCREEN -----------
    def show_game_over(self, level):
        g = displayio.Group()
        self.display.root_group = g
        g.append(label.Label(terminalio.FONT, text="GAME OVER", scale=2, x=4, y=28))
        g.append(label.Label(terminalio.FONT, text=f"LVL {level}", x=36, y=52))

    # ----------- WIN SCREEN -----------
    def show_win(self):
        g = displayio.Group()
        self.display.root_group = g
        g.append(label.Label(terminalio.FONT, text="YOU WIN!", scale=2, x=12, y=28))
        g.append(label.Label(terminalio.FONT, text="Press to menu", x=10, y=50))
