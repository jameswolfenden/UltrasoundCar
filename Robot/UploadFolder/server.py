from machine import UART
import time


def sendUART(toSend):
    uart.write(toSend+'\r\n')

def readUART():
    recv=bytes()
    while uart.any()>0:
        recv+=uart.read(1)
    res=recv.decode('utf-8')
    return res

def sendReceiveUART(toSend, wait=1):
    sendUART(toSend)
    print("Sent "+toSend)
    #time.sleep(wait)
    read = readUART()
    print("Receive " +read)
    if (read.rstrip()[-2:]!="OK"):
        print("im not ok")
        time.sleep(wait)
    return(read)

def sendString(toSend):
    length=str(len(toSend))
    send='AT+CIPSEND=0,'+length
    sendReceiveUART(send)
    sendReceiveUART(toSend)



uart = UART(1,115200)


sendReceiveUART('AT+RST')
sendReceiveUART('AT+GMR')
sendReceiveUART('AT+CWMODE=3')
sendReceiveUART('AT+CWSAP?')
sendReceiveUART('AT+CWSAP="ultrasound robot","password123",5,3')
sendReceiveUART('AT+CIPMUX=1')
sendReceiveUART('AT+CIPSERVER=1,80')


time.sleep(1)

for i in range(10):
    sendString(str(i))
