from machine import UART
import time,utime


def sendUART(toSend):
    uart.write(toSend+'\r\n')

def readUART():
    recv=bytes()
    while uart.any()>0:
        recv+=uart.read(1)
    res=recv.decode('utf-8')
    return res

def sendReceiveUART(toSend, wait=0):
    sendUART(toSend)
    print("Sent "+toSend)
    time.sleep(wait)
    read = readUART()
    print("Receive " +read)
    if (read.rstrip()[-2:]!="OK"):
        print("im not ok")
        time.sleep(wait)
    return(read)

def sendCMD(cmd,timeout=2000,ack='OK'):
    sendUART(cmd)
    t = utime.ticks_ms()
    while (utime.ticks_ms() - t) < timeout:
        s=uart.read()
        if(s != None):
            s=s.decode('utf-8')
            print(s)
            if(s.find(ack) >= 0):
                return True
    return False

def sendString(toSend):
    length=str(len(toSend))
    send='AT+CIPSEND=0,'+length
    sendCMD(send)
    sendCMD(toSend)



uart = UART(1,115200)


sendCMD('AT+RST')
sendCMD('AT+GMR')
sendCMD('AT+CWMODE=3')
sendCMD('AT+CWSAP?')
sendCMD('AT+CWSAP="ultrasound robot","password123",5,3')
sendCMD('AT+CIPMUX=1')
time.sleep(1)
sendCMD('AT+CIPSERVER=1,80')
time.sleep(1)
readUART()
sendCMD('AT+CIPSERVER?')
time.sleep(1)
readUART()

time.sleep(0.5)

for i in range(10):
    sendString(str(i))
