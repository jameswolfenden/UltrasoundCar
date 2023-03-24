import NewCar_pico_4wd as car
import time
import math

print("hello")

gain = range(1,17,1) # gain


for g in gain:
    car.srf_2.set_gain(g)
    print("gain ", g, " distance: ", car.srf_2.read_distance(0.07))