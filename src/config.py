# config.py
import board

# ============================
# I2C Pins
# ============================
I2C_SCL = board.SCL
I2C_SDA = board.SDA

# ============================
# Encoder pins
# ============================
ENCODER_CLK_PIN = board.D3
ENCODER_DT_PIN  = board.D2
ENCODER_SW_PIN  = board.D8

# ============================
# NeoPixel
# ============================
NEOPIXEL_PIN = board.D7
NEOPIXEL_NUM_PIXELS = 1

# ============================
# Game Actions
# ============================
ACTION_ROTATE = "ROTATE"
ACTION_PRESS = "PRESS"

ACTION_TILT_LEFT = "TILT_LEFT"
ACTION_TILT_RIGHT = "TILT_RIGHT"
ACTION_TILT_FORWARD = "TILT_FWD"
ACTION_TILT_BACKWARD = "TILT_BACK"

ACTIONS = [
    ACTION_ROTATE,
    ACTION_PRESS,
    ACTION_TILT_LEFT,
    ACTION_TILT_RIGHT,
    ACTION_TILT_FORWARD,
    ACTION_TILT_BACKWARD,
]

ACTION_LABELS = {
    ACTION_ROTATE: "TURN",
    ACTION_PRESS:  "PRESS",
    ACTION_TILT_LEFT:  "LEFT",
    ACTION_TILT_RIGHT: "RIGHT",
    ACTION_TILT_FORWARD: "FWD",
    ACTION_TILT_BACKWARD: "BACK",
}

# 用来识别 tilt 类动作
TILT_ACTIONS = {
    ACTION_TILT_LEFT,
    ACTION_TILT_RIGHT,
    ACTION_TILT_FORWARD,
    ACTION_TILT_BACKWARD,
}

# ============================
# Difficulty & Levels
# ============================
DIFFICULTIES = [
    {
        "name": "Easy",
        "time_start": 4.0,      # 第1关：4秒
        "time_end": 3.0,        # 第10关：3秒
        "sequence_lengths": [3, 3, 4, 4, 4, 5, 5, 5, 6, 6]  # 每关的步数
    },
    {
        "name": "Medium",
        "time_start": 3.5,      # 第1关：3.5秒
        "time_end": 2.5,        # 第10关：2.5秒
        "sequence_lengths": [4, 4, 5, 5, 5, 6, 6, 6, 7, 7]
    },
    {
        "name": "Hard",
        "time_start": 3.0,      # 第1关：3秒
        "time_end": 2.0,        # 第10关：2秒
        "sequence_lengths": [5, 5, 6, 6, 6, 7, 7, 7, 8, 8]
    },
]

DEFAULT_DIFFICULTY_INDEX = 0
LEVEL_COUNT = 10

# ============================
# System settings
# ============================
BUTTON_DEBOUNCE_DELAY = 0.2
ACCEL_CALIBRATION_SAMPLES = 50
ACCEL_THRESHOLD = 3.5  # 降低阈值,约20度倾斜即可触发 (原来是6.0)
TILT_DELTA_THRESHOLD = 2.0

MAIN_LOOP_DELAY = 0.01

# ============================
# Game States
# ============================
STATE_MENU = "MENU"
STATE_PLAYING = "PLAYING"
STATE_GAME_OVER = "GAME_OVER"
STATE_WIN = "WIN"
