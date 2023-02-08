from wsNew import WS_Server
import time
import pico_4wdNew as car

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

inPipe = True

car.move("forward", 10)
time.sleep(0.5)
car.move("stop")

car.v_servo.set_angle(0)
car.h_servo.set_angle(0)

time.sleep(5)

while inPipe:
    ws.loop()
#    car.move("forward", 50)
    car.h_servo.set_angle(90)
    time.sleep(10)
#    car.move("stop")
    ws.send_data_string("[")
    for angle in range(90, -91, -10):
        car.h_servo.set_angle(angle)
        time.sleep(0.075)
        distance = car.sonar.get_distance()
        if angle==0 and distance<10:
            inPipe = False
        ws.send_data_string(str(round(distance, 3)))
    ws.send_data_string("]")

ws.send_data_string("stop")
car.servo.set_angle(0)

