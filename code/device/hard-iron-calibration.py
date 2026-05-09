import time, math
from lis3mdl import LIS3MDL

sensor = LIS3MDL()

def read_magnetometer():
    """
    Return raw magnetometer readings as (x, y, z).
    Replace this with your actual sensor-specific code.
    """
    # Example:
    # x = mag.magnetic[0]
    # y = mag.magnetic[1]
    # z = mag.magnetic[2]
    
    x, y, z = sensor.readG()
    return x, y, z


def calibrate(duration_sec=30, sample_delay=0.05):
    print("Calibration starting...")
    print("Rotate the sensor slowly in all directions.")
    print(f"Collecting data for {duration_sec} seconds...\n")

    min_x = float("inf")
    min_y = float("inf")
    min_z = float("inf")
    max_x = float("-inf")
    max_y = float("-inf")
    max_z = float("-inf")

    start = time.time()
    sample_count = 0

    while time.time() - start < duration_sec:
        try:
            x, y, z = read_magnetometer()
        except Exception as e:
            print(f"Read error: {e}")
            time.sleep(sample_delay)
            continue

        min_x = min(min_x, x)
        min_y = min(min_y, y)
        min_z = min(min_z, z)

        max_x = max(max_x, x)
        max_y = max(max_y, y)
        max_z = max(max_z, z)

        sample_count += 1

        if sample_count % 20 == 0:
            elapsed = time.time() - start
            print(
                f"[{elapsed:5.1f}s] "
                f"x=({min_x:8.2f}, {max_x:8.2f}) "
                f"y=({min_y:8.2f}, {max_y:8.2f}) "
                f"z=({min_z:8.2f}, {max_z:8.2f})"
            )

        time.sleep(sample_delay)

    offset_x = (max_x + min_x) / 2.0
    offset_y = (max_y + min_y) / 2.0
    offset_z = (max_z + min_z) / 2.0

    scale_x = (max_x - min_x) / 2.0
    scale_y = (max_y - min_y) / 2.0
    scale_z = (max_z - min_z) / 2.0

    avg_scale = (scale_x + scale_y + scale_z) / 3.0 if sample_count > 0 else 1.0

    print("\nCalibration finished.")
    print(f"Samples collected: {sample_count}")
    print("\nOffsets:")
#     print(f"OFFSET_X = {offset_x:.3f}")
#     print(f"OFFSET_Y = {offset_y:.3f}")
#     print(f"OFFSET_Z = {offset_z:.3f}")
    print(f"OFFSET_X = {offset_x}")
    print(f"OFFSET_Y = {offset_y}")
    print(f"OFFSET_Z = {offset_z}")
    
#     print("\nOptional scale factors (rough soft-iron correction):")
#     if scale_x != 0 and scale_y != 0 and scale_z != 0:
#         corr_x = avg_scale / scale_x
#         corr_y = avg_scale / scale_y
#         corr_z = avg_scale / scale_z
#         print(f"SCALE_X = {corr_x:.6f}")
#         print(f"SCALE_Y = {corr_y:.6f}")
#         print(f"SCALE_Z = {corr_z:.6f}")
#     else:
#         print("Scale factors unavailable because one axis had zero range.")

    return {
        "offset_x": offset_x,
        "offset_y": offset_y,
        "offset_z": offset_z,
        "min_x": min_x,
        "max_x": max_x,
        "min_y": min_y,
        "max_y": max_y,
        "min_z": min_z,
        "max_z": max_z,
    }


def corrected_magnetometer_reading(offset_x, offset_y, offset_z):
    x, y, z = read_magnetometer()
    return x - offset_x, y - offset_y, z - offset_z


def heading_degrees(x, y):
    """
    Compute heading from corrected x, y.
    Assumes sensor is level enough for simple compass use.
    """
    heading = math.degrees(math.atan2(y, x))
    if heading < 0:
        heading += 360
    return heading


if __name__ == "__main__":
    result = calibrate(duration_sec=30, sample_delay=0.05)

    ox = result["offset_x"]
    oy = result["offset_y"]
    oz = result["offset_z"]

    print("\nLive corrected heading. Press Ctrl+C to stop.\n")
    while True:
        x, y, z = corrected_magnetometer_reading(ox, oy, oz)
        hdg = heading_degrees(x, y)
        print(f"x={x:8.2f} y={y:8.2f} z={z:8.2f} heading={hdg:7.2f}°", end="\r")
        time.sleep(0.1)