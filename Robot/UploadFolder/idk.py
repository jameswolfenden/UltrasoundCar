import NewCar_pico_4wd as car
import time
import math

print("hello")

gain = range(1,17,1) # gain

car.srf_1.set_range(255)
car.srf_2.set_range(255)

angles = range(-90, 81,10)
car.h_servo.set_angle(0)
time.sleep(2)
car.h_servo.set_angle(-90)
time.sleep(2)
for angle in angles:
    car.h_servo.set_angle(angle)
    print(angle)
    time.sleep(2)

gain_time = []
for g in gain:
    car.srf_1.set_gain(g)
    car.srf_2.set_gain(g)
    readfrom = car.srf_1.read_time(0.1)
    readfrom2 = car.srf_2.read_time(0.1)
    print("gain ", g, " distance: ", readfrom, " distance2: ", readfrom2)



