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

car.h_servo.set_angle(0)
car.v_servo.set_angle(0)
time.sleep(1)

car.srf.set_range(20) #  max of like 1.5m idk

for radius in range(5,16,5):
    car.h_servo.set_angle(0)
    car.v_servo.set_angle(45)
    time.sleep(0.5)
    for angle in range(0,360,10):
        v,h=get_angles(angle/180*math.pi,0.2,radius)
        car.h_servo.set_angle(h)
        car.v_servo.set_angle(v)
        time.sleep(0.5)
        gain_data_full = []
        for i in range(1,17):
            gain_data = []
            car.srf.set_gain(i)
            ttime = car.srf.read_time(0.07)
            print("gain ", i, " time ", ttime)
            gain_data.append(ttime)
        gain_data_full.append(gain_data)

    # save 2d list to csv
    filename = "radius_"+str(radius)+".csv"
    f = open(filename, "w")
    for i,item in enumerate(gain_data_full):
        for j,item2 in enumerate(item):
            f.write(str(item2))
            if j<len(item)-1:
                f.write(',')
        if i<len(gain_data_full)-1:
            f.write('\n')
    f.close()


# while True:
#     for point in scan_points(6):
#         v,h=get_angles(point,0.2,0.25)
#         car.h_servo.set_angle(h)
#         car.v_servo.set_angle(v)
#         time.sleep(0.25)
#         print("Angle: " +str(math.degrees(point))+", distance: " + str(car.srf.read_distance()))
    