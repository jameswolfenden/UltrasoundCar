from NewCar_pico_rdp import Motor, Speed, h_Servo, v_Servo, WS2812, mapping, SRF10
from machine import Pin, ADC
import time
import math

left_front  = Motor(17, 16, dir=1) # motor 1
right_front = Motor(15, 14, dir=-1) # motor 2
left_rear   = Motor(13, 12, dir=1) # motor 3
right_rear  = Motor(11, 10, dir=-1) # motor 4
motors = [left_front, right_front, left_rear, right_rear]

h_servo = h_Servo(18)
v_servo = v_Servo(20)


srf_1 = SRF10(1,0,0)
srf_2 = SRF10(3,2,1)

speed = Speed(8, 9)

np =  WS2812(Pin(19, Pin.OUT), 24)
# slowly increase power of the motor, to avoid hight reverse voltage from motors
def set_motor_power_gradually(*powers):
    flags = [True, True, True, True]
    while flags[0] or flags[1] or flags[2] or flags[3]:
        for i, motor in enumerate(motors):
            # print(motor.power, powers[i])
            if motor.power > powers[i]:
                motor.power -= 1
            elif motor.power < powers[i]:
                motor.power += 1
            else:
                flags[i] = False
        time.sleep_ms(1)

# set power 
def set_motor_power(*powers):
    for i, motor in enumerate(motors):
        motor.power = powers[i]

def stop():
    set_motor_power(0, 0, 0, 0)

def move(dir, power=0):
    if dir == "forward":
        set_motor_power_gradually(power, power, power, power)
    elif dir == "backward":
        set_motor_power_gradually(-power, -power, -power, -power)
    elif dir == "left":
        set_motor_power_gradually(-power, power, -power, power)
    elif dir == "right":
        set_motor_power_gradually(power, -power, power, -power)
    else:
        set_motor_power_gradually(0, 0, 0, 0)

def scan_points(points):
    split = int(180/(points-1))
    return [float(x) for x in range(-90,90,split)]

def get_sensor_position(angle_degrees, radius):
    angle_radians = math.radians(angle_degrees)
    sensor_position = [radius*math.sin(angle_radians), radius*math.cos(angle_radians), 0]
    return sensor_position

def stop(self):
    self.h_servo.duty_u16(0)
