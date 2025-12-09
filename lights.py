# lights.py
"""
NeoPixel 灯光管理
- 使用 config.NEOPIXEL_PIN / NEOPIXEL_NUM_PIXELS
- 提供简单的状态灯和事件效果（成功/失败/开始/通关）
"""

import time
import board
import neopixel
import config


class LightsManager:
    def __init__(self, brightness=0.2):
        """
        brightness: 整体亮度，0~1
        3.3V 供电时建议不要太高，0.2 左右就够亮了
        """
        self.pixels = neopixel.NeoPixel(
            config.NEOPIXEL_PIN,
            config.NEOPIXEL_NUM_PIXELS,
            brightness=brightness,
            auto_write=False,
        )
        self.off()

    # -----------------------------
    # 工具函数
    # -----------------------------
    def _fill(self, color):
        """填充所有像素为同一颜色并刷新"""
        for i in range(config.NEOPIXEL_NUM_PIXELS):
            self.pixels[i] = color
        self.pixels.show()

    def off(self):
        """关灯"""
        self._fill((0, 0, 0))

    # -----------------------------
    # 状态类效果（持续状态）
    # -----------------------------
    def set_idle(self):
        """待机/菜单状态，比如蓝色常亮"""
        self._fill((0, 0, 40))

    def set_playing(self):
        """游戏进行中，比如白色微亮"""
        self._fill((30, 30, 30))

    def set_warning(self):
        """时间快到了之类，可以用黄色提示"""
        self._fill((40, 40, 0))

    # -----------------------------
    # 事件类效果（短暂闪烁）
    # 会阻塞几十毫秒，用于反馈事件
    # -----------------------------
    def _flash(self, color, times=3, on_time=0.1, off_time=0.05):
        """通用闪烁函数"""
        for _ in range(times):
            self._fill(color)
            time.sleep(on_time)
            self.off()
            time.sleep(off_time)

    def game_start(self):
        """游戏开始时提示（绿色闪几下）"""
        self._flash((0, 50, 0), times=2, on_time=0.1, off_time=0.1)

    def success(self):
        """动作正确/过关：绿色闪烁"""
        self._flash((0, 80, 0), times=3, on_time=0.08, off_time=0.05)

    def failure(self):
        """动作错误/超时：红色闪烁"""
        self._flash((80, 0, 0), times=3, on_time=0.1, off_time=0.05)

    def win(self):
        """通关：简单彩虹效果"""
        colors = [
            (80, 0, 0),    # 红
            (80, 40, 0),   # 橙
            (80, 80, 0),   # 黄
            (0, 80, 0),    # 绿
            (0, 0, 80),    # 蓝
            (50, 0, 80),   # 紫
        ]
        for c in colors:
            self._fill(c)
            time.sleep(0.1)
        self.off()

