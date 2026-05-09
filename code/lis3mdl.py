# Driver for the LIS3MDL magnetometer
# April 27, 2024 v0.03

import smbus, sys, time, math
from typing import ClassVar, Tuple, Final, List

# Default I2C address
_ADDRESS: Final[int] = 0x1C
# Default sensing scale: ±16 Gauss
_SCALE: Final[int] = 4

# Register addresses
_REG_WHO_AM_I: Final[int] = 0x0F
_CTRL_REG1: Final[int] = 0x20
_CTRL_REG2: Final[int] = 0x21
_CTRL_REG3: Final[int] = 0x22
_CTRL_REG4: Final[int] = 0x23
_CTRL_REG5: Final[int] = 0x24

# Defaults to 80Hz data rate
#
class LIS3MDL:

    def __init__(self, *,
                 address: int =_ADDRESS,
                 scale: int = _SCALE,
                 offset: List[float] = [0,0,0]) -> None: 
        assert scale in [4, 8, 12, 16], "Wrong LIS3MDL sensing scale: " +\
               str(scale) + "." + " It must be 4, 8, 12 or 16."

        self._i2c: smbus.SMBus = smbus.SMBus(1)
        self._addr: int = address
        self._scale: int = scale
        self._offset: List[float, float, float] = offset
        
        if self._scale == 4:
            scaleHex: int = 0x00
        elif self._scale == 8:
            scaleHex: int = 0x20
        elif self._scale == 12:
            scaleHex: int = 0x40
        elif self._scale == 16:
            scaleHex: int = 0x60
        
        try:
            # Ping the sensor
            sensorId = self._i2c.read_byte_data(self._addr, _REG_WHO_AM_I)
            if sensorId != 0x3D:
                raise RuntimeError("Failed to find LIS3MDL.")
            # Clear/reset the sensor's memory. REBOOT=1, SOFT_RST=1
            self._i2c.write_byte_data(self._addr, _CTRL_REG2, 0x0C)
            # Ultra high-performance (lowest noise) mode, 80 Hz data rate
            self._i2c.write_byte_data(self._addr, _CTRL_REG1, 0x7C)
            self._i2c.write_byte_data(self._addr, _CTRL_REG4, 0x0C)            
            # Sensing scale
            self._i2c.write_byte_data(self._addr, _CTRL_REG2, scaleHex)
            # Continuous conversion mode
            self._i2c.write_byte_data(self._addr, _CTRL_REG3, 0x00)
            print("LIS3MDL cconfigured with " + "I2C addr=" + hex(self._addr) +\
                  ", sensing scale=±" + str(self._scale) + " Gauss" +\
                  ", data rate=80Hz")
        except OSError:
            print("Wrong I2C address: " + hex(self._addr))
            raise

    @property
    def offset(self) -> List[float]:
        return self._offset
    
    def setOffset(self, offset: List[float]) -> None:
        self._offset = offset

    # Read X, Y, and Z magnetic values in Gauss and return them as a tuple.
    #
    def readG(self) -> Tuple[float, float, float]:
        # xh: Most significant part of magnetic data
        # xl: Least significant part of magnetic data
        # Concat xh and xl to get the complete magnetic data.
        xl = self._i2c.read_byte_data(self._addr, 0x28)
        xh = self._i2c.read_byte_data(self._addr, 0x29)
        yl = self._i2c.read_byte_data(self._addr, 0x2A)
        yh = self._i2c.read_byte_data(self._addr, 0x2B)
        zl = self._i2c.read_byte_data(self._addr, 0x2C)
        zh = self._i2c.read_byte_data(self._addr, 0x2D)
        
        # Concat xh (8-bits) and xl (8 bits) to derive the complete
        # left-justified 16-bit data. 
        x = (xh << 8 | xl)
        y = (yh << 8 | yl)
        z = (zh << 8 | zl)
        
        # Each magnetic value is expressed as two's complement. Convert it
        # to a signed value [-32768, 32767]. Note: 2^16 = 65,536
        if x >= 32768:
            x -= 65536
        if y >= 32768:
            y -= 65536
        if z >= 32768:
            z -= 65536
        
        # Convert mag values to Gauss values based on the sensing scale.
#         divider = 65536/(2 * self._scale)
        if self._scale == 4:
            divider = 6842
        if self._scale == 8:
            divider = 3421
        if self._scale == 12:
            divider = 2281
        if self._scale == 16:
            divider = 1711
        return (x/divider - self._offset[0],
                y/divider - self._offset[1],
                z/divider - self._offset[2])

    # Read X, Y, and Z magnetic values in nT (nano Tesla) and return them as a tuple.
    #
    def readT(self) -> Tuple[float, float, float]:
        magVals = self.readG()
        return (magVals[0]/10000 * 10**9,
                magVals[1]/10000 * 10**9,
                magVals[2]/10000 * 10**9)

    # Return magnetic field strength in Gauss
    #
    def magneticFieldStrengthG(self) -> float:
        magVals = self.readG()
        return ( magVals[0]**2 + magVals[1]**2 + magVals[2]**2 )**0.5
    
    # Return magnetic field strength in nT (nano Tesla)
    #
    def magneticFieldStrengthT(self) -> float:
        return self.magneticFieldStrengthG()/10000 * 10**9 

    # If declination is negative (west), pass negative values for declinationDeg
    # and declinationMin. For example, declination is known to be -14°6' (west) in
    # Boston, MA. In this case, pass declinationDeg=-14 and  declinationMin=-6. 
    # 
    def declinationDegMinToDecimalDeg(self, declinationDeg, declinationMin) -> float:
        return declinationDeg + declinationMin/60
        
    # Return the bearing of the positive X-axis in azimuth: N: 0 degree, E: 90 degrees,
    # S: 180 degrees, and W: 270 degrees. This works only when the magnetometer
    # is placed on a flat/level surface. Tilt-compensation is NOT implemented. 
    #
    def bearing(self, magX, magY) -> float: 
        bearingRad = math.atan2(magY, magX)
        if(bearingRad < 0):
            bearingRad += 2*math.pi
        if(bearingRad > 2*math.pi):
            bearingRad -= 2*math.pi
        return 360 - math.degrees(bearingRad)

    # Return the tilt-compensented bearing of the positive X-axis in azimuth:
    # N: 0 degree, E: 90 degrees, S: 180 degrees, and W: 270 degrees. 
    #
    def tiltCompensentedBearing(self, magX, magY, magZ, pitch, roll):
        magFieldStrength = math.sqrt(magX**2 + magY**2 + magZ**2)
        magX = magX/magFieldStrength
        magY = magY/magFieldStrength
        magZ = magZ/magFieldStrength
        
        xComp = magX * math.cos(pitch) + magZ * math.sin(pitch)
        yComp = magX * math.sin(roll) * math.sin(pitch) + \
                magY * math.cos(roll) - \
                magZ * math.sin(roll) * math.cos(pitch)
        return self.bearing(xComp, yComp)

if __name__ == "__main__":
    sensor = LIS3MDL()
    print("Gauss:", sensor.readG() )
    print("nT:", sensor.readT() )
    print("Magnetic field strength (Gauss): ", sensor.magneticFieldStrengthG())
    print("Magnetic field strength (nT): ", sensor.magneticFieldStrengthT())
#     print( sensor.getBearing( sensor.declinationDegMinToDecimalDeg(-14, -6), axis="x"))
    
    