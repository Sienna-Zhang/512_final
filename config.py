import board

# ============================
# I2C Pins
# ============================
I2C_SCL = board.SCL
I2C_SDA = board.SDA

# ============================
# Encoder Pins
# ============================
ENCODER_CLK_PIN = board.D3
ENCODER_DT_PIN  = board.D2
ENCODER_SW_PIN  = board.D8

# ============================
# NeoPixel Settings
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

# Display labels for actions
ACTION_LABELS = {
    ACTION_ROTATE: "TURN",
    ACTION_PRESS:  "PRESS",
    ACTION_TILT_LEFT:  "LEFT",
    ACTION_TILT_RIGHT: "RIGHT",
    ACTION_TILT_FORWARD: "FWD",
    ACTION_TILT_BACKWARD: "BACK",
}

# Used to identify tilt-type actions
TILT_ACTIONS = {
    ACTION_TILT_LEFT,
    ACTION_TILT_RIGHT,
    ACTION_TILT_FORWARD,
    ACTION_TILT_BACKWARD,
}

# ============================
# Difficulty & Level Settings
# ============================
DIFFICULTIES = [
    {"name": "Easy",   "time_start": 5.0, "time_end": 4.0, "base_sequence_length": 3},
    {"name": "Medium", "time_start": 4.0, "time_end": 3.0, "base_sequence_length": 4},
    {"name": "Hard",   "time_start": 3.0, "time_end": 2.0, "base_sequence_length": 5},
]

DEFAULT_DIFFICULTY_INDEX = 0
LEVEL_COUNT = 10
SEQUENCE_LENGTH_INCREMENT = 1

# ============================
# System Settings
# ============================
BUTTON_DEBOUNCE_DELAY = 0.2
ACCEL_CALIBRATION_SAMPLES = 50
ACCEL_THRESHOLD = 6.0
TILT_DELTA_THRESHOLD = 2.0

MAIN_LOOP_DELAY = 0.01

# ============================
# Game States
# ============================
STATE_MENU = "MENU"
STATE_PLAYING = "PLAYING"
STATE_GAME_OVER = "GAME_OVER"
STATE_WIN = "WIN"
