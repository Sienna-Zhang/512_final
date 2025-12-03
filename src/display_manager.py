# display_manager.py
"""
OLED 显示管理（使用 displayio + adafruit_displayio_ssd1306）
适配 CircuitPython 9/10：使用 i2cdisplaybus.I2CDisplayBus
"""

import displayio
import busio
import terminalio
from adafruit_display_text import label
from i2cdisplaybus import I2CDisplayBus
import adafruit_displayio_ssd1306

import config


class DisplayManager:
    def __init__(self):
        # 先释放之前的显示（防止多次运行时报错）
        displayio.release_displays()

        # 初始化 I2C：使用你在 config 里设置的引脚
        i2c = busio.I2C(config.I2C_SCL, config.I2C_SDA)

        # 使用 I2CDisplayBus（CP10 里替代了 displayio.I2CDisplay）
        display_bus = I2CDisplayBus(i2c, device_address=0x3C)
        # 如果你们的屏有 RST 脚、且连了某个 GPIO，可以写成：
        # display_bus = I2CDisplayBus(i2c, device_address=0x3C, reset=board.Dx)

        # 创建 128x64 的 SSD1306 displayio 显示对象
        self.display = adafruit_displayio_ssd1306.SSD1306(
            display_bus, width=128, height=64
        )

        # 根 group，用来放文字和其它元素
        self._root = displayio.Group()
        # 在 CP9/10 里应使用 root_group 属性
        self.display.root_group = self._root

    # ---------- 内部工具 ----------
    def _clear(self):
        """清空屏幕上的所有元素"""
        self._root = displayio.Group()
        self.display.root_group = self._root

    def _add_label(self, text, x, y, scale=1):
        """在 (x, y) 位置放一行文字"""
        lbl = label.Label(terminalio.FONT, text=text, x=x, y=y, scale=scale)
        self._root.append(lbl)

    # ---------- 通用文本 ----------
    def show_text(self, line1="", line2="", line3=""):
        """最多显示三行简单文本，调试用"""
        self._clear()
        if line1:
            self._add_label(line1, x=0, y=15, scale=1)
        if line2:
            self._add_label(line2, x=0, y=35, scale=1)
        if line3:
            self._add_label(line3, x=0, y=55, scale=1)

    # ---------- 难度菜单 ----------
    def show_menu(self, difficulties, current_index):
        """
        难度选择菜单
        difficulties: [{ "name": "EASY", ...}, ...]
        current_index: 当前选中难度的索引
        """
        self._clear()

        self._add_label("Select Difficulty", x=0, y=10, scale=1)

        start_y = 30
        line_spacing = 12

        for i, diff in enumerate(difficulties):
            name = diff.get("name", f"Opt {i}")
            prefix = ">" if i == current_index else " "
            text = f"{prefix} {name}"
            self._add_label(text, x=0, y=start_y + i * line_spacing, scale=1)

    # ---------- 游戏中界面 ----------
    def show_level(self, level, step_index, total_steps, instruction_label):
        """
        level: 当前关卡
        step_index: 当前是本关第几步（0-based）
        total_steps: 本关总步数
        instruction_label: 当前指令（如 'Shake'）
        """
        self._clear()
        self._add_label(f"Level {level}", x=0, y=10, scale=1)
        self._add_label(f"Do: {instruction_label}", x=0, y=30, scale=1)
        self._add_label(
            f"Step {step_index + 1}/{total_steps}", x=0, y=50, scale=1
        )

    # ---------- Game Over ----------
    def show_game_over(self, level_reached):
        self._clear()
        self._add_label("GAME OVER", x=10, y=20, scale=2)
        self._add_label(f"Reached L{level_reached}", x=0, y=45, scale=1)
        self._add_label("Press to restart", x=0, y=60, scale=1)

    # ---------- Win ----------
    def show_win(self):
        self._clear()
        self._add_label("YOU WIN!", x=10, y=25, scale=2)
        self._add_label("Press to restart", x=0, y=55, scale=1)

