import time, math
from statistics import mean
from lis3mdl import LIS3MDL
from lis3dh import LIS3DH

offset = [0.06496638409821687, -0.17736042092955276, 0.15229465068693365]
#         -0.8004238526746565 , 0.1680064308681672 , 1.54983922829582]
#         -0.10494007600116925 , -0.027769657994738378 , 0.04311604793919904]

mag = LIS3MDL(offset=offset)
accel = LIS3DH()

# Return the tilt-compensented bearing of the positive X-axis in azimuth:
# N: 0 degree, E: 90 degrees, S: 180 degrees, and W: 270 degrees.
#
def bearingPitch():
    magX, magY, magZ = mag.readG()
    print("Gauss:", magX, magY, magZ)
    print("Magnetic field strength (nT): ", mag.magneticFieldStrengthT())
    print("2D Bearing: ", mag.bearing(magX, -magY))
    
    gX, gY, gZ = accel.readG()
    pitch, roll = accel.pitchRoll(-gX, gY, gZ)
    print("Pitch:", math.degrees(pitch), "Roll:", math.degrees(roll))
    bearing = mag.tiltCompensentedBearing(magX, -magY, -magZ,
                                          pitch, roll)
    print("3D Bearing: ", bearing)
    return (bearing, math.degrees(pitch))

if __name__ == "__main__":
    while True:
        try:
            bearing, pitch = bearingPitch()
            print("Bearing: ", bearing)
            print("Pitch: ", pitch)
            print("")
            time.sleep(1)
        except KeyboardInterrupt:
            break