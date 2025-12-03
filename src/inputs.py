# inputs.py
"""
输入管理：旋转编码器 / 按钮 / ADXL345 加速度计
"""

import time
import board
import busio
import digitalio

import adafruit_adxl34x
import config


class InputManager:
    def __init__(self):

        # -----------------------------
        # 编码器旋钮（CLK / DT）
        # -----------------------------
        self.enc_clk = digitalio.DigitalInOut(config.ENCODER_CLK_PIN)
        self.enc_clk.direction = digitalio.Direction.INPUT
        self.enc_clk.pull = digitalio.Pull.UP

        self.enc_dt = digitalio.DigitalInOut(config.ENCODER_DT_PIN)
        self.enc_dt.direction = digitalio.Direction.INPUT
        self.enc_dt.pull = digitalio.Pull.UP

        self.last_clk = self.enc_clk.value

        # -----------------------------
        # 按钮
        # -----------------------------
        self.enc_sw = digitalio.DigitalInOut(config.ENCODER_SW_PIN)
        self.enc_sw.direction = digitalio.Direction.INPUT
        self.enc_sw.pull = digitalio.Pull.UP
        self._last_button_time = 0

        # -----------------------------
        # 加速度计 ADXL345（I2C）
        # -----------------------------
        i2c = busio.I2C(config.I2C_SCL, config.I2C_SDA)
        self.accel = adafruit_adxl34x.ADXL345(i2c)

        # 加速度计初始偏移（后面做校准）
        self.offset_x = 0
        self.offset_y = 0
        self.offset_z = 0

    # -------------------------------------------------------
    # 编码器：返回 "LEFT" / "RIGHT" / None
    # -------------------------------------------------------
    def get_encoder_turn(self):
        current_clk = self.enc_clk.value

        # 检测边沿变化
        if current_clk != self.last_clk:
            self.last_clk = current_clk

            if current_clk:  # 只在上升沿处理
                if self.enc_dt.value != current_clk:
                    return "RIGHT"
                else:
                    return "LEFT"

        return None

    # -------------------------------------------------------
    # 按钮检测：仅检测“按下瞬间”
    # -------------------------------------------------------
    def get_button_press(self):
        if not self.enc_sw.value:  # 拉高，上按为 0
            now = time.monotonic()
            if now - self._last_button_time > config.BUTTON_DEBOUNCE_DELAY:
                self._last_button_time = now
                return True
        return False

    # -------------------------------------------------------
    # 加速度计原始数据（带偏移）
    # -------------------------------------------------------
    def get_accel(self):
        x, y, z = self.accel.acceleration
        return (
            x - self.offset_x,
            y - self.offset_y,
            z - self.offset_z,
        )

    # -------------------------------------------------------
    # Shake 检测（粗略版，后面一起调试）
    # -------------------------------------------------------
    def detect_shake(self):
        x, y, z = self.get_accel()
        total = abs(x) + abs(y) + abs(z)
        return total > config.SHAKE_THRESHOLD
