import pico_4wd as car
import time
#import os

#os.remove("list_data.csv")

## make sure file exists befre deleting
        
measure_num = 1
list_tot = []
inPipe = True

car.move("forward", 10)
time.sleep(0.5)
car.move("stop")


car.servo.set_angle(0)

time.sleep(5)

while inPipe:
    car.move("forward", 50)
    car.servo.set_angle(90)
    time.sleep(1)
    car.move("stop")
    list_tmp = []
    for angle in range(90, -91, -10):
        car.servo.set_angle(angle)
        time.sleep(0.075)
        #list_tmp.append(angle)
        distance = car.sonar.get_distance()
        list_tmp.append(round(distance, 3))
        if angle==0 and distance<10:
            inPipe = False
    list_tot.append(list_tmp)

# Write Files
file = open("list_data.csv", "w")

for w in range(len(list_tot[0:])):
    file.write(str(list_tot[w])[1:-1] + "\n")
    file.flush()

car.servo.set_angle(0)

file.close()