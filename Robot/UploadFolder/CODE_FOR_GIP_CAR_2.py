#machine.reset()
import pico_4wdNew as car
import time
from ws import WS_Server
import math
        
measure_num = 1
all_data = []

inPipe = True


car.move("forward", 20)
time.sleep(5)
car.move("stop")

car.v_servo.set_angle(0)
car.h_servo.set_angle(0)

time.sleep(1)

gain = 14
car.srf.set_gain(gain)

while inPipe:

    car.move("forward", 10)

    for point in car.scan_points(6):
        v,h=car.get_angles(point,0.2,0.25)
        car.h_servo.set_angle(h)
        car.v_servo.set_angle(v)
        distance = car.srf.read_distance()
        time.sleep(0.25)
        print("Angle: " +str(math.degrees(point))+", distance: " + str(distance))
    
        if distance < 7:
            car.move("stop", 10)
            # inital set of the sensor 

            car.h_servo.set_angle(90)
            car.v_servo.set_angle(60)
            time.sleep(0.4)
    

            # verticle scan

            for v_angle in range(60, -40, -10):
                car.v_servo.set_angle(v_angle)
                time.sleep(0.05)
        
        
                # horizontal scan

                for h_angle in range(90, -95, -10):
                    car.h_servo.set_angle(h_angle)
                    time.sleep(0.01)
            
                    #distances and gain
                    gain = 14
                    car.srf.set_gain(gain)
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
            inPipe = False 



while scan:

# inital set of the sensor 

    car.h_servo.set_angle(90)
    car.v_servo.set_angle(60)
    time.sleep(0.4)
    

# verticle scan

    for v_angle in range(60, -40, -10):
        car.v_servo.set_angle(v_angle)
        time.sleep(0.05)
        
        
# horizontal scan

        for h_angle in range(90, -95, -10):
            car.h_servo.set_angle(h_angle)
            time.sleep(0.01)
            
            #distances and gain
            gain = 14
            car.srf.set_gain(gain)
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
    # Driving through the pipe - knowing when to stop, turn or go straight on
            
    for angle in [-95,0,90]:
                
        car.v_servo.set_angle(0)
        car.h_servo.set_angle(angle)
        time.sleep(0.5)
        distance1 = car.sonar.get_distance()
        dist12 = []
        dist1.append(dist12)
        dist12.append(round(distance1, 3))
                
        if angle == 0 and distance1 > 10:
            car.move("forward", 10)
            time.sleep(0.1)
            car.move("stop")
                
        elif angle < -85 and distance>45: 
            car.move("right", 4)
            time.sleep(0.3)
            car.move("stop")
                
        elif angle >85 and distance>45:
            car.move("right", 4)
            time.sleep(0.3)
            car.move("stop")
                
        else:
            inPipe = False


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



# changing the data to equal the pipe diameters

""" have a file with the max distances on then compare then to the file list_data and then if the distances in list data are bigger
then replace with the max distance """


import math

# pipe information 

pipe_diameter = 30
position_of_sensor = [0,-5,0] #centre of pipe = [0,0,0] - a robot ultra sonic sensor position
scan_postion = 201
scan_places_on_pipe = [[0,0,scan_postion],[0,(pipe_diameter/2),scan_postion],[0,-(pipe_diameter/2),scan_postion],[(pipe_diameter/2),0,scan_postion],[-(pipe_diameter/2),0,scan_postion]]

print(scan_places_on_pipe[0][1])
print(position_of_sensor[1])

distance = math.sqrt((scan_places_on_pipe[0][0] - position_of_sensor[0])**2 + (scan_places_on_pipe[0][1] - position_of_sensor[1])**2 + (scan_places_on_pipe[0][2] - position_of_sensor[2])**2)
print(distance)

cc =(scan_places_on_pipe[0][1] - position_of_sensor[1])**2
print(cc)

# calculating distances 

for position in range(0,5,1):
    max_distance = math.sqrt((scan_places_on_pipe[position][0] - position_of_sensor[0])**2 + (scan_places_on_pipe[position][1] - position_of_sensor[1])**2 + (scan_places_on_pipe[position][2] - position_of_sensor[2])**2) 
    print(max_distance)