# config.py
"""
全局配置 & 常量
- 引脚映射（XIAO ESP32-C3）
- 硬件相关参数（NeoPixel 数量、加速度计阈值等）
- 游戏参数（难度、关卡数、动作类型、状态常量）
"""

import board

# =========================
# 硬件引脚配置
# =========================

# --- I2C：OLED + ADXL345 共用 ---
# 如果你是按课程文档接的，一般直接用板子的 SCL/SDA 即可
I2C_SCL = board.D5
I2C_SDA = board.D4

# --- 旋转编码器 ---
# ⚠️ 下面这三个引脚需要你根据自己的实际接线改一下
# 建议：挑 3 个空闲数字引脚即可，比如 D4 / D5 / D6
ENCODER_CLK_PIN = board.D8      # A / CLK
ENCODER_DT_PIN = board.D9       # B / DT
ENCODER_SW_PIN = board.D7       # 按钮开关（SW）

# --- NeoPixel ---
# 如果你之前实验用过某个脚，就沿用那个
NEOPIXEL_PIN = board.D10        # 数据引脚
NEOPIXEL_NUM_PIXELS = 1         # 你只有一个灯的话就是 1

# =========================
# 传感器 / 输入相关参数
# =========================

# 加速度计：用于检测 Shake 等动作
# SHAKE_THRESHOLD 是“抖动有多大才算摇动”
# 可以后面根据实际体验再调
SHAKE_THRESHOLD = 10.0          # m/s^2 之类的量级，后续可微调
ACCEL_CALIBRATION_SAMPLES = 50  # 开机时用于取平均偏移的样本数
ACCEL_FILTER_WINDOW = 4         # 简单滑动平均窗口大小

# 旋转编码器“去抖”相关（可以后续根据需要调）
ENCODER_DEBOUNCE_DELAY = 0.005  # 秒，过短会抖动，过长会变钝

# 按钮去抖
BUTTON_DEBOUNCE_DELAY = 0.05    # 秒，50ms 左右一般够用

# =========================
# 游戏参数配置
# =========================

# 至少 10 个关卡
LEVEL_COUNT = 10

# 难度设置：
# name: 名字（显示在屏幕上）
# step_time: 每一步允许的时间（秒）
# base_sequence_length: 起始关卡的指令长度（你可以在关卡提升时逐渐增加）
DIFFICULTIES = [
    {
        "name": "EASY",
        "step_time": 3.0,
        "base_sequence_length": 3,
    },
    {
        "name": "MEDIUM",
        "step_time": 2.0,
        "base_sequence_length": 4,
    },
    {
        "name": "HARD",
        "step_time": 1.5,
        "base_sequence_length": 5,
    },
]

DEFAULT_DIFFICULTY_INDEX = 0  # 默认选中 EASY

# 每一关指令长度随关卡递增的简单系数（可以在 game_logic 里用）
SEQUENCE_LENGTH_INCREMENT = 1  # 每升一级，长度 +1

# =========================
# 游戏动作类型（4 种走法）
# =========================

ACTION_ROTATE_LEFT = 0
ACTION_ROTATE_RIGHT = 1
ACTION_BUTTON_PRESS = 2
ACTION_SHAKE = 3

# 方便在别的地方遍历 / 随机生成
ACTIONS = (
    ACTION_ROTATE_LEFT,
    ACTION_ROTATE_RIGHT,
    ACTION_BUTTON_PRESS,
    ACTION_SHAKE,
)

# 显示给玩家看的文字（和上面的动作常量对应）
ACTION_LABELS = {
    ACTION_ROTATE_LEFT: "Turn Left",
    ACTION_ROTATE_RIGHT: "Turn Right",
    ACTION_BUTTON_PRESS: "Press",
    ACTION_SHAKE: "Shake",
}

# =========================
# 游戏状态常量（状态机用）
# =========================

STATE_BOOT = 0        # 可选：开机动画 / Logo
STATE_MENU = 1        # 难度选择界面
STATE_READY = 2       # 进入关卡前的准备（倒计时、提示等）
STATE_PLAYING = 3     # 正在进行关卡（玩家输入）
STATE_GAME_OVER = 4   # 失败界面
STATE_WIN = 5         # 通关界面

# =========================
# 其它通用设置
# =========================

# 主循环目标刷新间隔（可以在 code.py 里用）
MAIN_LOOP_DELAY = 0.01  # 10ms 一次循环，大概 100 FPS，够用
