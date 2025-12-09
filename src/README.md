# 🎮 90s Handheld Reaction Game  
*A Reaction-Based Handheld Game Powered by Xiao ESP32C3 + CircuitPython*

## 📌 Overview  
This project implements a **90s-style handheld reaction game**, inspired by classic toys like *Bop It*.  
The device is built using a **Seeed Studio Xiao ESP32C3** with CircuitPython and integrates tilt detection, rotation, button input, and visual feedback.

Players follow on-screen instructions—tilting, pressing, or turning—within a shrinking time limit as levels progress.  
The game includes difficulty selection, level advancement, win/lose screens, and RGB LED feedback.

---

# 🕹️ How the Game Works

## 1. Difficulty Selection
- The OLED displays **Easy / Medium / Hard**  
- Rotate the encoder to choose  
- Press the button to start  

Each difficulty defines:
- Initial reaction time  
- Final reaction time (Level 10)  
- Base sequence length  

---

## 2. Gameplay Mechanics
The game randomly generates actions such as:

| Action | Player Behavior |
|--------|-----------------|
| TURN | Rotate encoder |
| PRESS | Press the tactile button |
| TILT_LEFT / RIGHT | Tilt device left or right |
| TILT_FWD / BACK | Tilt device forward or backward |

Rules:
- Correct action → green flash  
- Wrong / timeout → red flash + Game Over  
- No two tilt actions appear consecutively  

Players complete **10 levels**, each with decreasing time limits and longer sequences.

---

## 🔧 Hardware Components

| Component | Purpose |
|-----------|---------|
| Xiao ESP32C3 | Main controller |
| SSD1306 OLED | UI display |
| ADXL345 Accelerometer | Tilt detection |
| Rotary Encoder | TURN input + difficulty navigation |
| Panel-Mount Button | PRESS action |
| NeoPixel RGB LED | Visual feedback |
| Li-Po Battery + Switch | Portable power |
| Custom 3D Enclosure | Secure and ergonomic shell |

---

# 🧱 Enclosure Design

The device uses a **semi-transparent 3D-printed shell**, allowing internal wiring and LEDs to subtly show through, creating a clean retro–mechanical aesthetic.  
The shape supports **two-handed gameplay**: right hand on the encoder, left hand on the side-mounted button.

A separate **12 mm panel-mount momentary pushbutton** (as shown in the images) replaces the encoder’s built-in switch and provides reliable PRESS input.

---

# 🧠 Software Architecture

### `code.py`
Main loop, system initialization, and state updates.

### `inputs.py`
Manages:
- Encoder rotation
- Button press
- Accelerometer tilt  
Includes debouncing and threshold logic.

### `display_manager.py`
Renders:
- Menu  
- Level instructions  
- Game Over / Victory screens  

Positions text based on direction.

### `game_logic.py`
Implements:
- Difficulty scaling  
- Sequence generation  
- Timing  
- Success/failure feedback  
- Level progression  

### `lights.py`
NeoPixel effects:
- Idle
- Success
- Failure
- Win animation

### `i2c_bus.py`
Ensures all components share a **single I²C bus** to avoid pin conflicts.

---

# 📁 Repository Structure
/
├── code.py
├── config.py
├── inputs.py
├── display_manager.py
├── game_logic.py
├── lights.py
├── i2c_bus.py
├── lib/ (CircuitPython libraries)
└── README.md


---

# 🔋 Power System

The Li-Po battery connects through a side-mounted power switch and feeds the Xiao ESP32C3’s BAT/GND pins.  
The enclosure keeps all wires secure while still allowing visibility through the translucent shell.

---

# 🏁 Conclusion

This project combines embedded hardware, sensor-based interaction, and real-time game logic into a handheld device that feels both nostalgic and modern.  
Its modular CircuitPython architecture, ergonomic enclosure, and multi-input gameplay recreate the charm of 90s reaction games in a portable form.


