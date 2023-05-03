#machine.reset()
import NewCar_pico_4wd as car
import time
import math

print("hello")


# Write Files
filename = "all_data.csv"
f = open(filename, "w")
f.close()
"""
car.h_servo.set_angle(0)
print(car.srf_2.read_distance(0.07))
time.sleep(2)
car.h_servo.set_angle(-90)
print(car.srf_2.read_distance(0.07))
time.sleep(2)
car.h_servo.set_angle(95)
print(car.srf_2.read_distance(0.07))
time.sleep(2)
time.sleep(1)
"""
# parameters

gain = range(1,17,1) # gain

# Pipe parameters & scan position, # scan of blockage parameters
pipe_radius = [15]  # radius
r = [7.5]  # sensor radius
n = 8 #number of point when moving
points = 36 # number of points scan
speed = 5

"""
start_time = time.ticks_ms() # get start time
car.move("forward", 1)
time.sleep(10)
car.move("stop")
end_time = time.ticks_ms()
distance_travelled = ((end_time - start_time)/1000) * car.speed.get_speed()
dists = car.speed.get_mileage()
print(dists)
print(distance_travelled)
time.sleep(15)
"""
# set up
measure_num = 1

inPipe = False
car.h_servo.set_angle(-90)
time.sleep(2)
start_time = time.ticks_ms() # get start time

while inPipe:
    
    # initial test and reset of the car
    car.move("forward", speed)
    car.srf_1.set_gain(4)
    car.srf_2.set_gain(4)
        
    for angle in car.scan_points(n):
        car.h_servo.set_angle(angle)
        Y = car.speed.get_speed()
        distance_1 = car.srf_1.read_distance(0.07)
        distance_2 = car.srf_2.read_distance(0.07)
        print(distance_1)
        print(distance_2)
        
        if angle > 88:
           car.h_servo.set_angle(-90)
           time.sleep(0.1)
           car.h_servo.stop()

        if distance_1 < 25:
            car.move("stop", 1)
            x = (25 - distance_1)/(Y)
            car.move("backward",speed)
            time.sleep(x)
            car.move("stop",1)
            inPipe = False
            break
        
        if distance_2 < 25:
            car.move("stop", 1)
            Y = car.speed.get_speed()
            x = (25 - distance_2)/(Y)
            car.move("backward",speed)
            time.sleep(x)
            car.move("stop",1)
            inPipe = False
            break

end_time = time.ticks_ms()
distance_travelled = car.speed.get_mileage()
print(distance_travelled)

filebuffer1 = ""
filebuffer2 = ""
# scan of blockage
for radius in r:
    print(radius)
    
    # create a new file for each scan
    filename = "scan_data_time_" + str(radius) + ".csv"
    f = open(filename, "w")
    f.close()

    print(car.scan_points(points))
    # each loop
    for angle in car.scan_points(points):
        car.h_servo.set_angle(angle)
        #time.sleep(0.1)
        #car.h_servo.stop()
        print(angle)
        #time.sleep(0.1)
        #distance = car.srf_1.read_distance(0.07)
        #time.sleep(0.1)
        sensor_position = car.get_sensor_position(angle, radius)
        print(sensor_position)
        
        # changin gain
        gain_time_data_1 = []
        gain_time_data_2 = []
        for g in gain:
            car.srf_1.set_gain(g)
            time_data_1 = car.srf_1.read_time(0.07)
            car.srf_2.set_gain(g)
            time_data_2 = car.srf_2.read_time(0.07)
            
            # add the data to the list
            gain_time_data_1.append(time_data_1)
            gain_time_data_2.append(time_data_2)

        filebuffer1 += str(gain_time_data_1) + "\n"
        filebuffer2 += str(gain_time_data_2) + "\n"
    # save the data to the file for this scan and this gain
    with open(filename, "a") as f:
        f.write(filebuffer1)    
        f.write(filebuffer2)

time.sleep(0.1)

car.h_servo.set_angle(0)
time.sleep(0.1)
car.h_servo.stop()

time.sleep(0.1)

#x1 = (distance_travelled)/(Y/100)
#print(x1)
car.move("backward",speed)
#time.sleep(x1+0.15)
car.move("stop",10)