import time
from i2c_bus import get_i2c
from display_manager import DisplayManager
from inputs import InputManager
from lights import LightsManager
from game_logic import Game
import config

i2c = get_i2c()

# Initialize inputs (ADXL345) before the OLED
inputs = InputManager(i2c)
display = DisplayManager(i2c)
lights = LightsManager()

game = Game(display, inputs, lights)

while True:
    now = time.monotonic()
    game.update(now)
    time.sleep(config.MAIN_LOOP_DELAY)
