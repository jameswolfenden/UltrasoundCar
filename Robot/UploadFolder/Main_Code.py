#machine.reset()
import pico_4wdNew as car
import time
from ws import WS_Server


NAME = 'my_4wd_car'

# AP Mode
WIFI_MODE = "ap"
SSID = ""
PASSWORD = "12345678"

def on_receive(data):
    print(data)

ws = WS_Server(name=NAME, mode=WIFI_MODE, ssid=SSID, password=PASSWORD)
ws.on_receive = on_receive
ws.start()


time.sleep(2)

#os.remove("list_data.csv")

## make sure file exists befre deleting
        
measure_num = 1
all_data = []

inPipe = True


car.move("forward", 1)
time.sleep(0.5)
car.move("stop")

car.v_servo.set_angle(0)
car.h_servo.set_angle(0)

time.sleep(1)


while inPipe:

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
            
            #distances
            distance = car.sonar.get_distance()
            print('distance:%s'% distance)
            
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


