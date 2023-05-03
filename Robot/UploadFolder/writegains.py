import NewCar_pico_4wd as car
import time
import math

print("hello")

gain = range(1,17,1) # gain

car.srf_1.set_range(254)

gain_time = []
for g in gain:
    car.srf_1.set_gain(g)
    readfrom = car.srf_1.read_time(0.04)
    print("gain ", g, " distance: ", readfrom)
    gain_time.append(readfrom)


with open("plate70pole40-2.csv", "a") as f:
    f.write(str(gain_time))
