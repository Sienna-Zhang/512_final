# inputs.py

import time
import digitalio
import adafruit_adxl34x
import config

class InputManager:

    def __init__(self, i2c):
        # ---- Encoder ----
        self.clk = digitalio.DigitalInOut(config.ENCODER_CLK_PIN)
        self.clk.direction = digitalio.Direction.INPUT
        self.clk.pull = digitalio.Pull.UP

        self.dt = digitalio.DigitalInOut(config.ENCODER_DT_PIN)
        self.dt.direction = digitalio.Direction.INPUT
        self.dt.pull = digitalio.Pull.UP

        self.last_clk = self.clk.value
        self.last_turn_time = 0

        # ---- Button ----
        self.btn = digitalio.DigitalInOut(config.ENCODER_SW_PIN)
        self.btn.direction = digitalio.Direction.INPUT
        self.btn.pull = digitalio.Pull.UP
        self.last_btn_time = 0

        # ---- Accelerometer ----
        self.accel = adafruit_adxl34x.ADXL345(i2c)

    # ---- ROTATE (no direction) ----
    def get_turn(self):
        clk = self.clk.value
        if clk != self.last_clk:
            self.last_clk = clk
            if time.monotonic() - self.last_turn_time > 0.1:
                self.last_turn_time = time.monotonic()
                return config.ACTION_ROTATE
        return None

    # ---- PRESS ----
    def get_press(self):
        if not self.btn.value:
            if time.monotonic() - self.last_btn_time > config.BUTTON_DEBOUNCE_DELAY:
                self.last_btn_time = time.monotonic()
                return config.ACTION_PRESS
        return None

    # ---- TILT detection ----
    def get_tilt(self):
        x, y, z = self.accel.acceleration

        if x > config.ACCEL_THRESHOLD:
            return config.ACTION_TILT_RIGHT
        if x < -config.ACCEL_THRESHOLD:
            return config.ACTION_TILT_LEFT
        if y > config.ACCEL_THRESHOLD:
            return config.ACTION_TILT_FORWARD
        if y < -config.ACCEL_THRESHOLD:
            return config.ACTION_TILT_BACKWARD
        return None

