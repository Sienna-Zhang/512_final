# 🎮 Simon-Style Memory Game  
*A Reaction-Based Handheld Game Powered by Seeeduino XIAO + CircuitPython*

## 📌 Overview  
This project implements a **Simon-style memory game**, inspired by classic 90s handheld reaction toys like *Bop It* and *Simon*.  
The device is built using a **Seeed Studio Xiao SAMD21** with CircuitPython and integrates tilt detection, rotation, button input, and visual feedback through an OLED display and RGB LED.

Players must complete increasingly complex action sequences—tilting, pressing, or turning—within a time limit that shrinks as levels progress.  
The game features three difficulty modes, 10 progressive levels, win/lose screens, and rainbow LED celebration effects.

---

## 🕹️ How the Game Works

### 1. Difficulty Selection
- The OLED displays **Easy / Medium / Hard**  
- Rotate the encoder to cycle through difficulties  
- Press the button to start the game  

Each difficulty defines:
- **Time per action** - starts at `time_start`, decreases linearly to `time_end` by level 10
- **Sequence complexity** - number of actions increases with each level

| Difficulty | Level 1 Time | Level 10 Time | Starting Length | Final Length |
|------------|--------------|---------------|-----------------|--------------|
| Easy       | 4.0s         | 3.0s          | 3 actions       | 6 actions    |
| Medium     | 3.5s         | 2.5s          | 4 actions       | 7 actions    |
| Hard       | 3.0s         | 2.0s          | 5 actions       | 8 actions    |

---

### 2. Gameplay Mechanics

#### Available Actions
The game randomly generates sequences from **6 possible actions**:

| Action | Display | Player Response |
|--------|---------|-----------------|
| TURN | "TURN" | Rotate the encoder (any direction) |
| PRESS | "PRESS" | Press the tactile button |
| LEFT | "LEFT" | Tilt device left |
| RIGHT | "RIGHT" | Tilt device right |
| FWD | "FWD" | Tilt device forward |
| BACK | "BACK" | Tilt device backward |

#### Game Rules
- ✅ **Correct action** → Green LED flash + advance to next step
- ❌ **Wrong action or timeout** → Red LED flash + Game Over screen
- 🎯 **Complete all 10 levels** → Rainbow LED animation + Victory screen
- 🔄 **Smart sequence generation** → No two consecutive tilt actions in the same direction (prevents impossible moves)

#### Visual Feedback
- **Action text positioning**: Displayed on screen in the direction you need to tilt
  - "FWD" appears at the top
  - "BACK" appears at the bottom
  - "LEFT" appears on the left
  - "RIGHT" appears on the right
- **Level indicator**: Shows current level and step progress (e.g., "L3 2/5")
- **LED feedback**:
  - Blue = Menu/Idle
  - White = Playing
  - Green flash = Success
  - Red flash = Failure
  - Rainbow cycle = Victory

---

## 📊 Level Progression

### Difficulty Curve
- **Sequence length** increases gradually across 10 levels
- **Time limit** decreases linearly from start to end time
- **Example (Easy mode)**:
  - Level 1: 3 actions, 4.0s each
  - Level 5: 5 actions, 3.5s each
  - Level 10: 6 actions, 3.0s each

### Total Game Duration
- **Easy**: ~45 actions total (~2-3 minutes)
- **Medium**: ~55 actions total (~3-4 minutes)
- **Hard**: ~65 actions total (~4-5 minutes)

---

## 🔧 Hardware Components

| Component | Model | Purpose |
|-----------|-------|---------|
| Microcontroller | Seeeduino XIAO SAMD21 | Main controller (CircuitPython) |
| Display | SSD1306 OLED (128×64, I²C) | Game UI and instructions |
| Accelerometer | ADXL345 (I²C) | 3-axis tilt detection |
| Encoder | Rotary Encoder with Switch | TURN action + menu navigation |
| Button | Panel-Mount Tactile Button | PRESS action |
| LED | NeoPixel WS2812B | Visual feedback and effects |
| Power | Li-Po Battery + Switch | Portable power supply |
| Enclosure | 3D-Printed Shell | Protective and ergonomic housing |

### Pin Configuration
```python
# I2C Bus (shared)
SCL = board.SCL
SDA = board.SDA

# Rotary Encoder
ENCODER_CLK = board.D3
ENCODER_DT  = board.D2
ENCODER_SW  = board.D8

# NeoPixel LED
NEOPIXEL_PIN = board.D7
```

---

## 🧱 Enclosure Design

The device uses a **semi-transparent 3D-printed shell** that:
- Shows internal components through the translucent material
- Creates a retro-modern aesthetic with visible wiring and LED glow
- Supports **two-handed gameplay**:
  - Right hand operates the rotary encoder
  - Left hand accesses the side-mounted button
- Keeps all wiring secure while maintaining visibility

The **12mm panel-mount button** is mounted on the side for ergonomic PRESS actions, separate from the encoder's built-in switch.

---

## 🧠 Software Architecture

### Core Design Principles
- **Modular architecture** - Each component has a dedicated manager class
- **State machine pattern** - Clean state transitions (MENU → PLAYING → WIN/GAME_OVER)
- **Object composition** - Game class coordinates all hardware managers
- **Non-blocking animations** - LED effects don't freeze gameplay

### File Structure

#### `code.py`
Main entry point that:
- Initializes I²C bus and all hardware managers
- Creates the Game instance
- Runs the main loop at 100Hz

#### `config.py`
Configuration hub containing:
- Hardware pin definitions
- Game parameters (difficulties, time limits, sequence lengths)
- Action definitions and labels
- System settings (thresholds, debounce delays)

#### `i2c_bus.py`
**Singleton pattern** implementation:
- Ensures only one I²C bus instance exists
- Prevents pin conflicts between OLED and accelerometer
- Shared by all I²C devices

#### `inputs.py`
Input manager handling:
- **Rotary encoder** - Falling edge detection with 0.15s debounce
- **Button press** - Active-low detection with 0.2s debounce
- **Accelerometer** - Threshold-based tilt detection (±3.5 m/s² = ~20° tilt)

**Key Features**:
- Software debouncing prevents false triggers
- Improved encoder detection using CLK falling edge
- Accelerometer reads X/Y/Z acceleration for tilt direction

#### `display_manager.py`
OLED display controller:
- **Menu screen** - Difficulty selection with arrow indicator
- **Level screen** - Level number, step progress, and action prompt
- **Game Over screen** - Shows final level reached
- **Win screen** - Victory message with return prompt

**Smart positioning**: Action text appears in the direction you need to tilt

#### `lights.py`
NeoPixel LED manager:
- **State lighting**: Idle (blue), Playing (white), Warning (yellow)
- **Event feedback**: Success (green flash), Failure (red flash)
- **Win animation**: Non-blocking rainbow cycle at 0.15s intervals
- Brightness set to 0.2 (20%) for 3.3V power safety

#### `game_logic.py`
Core game engine implementing:
- **State machine**: Menu, Playing, Game Over, Win
- **Level generator**: Random sequences avoiding consecutive same-direction tilts
- **Timing system**: Deadline-based timeout detection
- **Success/failure handling**: LED feedback and state transitions
- **Win condition**: Detects completion of level 10

---

## 🎯 Technical Highlights

### 1. Tilt Detection Algorithm
```python
# Threshold: 3.5 m/s² ≈ 20° tilt angle
ACCEL_THRESHOLD = 3.5

def get_tilt(self):
    x, y, z = self.accel.acceleration
    
    if x > ACCEL_THRESHOLD:
        return ACTION_TILT_RIGHT
    if x < -ACCEL_THRESHOLD:
        return ACTION_TILT_LEFT
    # Similar for Y-axis (forward/backward)
```

**Calculation**: For a device at ~20° tilt:
- Horizontal acceleration ≈ g × sin(20°) ≈ 3.35 m/s²
- Threshold of 3.5 provides good balance between sensitivity and stability

### 2. Debouncing Strategy
**Problem**: Mechanical switches produce multiple signals ("bounce") during activation

**Solution**: Time-based software debouncing
```python
if time.monotonic() - self.last_press_time > 0.2:  # 200ms debounce
    self.last_press_time = time.monotonic()
    return ACTION_PRESS
```

### 3. Encoder Edge Detection
**Improvement**: Only trigger on CLK falling edge (HIGH → LOW)
- Prevents multiple detections per rotation
- More reliable than level-based detection
- 0.15s debounce eliminates mechanical noise

### 4. Non-Blocking Victory Animation
```python
def update(self, now):
    if now - self.win_last_change >= 0.15:
        # Cycle to next color
        self.win_color_index = (self.win_color_index + 1) % 7
```
- Called in main loop, not blocking
- Player can still press button to return to menu
- Cycles through 7 colors: Red → Orange → Yellow → Green → Cyan → Blue → Purple

### 5. Sequence Generation Logic
```python
while action in TILT_ACTIONS and action == last_tilt:
    action = random.choice(ACTIONS)  # Re-roll
```
- Prevents impossible sequences (e.g., LEFT immediately followed by LEFT)
- Ensures playability while maintaining randomness

---

## 📋 Power System

- **Battery**: Li-Po cell (3.7V nominal)
- **Connection**: BAT and GND pins on Xiao SAMD21
- **Switch**: Side-mounted power switch for easy on/off
- **LED brightness**: Limited to 20% to prevent excessive current draw on 3.3V logic

---

## 🚀 Installation & Setup

### Required Libraries (CircuitPython)
Copy these to the `lib/` folder on your CIRCUITPY drive:
- `adafruit_bus_device`
- `adafruit_displayio_ssd1306.mpy`
- `adafruit_display_text`
- `adafruit_adxl34x.mpy`
- `neopixel.mpy`

### Wiring Diagram
```
Seeeduino XIAO:
  SCL ─────────┬─ OLED SCL
               └─ ADXL345 SCL
  
  SDA ─────────┬─ OLED SDA
               └─ ADXL345 SDA
  
  D2 ────────── Encoder DT
  D3 ────────── Encoder CLK
  D8 ────────── Encoder SW (or external button)
  D7 ────────── NeoPixel DIN
  
  3V3 ─────────┬─ OLED VCC
               ├─ ADXL345 VCC
               ├─ Encoder VCC
               └─ NeoPixel VCC
  
  GND ──────── Common Ground
  BAT ──────── Li-Po +
```

### Upload Code
1. Install CircuitPython on Xiao SAMD21
2. Copy all `.py` files to CIRCUITPY drive
3. Copy required libraries to `lib/` folder
4. Reset device - game will start automatically

---

## 🎮 Gameplay Tips

1. **Hold the device steady** before tilting - the accelerometer detects relative motion
2. **Small tilts work** - You only need ~20° angle to trigger tilt actions
3. **Quick reactions** - Time limits get shorter as you progress
4. **Watch the countdown** - Serial monitor shows remaining time in debug mode
5. **Practice mode** - Start with Easy difficulty to learn the controls

---

## 🔍 Debug Mode

Serial output provides real-time feedback (connect at 115200 baud):
```
✅ Correct tilt: TILT_LEFT
⏱️ Time left: 0.8s, Waiting for: ACTION_PRESS
🎉 Level 3 completed!
⏰ TIMEOUT! Expected: ACTION_ROTATE
🏆 YOU WIN! All levels completed!
```

Remove `print()` statements in production for cleaner operation.

---

## 🏆 Conclusion

This project demonstrates:
- **Embedded systems programming** with CircuitPython
- **Sensor fusion** combining accelerometer, encoder, and button inputs
- **State machine design** for game flow management
- **Real-time systems** with deadline-based timing
- **Hardware integration** across multiple I²C devices and GPIO pins
- **User experience design** with visual, tactile, and LED feedback

The result is a portable, battery-powered handheld device that recreates the addictive gameplay of 90s reaction games while showcasing modern embedded development practices.

---

## 📦 Repository Structure
```
simon-game/
├── code.py              # Main entry point
├── config.py            # Configuration and constants
├── game_logic.py        # Core game engine
├── inputs.py            # Input handling (encoder, button, accelerometer)
├── display_manager.py   # OLED display controller
├── lights.py            # NeoPixel LED effects
├── i2c_bus.py          # I²C bus singleton
├── lib/                 # CircuitPython libraries
└── README.md           # This file
```

---

## 📄 License

This project is open source. Feel free to modify, improve, and share!

---

## 🙏 Acknowledgments

- Inspired by classic games: *Simon*, *Bop It*, and other 90s handheld reaction toys
- Built with [CircuitPython](https://circuitpython.org/)
- Hardware by [Seeed Studio](https://www.seeedstudio.com/)

---

**Enjoy the game! 🎉**
