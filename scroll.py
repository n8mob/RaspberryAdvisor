import sys
sys.path.append('/home/n8/c/DFRobot_RGB1602_RaspberryPi/python')
import rgb1602
import time


import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(16, GPIO.IN)
GPIO.setup(17, GPIO.IN)
GPIO.setup(18, GPIO.IN)
GPIO.setup(19, GPIO.IN)
GPIO.setup(20, GPIO.IN)

lcd = rgb1602.RGB1602(16,2)

# Define keys
lcd_key = 0
key_in  = 0

btnRIGHT  = 0
btnUP     = 1
btnDOWN   = 2
btnLEFT   = 3
btnSELECT = 4


#Read the key value
def read_LCD_buttons():
  key_in16 = GPIO.input(16)
  key_in17 = GPIO.input(17)
  key_in18 = GPIO.input(18)
  key_in19 = GPIO.input(19)
  key_in20 = GPIO.input(20)
  
  if (key_in16 == 1):
    return btnSELECT
  if (key_in17 == 1):
    return btnUP
  if (key_in18 == 1):
    return btnDOWN
  if (key_in19 == 1):
    return btnLEFT
  if (key_in20 == 1):
    return btnRIGHT

instructions = "Scroll <-->"
long_message = "this message is entirely too long to fit"
scroll_offset = 0

lcd.setCursor(0,0)
lcd.printout(instructions)
lcd.setCursor(0,1)
lcd.printout(long_message)

while True:
  lcd_key = read_LCD_buttons()  #  Reading keys
  time.sleep(0.2)
  lcd_key = read_LCD_buttons()

  if (lcd_key == btnRIGHT):
    scroll_offset = max(0, scroll_offset + 1)
  elif (lcd_key == btnLEFT):
    scroll_offset = max(0, scroll_offset - 1)

  lcd.setCursor(0,0)
  lcd.printout(instructions + f' +{scroll_offset:2}')

  lcd.setCursor(0,1)
  lcd.printout(long_message[scroll_offset:])
