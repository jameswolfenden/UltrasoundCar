#machine.reset()
import pico_4wdNew as car
import time
import math

# parameters
gain = 16 #gain
#car.srf.set_gain(gain)

# Pipe parameters & scan position

r = 15 # radius
d1 = 20 # distance from sensor
h = 0 # height of sensor
n = 8 # number of points


# scan of blockage parameters
d2 = 20 # distance from sensor
number_of_circles = range(0,16,1)
n = 4 # number of points

#initial test and reset of the car

car.move("forward", 1)
time.sleep(0.5)
car.move("stop")

car.v_servo.set_angle(0)
car.h_servo.set_angle(0)

time.sleep(1)

#set up
measure_num = 1
all_data = []

inPipe = True

while inPipe:

    car.move("forward", 10)

    for point in car.scan_points(n):
        v,h = car.get_angles(point, d1,r, h)
        car.h_servo.set_angle(h)
        car.v_servo.set_angle(v)
        print(h)
        print(v)
        distance = car.srf.read_distance(0.07)
        time.sleep(0.25)
        print("Angle: " +str(math.degrees(point))+", distance: " + str(distance))

        if distance < 20:
            car.move("stop", 1)
            inPipe = False
            
            break 
            
            # inital set of the sensor 

            car.h_servo.set_angle(90)
            car.v_servo.set_angle(60)
            time.sleep(0.4)
            
  

            # scan of blockage
for ci in number_of_circles:
    c = ci
    print(c)

    # each loop
    for point in car.scan_points(n):
        v,h = car.get_angles(point, d2, c, h)
        car.h_servo.set_angle(h)
        car.v_servo.set_angle(v)
        distance = car.srf.read_distance(0.07)
        time.sleep(1)
        print("Angle: " +str(math.degrees(point))+", distance: " + str(distance))
"""
                    #distances and gain
                    distance = car.srf.read_distance()
                    print("Distance:", distance, "cm at gain: ",gain)
            
                    #list of angle vertical
                    v_angle_data = []
                    v_angle_data.append(v_angle)
                    print('v_angle:%s'% v_angle)
                    v_angle_data.append(round(distance, 3))
    
                    #list of angle horozontally
                    print('h_angle:%s'% h_angle)
                    v_angle_data.append(h_angle)
                    all_data.append(v_angle_data)
            
                    time.sleep(0.1)
                    dist1 = []
                    """
            
# Write Files
filename = "all_data.csv"
f = open(filename, "w")
for row in all_data:
    f.write(str(row) + "\n")
f.close()
time.sleep(0.1)


car.h_servo.set_angle(0)
car.v_servo.set_angle(0)


time.sleep(0.1)


"""
            for v_angle in range(60, -60, -40):
                car.v_servo.set_angle(v_angle)
                time.sleep(0.05)
        
                # horizontal scan

                for h_angle in range(90, -95, -30):
                    car.h_servo.set_angle(h_angle)
                    time.sleep(0.01)

"""