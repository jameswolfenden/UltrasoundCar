from machine import Pin, I2C
import time

# Initialize I2C bus
i2c = I2C(0,freq=9600, scl=Pin(1), sda=Pin(0))

# SRF10 I2C address
SRF10_ADDR = 0x70

# SRF10 register addresses
SRF10_COMMAND = 0x00
SRF10_RANGE = 0x02
SRF10_GAIN = 0x01

def set_gain(gain):
    # Write the gain value to the gain register
    write_reg(SRF10_GAIN, gain)

def write_reg(register, value):
    i2c.writeto_mem(SRF10_ADDR, register, bytearray([value]))

def read_reg(register, num_bytes):
    return i2c.readfrom_mem(SRF10_ADDR, register, num_bytes)

def read_distance():
    # Initiate range measurement
    write_reg(SRF10_COMMAND, 0x51)
    time.sleep(0.07)
    # Read 2-byte range value
    range_bytes = read_reg(SRF10_RANGE, 2)
    distance = (range_bytes[0] << 8) + range_bytes[1]
    return distance


devices = i2c.scan()
print(str(devices))

# Example usage
while True:
    for gain in range(0,17):
        set_gain(gain)
        distance = read_distance()
        print("Distance:", distance, "cm at gain: ", gain)
        time.sleep(1)
