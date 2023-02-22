import pico_4wdNew as car
import time


car.h_servo.set_angle(0)
car.v_servo.set_angle(0)
time.sleep(1)

gain_data_full = []

car.srf.set_range(6) #  max of like 1.5m idk

for angle in range(-90,91,10):
    car.h_servo.set_angle(angle)
    car.v_servo.set_angle(0)
    time.sleep(0.5)
    gain_data = []
    for i in range(1,17):
        car.srf.set_gain(i)
        ttime = car.srf.read_time(0.07)
        print("gain ", i, " time ", ttime)
        gain_data.append(ttime)
    gain_data_full.append(gain_data)

# save 2d list to csv
filename = "gain_pings.csv"
f = open(filename, "w")
for i,item in enumerate(gain_data_full):
    for j,item2 in enumerate(item):
        f.write(str(item2))
        if j<len(item)-1:
            f.write(',')
    if i<len(gain_data_full)-1:
        f.write('\n')
f.close()