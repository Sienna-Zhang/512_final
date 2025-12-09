import board
import busio

_i2c = None

def get_i2c():
    """Create or return a shared I2C bus instance."""
    global _i2c
    if _i2c is None:
        _i2c = busio.I2C(board.SCL, board.SDA)
    return _i2c
