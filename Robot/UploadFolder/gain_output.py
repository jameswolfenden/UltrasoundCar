import pico_4wdNew as car
import time


car.h_servo.set_angle(0)
car.v_servo.set_angle(0)
time.sleep(1)

gain_data = []

car.srf.set_range(20) #  max of like 1.5m idk

for i in range(1,17):
    car.srf.set_gain(i)
    time = car.srf.read_time(0.1)
    print("gain ", i, " time ", time)
    gain_data.append(time)

filename = "gain_pings.csv"
f = open(filename, "w")
for i,item in enumerate(gain_data):
    f.write(str(item))
    if i<len(gain_data)-1:
        f.write(',')
f.close()

    
