# measure distance
import pico_4wdNew as car
import time

while True:
    print(car.sonar.get_distance())
    time.sleep(0.01)
