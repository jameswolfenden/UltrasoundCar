import math
import pico_4wdNew as car
import time

car.h_servo.set_angle(0)
car.v_servo.set_angle(0)
time.sleep(1)

car.srf.set_range(20) #  max of like 1.5m idk

offset = -0.03

for radius in range(5,16,5):
    car.h_servo.set_angle(0)
    car.v_servo.set_angle(-45)
    time.sleep(0.25)
    gain_data_full = []
    for angle in car.scan_points(8):
        v,h=car.get_angles(angle,0.2,radius/100,offset)
        car.h_servo.set_angle(h)
        car.v_servo.set_angle(v)
        time.sleep(0.25)
        gain_data = []
        for i in range(1,17):
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
    