import machine
import sys
import time

###############################################################################
# Settings

# Assign chip select (CS) pin (and start it high)
cs = machine.Pin(17, machine.Pin.OUT)

# Initialize SPI
spi = machine.SPI(0,
                  baudrate=1000000,
                  polarity=1,
                  phase=1,
                  bits=8,
                  firstbit=machine.SPI.MSB,
                  sck=machine.Pin(18),
                  mosi=machine.Pin(19))

###############################################################################
# Functions

def reg_write(spi, cs, data):
    """
    Write 1 byte to the specified register.
    """
    
    # Construct message (set ~W bit low, MB bit low)
    msg = bytearray()
    msg.append(0x00)
    msg.append(data)
    
    # Send out SPI message
    cs.value(0)
    time.sleep(0.01)
    spi.write(msg)
    cs.value(1)

    

###############################################################################
# Main

cs.value(1)
time.sleep(0.01)


level=0
print('level:' + str(level))
reg_write(spi,cs,level)

time.sleep(20)
for level in range(0, 256,8):
    print('level:' + str(level))
    reg_write(spi,cs,level)
    time.sleep(1)

