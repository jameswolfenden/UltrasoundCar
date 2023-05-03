import NewCar_pico_4wd as car
import time
import math

# parameters

gain = range(1,17,1) # gain

# Pipe parameters & scan position, # scan of blockage parameters
pipe_radius = [15]  # radius
r = [7.5]  # sensor radius
n = 8 #number of point when moving
points = 36 # number of points scan
speed = 5

position = 0

while True:
filebuffer1 = ""
filebuffer2 = ""
    print(radius)
    
    # create a new file for each scan
    filename = "scan_" + str(position*15) + ".csv"
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

    
    car.move("forward", 50)
    time.sleep(0.27)
    car.move("stop")
    position +=1

