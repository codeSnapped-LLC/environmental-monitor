from machine import I2C, Pin
from config import SOIL_DEPTH_1

class EnvironmentalSensor:
    def __init__(self, i2c_bus=0, sda_pin=8, scl_pin=9):
        """Initialize I2C and sensor hardware"""
        self.i2c = I2C(i2c_bus, sda=Pin(sda_pin), scl=Pin(scl_pin))
        self._scan_i2c_devices()
        
    def _scan_i2c_devices(self):
        """Scan for connected I2C devices"""
        devices = self.i2c.scan()
        if not devices:
            raise RuntimeError("No I2C devices found")
        print(f"Found I2C devices at: {[hex(d) for d in devices]}")
        
    def read_air_temperature(self):
        """Read air temperature in Celsius"""
        # TODO: Implement actual sensor reading
        return 23.5  # Mock value
        
    def read_soil_temperature(self, depth):
        """Read soil temperature in Celsius at specified depth"""
        # TODO: Implement actual sensor reading
        if depth == SOIL_DEPTH_1:
            return 19.8  # Mock value for depth 1
        return 17.2  # Mock value for depth 2
        
    def read_humidity(self):
        """Read relative humidity percentage"""
        # TODO: Implement actual sensor reading
        return 45.2  # Mock value
        
    def read_air_quality(self):
        """Read air quality (VOC/CO2) in ppm"""
        # TODO: Implement actual sensor reading
        return 412  # Mock value
        
    def read_ph(self):
        """Read pH of rainwater"""
        # TODO: Implement actual sensor reading
        return 6.8  # Mock value
