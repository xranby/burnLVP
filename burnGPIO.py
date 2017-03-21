###############################
#
#  burnGPIO.py
#
#  GPIO definition interface
#
#  Put All your pin definition here
#  All class will use this file for reference
#
#

global PIC_CLK
global PIC_DATA
global PIC_MCLR
global PIC_PGM

global isCHIP


isCHIP=False

# check CHIP or it is a raspberry Pi

f = open('/proc/cpuinfo','r')
cpuinfo = f.read()
f.close()


if cpuinfo.find('Allwinner') >0 :
   #  ------  chip  ------
   print('C.H.I.P GPIO')
   isCHIP=True
   import CHIP_IO.GPIO as MGPIO
#   MGPIO.toggle_debug()
   MGPIO.cleanup()
   #CLK GPIO
   PIC_CLK = 'I2C-SCL'

   #DATA GPIO 
   PIC_DATA = 'I2C-SDA'

   #MCLR GPIO
   PIC_MCLR = 'UART1-RX'

   #PGM
   PIC_PGM = 'UART1-TX'

else:
   #  ------ Raspberry Pi --
   print('Raspberry Pi GPIO')
   import RPi.GPIO as MGPIO

   #CLK GPIO
   PIC_CLK = 7

   #DATA GPIO 
   PIC_DATA = 24

   #MCLR GPIO
   PIC_MCLR = 21

   #PGM
   PIC_PGM = 26


# Because the current CHIP_IO python module function setup()
# can't be used more than once. I create a class to go around
# and use the function direction() which doesn't exist on the Raspberry Pi
   
class MyGPIO:

    def __init__(self, gpio):
        self.BOARD = gpio.BOARD
        self.OUT   = gpio.OUT
        self.IN    = gpio.IN
        self.gpio  = gpio
    
    def setup(self, pin, INOUT):
        if isCHIP:
            self.gpio.direction(pin,INOUT)
        else:
            self.gpio.setup(pin,INOUT)
            
    def setwarnings(self, flag):
        self.gpio.setwarnings(flag)

    def setmode(self , mode):
        if not isCHIP:
           self.gpio.setmode(GPIO.BOARD)
     
    def output(self, pin , value):
        self.gpio.output(pin,value)

    def input(self, pin):
        return self.gpio.input(pin)

    
GPIO = MyGPIO(MGPIO)

def Setup_Interface():
  GPIO.setwarnings(False)
  GPIO.setmode(GPIO.BOARD)
  MGPIO.setup(PIC_MCLR,GPIO.OUT)
  MGPIO.output(PIC_MCLR,False)
  MGPIO.setup(PIC_CLK,GPIO.OUT)
  MGPIO.setup(PIC_DATA,GPIO.OUT)
  MGPIO.setup(PIC_PGM,GPIO.OUT)
  


