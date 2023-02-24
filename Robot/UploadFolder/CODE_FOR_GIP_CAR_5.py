# machine.reset()
import pico_4wdNew as car
import time
import math

# Write Files
filename = "all_data.csv"
f = open(filename, "w")
f.close()

# parameters
gain = range(10, 16, 1)  # gain

# Pipe parameters & scan position
r = 15  # radius
d1 = 15  # distance from sensor
h1 = -3  # height of sensor
n1 = 4  # number of points

# scan of blockage parameters
d2 = 15  # distance from sensor
number_of_circles = range(0, 16, 3)
n2 = 8  # number of points

# initial test and reset of the car
car.move("forward", 0)
time.sleep(0.5)
car.move("stop")

car.v_servo.set_angle(0)
car.h_servo.set_angle(0)

time.sleep(1)

# set up
measure_num = 1

inPipe = True

while inPipe:

    car.move("forward", 0)

    for point in car.scan_points(n1):
        v, h = car.get_angles(point, d1, r, h1)
        car.h_servo.set_angle(h)
        car.v_servo.set_angle(v)
        distance = car.srf.read_distance(0.07)
        time.sleep(0.25)

        if distance < 20:
            car.move("stop", 1)
            inPipe = False

            break

            # initial set of the sensor

            car.h_servo.set_angle(90)
            car.v_servo.set_angle(60)
            
            time.sleep(1)

# scan of blockage
for ci in number_of_circles:
    c = ci
    print(c)
    
    # create a new file for each scan
    filename = "scan_data_" + str(ci) + ".csv"
    f = open(filename, "w")
    f.close()

    # each loop
    for point in car.scan_points(n2):
        v, h = car.get_angles(point, d2, c, h1)
        car.h_servo.set_angle(h)
        car.v_servo.set_angle(v)
        time.sleep(0.25)

        # changin gain
        gain_time_data = []
        for g in gain:
            car.srf.set_gain(g)
            time_data = car.srf.read_time(0.07)
            
            # add the data to the list
            gain_time_data.append(time_data)

        # save the data to the file for this scan and this gain
        with open(filename, "a") as f:
            f.write(str(gain_time_data) + "\n")

time.sleep(0.1)

car.h_servo.set_angle(0)
car.v_servo.set_angle(0)

time.sleep(0.1)
