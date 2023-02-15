import machine
import uasyncio as asyncio
import pico_4wdNew as car
import time, utime
from queue import Queue

# UART connection to the WiFi module
uart = machine.UART(1, baudrate=115200)  # Replace z with the UART number for the WiFi module

data_queue = Queue()  # Queue to hold the data to be sent
receive_queue = Queue()  # Queue to hold the data received from the WiFi module
busy = False  # Flag to indicate whether the WiFi module is busy

async def send_receive_string_uart(data,ack='OK',timeout=2000):
    """Function to asynchronously send and receive data from the UART"""
    uart.write(data+'\r\n')
    t = utime.ticks_ms()
    while (utime.ticks_ms() - t) < timeout:
        s=uart.read()
        if(s != None):
            s=s.decode('utf-8')
            print(s)
            if(s.find(ack) >= 0):
                return s
    print("No "+ack+" response!!!! Timed out!!!!")
    return None

async def send_receive_data_uart(data): # i manually wrote this so no error stuff
    length=str(len(data))
    send='AT+CIPSEND=0,'+length
    await send_receive_string_uart(send)
    return await send_receive_string_uart(data)


async def send_data_to_wifi(data):
    """Function to asynchronously send data to the WiFi module"""
    global busy
    busy = True
    await asyncio.sleep(0)  # Yield control to other tasks
    # Wait for the response from the WiFi module
    response = await send_receive_data_uart(data)
    if response == "pong":
        # Your code to handle the response goes here
        # Check if there is data in the queue
        if not data_queue.empty():
            # Dequeue the next data from the queue and send it
            data = await data_queue.get()
            response = await send_receive_data_uart(data)
            if response == "pong":
                # Your code to handle the response goes here
                await receive_queue.put(response)
    busy = False

async def send_ping_to_wifi():
    """Function to asynchronously send a ping to the WiFi module"""
    global busy
    while True:
        await asyncio.sleep(2)  # Wait for 2 seconds
        if not busy:
            busy = True
            # Wait for the response from the WiFi module
            response = await send_receive_data_uart("ping")
            if response == "pong":
                # Your code to handle the response goes here
                await receive_queue.put(response)
            busy = False

async def control_robot():
    """Function to continuously control the robot"""
    global busy
    while True:
        # Read the ultrasound data
        ultrasound_data = car.sonar.get_distance()

        # Control the robot based on the wifi data
        if not receive_queue.empty():
            # Get the data from the queue
            received_data = await receive_queue.get()
            # Your code to use the received data to control the robot goes here


        # Control the robot based on the ultrasound data
        if ultrasound_data == 0:
            # Your code to control the robot goes here
            print("move something!!!")

        # Send the ultrasound data to the WiFi module asynchronously
        if not busy:
            busy = True
            response = await send_receive_data_uart(str(ultrasound_data))
            if response == "pong":
                # Your code to handle the response goes here
                print(response)
            busy = False
        else:
            # Enqueue the data to be sent later
            await data_queue.put(str(ultrasound_data))

def setup_wifi():
    send_receive_uart('AT+RST')
    send_receive_uart('AT+GMR')
    send_receive_uart('AT+CWMODE=3')
    send_receive_uart('AT+CWSAP?')
    send_receive_uart('AT+CWSAP="ultrasound robot","password123",5,3')
    send_receive_uart('AT+CIPMUX=1')
    send_receive_uart('AT+CIPSERVER=1,80')
    

def send_receive_uart(data):
    asyncio.run(send_receive_string_uart(data))


setup_wifi()

# Create the event loop and run the functions
loop = asyncio.get_event_loop()
loop.create_task(control_robot())
loop.create_task(send_ping_to_wifi())
loop.run_forever()