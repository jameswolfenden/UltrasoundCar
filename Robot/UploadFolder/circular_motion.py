import math
import pico_4wdNew as car
import time

def get_angles(angle, distance, radius):
    v_angle = math.degrees(math.atan2(radius*math.cos(angle),distance))
    h_angle = math.degrees(math.atan2(radius*math.sin(angle),distance))
    return v_angle,h_angle

def scan_points(points):
    split = int(360/points)
    return [float(x)/180*math.pi for x in range(0,360,split)]

while True:
    for point in scan_points(6):
        v,h=get_angles(point,0.2,0.25)
        car.h_servo.set_angle(h)
        car.v_servo.set_angle(v)
        time.sleep(0.25)
        print("Angle: " +str(math.degrees(point))+", distance: " + str(car.sonar.get_distance()))
    