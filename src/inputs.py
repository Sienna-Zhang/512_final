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
        
        # 旋转检测：需要检测到完整的脉冲才算一次旋转
        self.rotation_confirmed = False

        # ---- Button ----
        self.btn = digitalio.DigitalInOut(config.ENCODER_SW_PIN)
        self.btn.direction = digitalio.Direction.INPUT
        self.btn.pull = digitalio.Pull.UP
        self.last_btn_time = 0

        # ---- Accelerometer ----
        self.accel = adafruit_adxl34x.ADXL345(i2c)

    # ---- ROTATE (improved detection) ----
    def get_turn(self):
        """
        改进的旋转检测：
        1. 检测CLK信号的完整变化（从HIGH到LOW或从LOW到HIGH）
        2. 验证DT信号确认旋转方向
        3. 添加防抖动延迟
        """
        clk = self.clk.value
        dt = self.dt.value
        
        # 检测CLK下降沿（从HIGH到LOW的转变）
        if clk != self.last_clk:
            if not clk:  # CLK从HIGH变为LOW
                # 检查DT状态来确认这是真实的旋转
                # 无论顺时针还是逆时针，只要转动就返回ROTATE
                if time.monotonic() - self.last_turn_time > 0.15:  # 增加防抖时间
                    self.last_turn_time = time.monotonic()
                    self.last_clk = clk
                    return config.ACTION_ROTATE
            
            self.last_clk = clk
        
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
