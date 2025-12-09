"""
NeoPixel lighting manager providing simple status and event effects.
"""

import time
import board
import neopixel
import config

class LightsManager:
    def __init__(self, brightness=0.2):
        """Initialize NeoPixel strip."""
        self.pixels = neopixel.NeoPixel(
            config.NEOPIXEL_PIN,
            config.NEOPIXEL_NUM_PIXELS,
            brightness=brightness,
            auto_write=False,
        )
        self.off()

    # Utility: fill color
    def _fill(self, color):
        """Set all pixels to a color and update."""
        for i in range(config.NEOPIXEL_NUM_PIXELS):
            self.pixels[i] = color
        self.pixels.show()

    def off(self):
        """Turn LEDs off."""
        self._fill((0, 0, 0))

    # ----------- STATE EFFECTS -----------
    def set_idle(self):
        """Idle/menu state indicator."""
        self._fill((0, 0, 40))

    def set_playing(self):
        """In-game indicator."""
        self._fill((30, 30, 30))

    def set_warning(self):
        """Warning indicator (time running out)."""
        self._fill((40, 40, 0))

    # ----------- EVENT EFFECTS (blocking flash) -----------
    def _flash(self, color, times=3, on_time=0.1, off_time=0.05):
        """Generic flash animation."""
        for _ in range(times):
            self._fill(color)
            time.sleep(on_time)
            self.off()
            time.sleep(off_time)

    def game_start(self):
        """Flash green when game starts."""
        self._flash((0, 50, 0), times=2, on_time=0.1, off_time=0.1)

    def success(self):
        """Flash green when action is correct."""
        self._flash((0, 80, 0), times=3, on_time=0.08, off_time=0.05)

    def failure(self):
        """Flash red when action fails."""
        self._flash((80, 0, 0), times=3, on_time=0.1, off_time=0.05)

    def win(self):
        """Show rainbow animation when winning."""
        colors = [
            (80, 0, 0),
            (80, 40, 0),
            (80, 80, 0),
            (0, 80, 0),
            (0, 0, 80),
            (50, 0, 80),
        ]
        for c in colors:
            self._fill(c)
            time.sleep(0.1)
        self.off()
