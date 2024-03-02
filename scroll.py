import sys
sys.path.append('/home/n8/c/DFRobot_RGB1602_RaspberryPi/python')
from datetime import datetime
import time
import signal
import RPi.GPIO as GPIO
import rgb1602

def handle_interrupt(sig, frame):
  print('\n\ngoodbye!\n\n')
  sys.exit(0)
  
signal.signal(signal.SIGINT, handle_interrupt)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(16, GPIO.IN)
GPIO.setup(17, GPIO.IN)
GPIO.setup(18, GPIO.IN)
GPIO.setup(19, GPIO.IN)
GPIO.setup(20, GPIO.IN)


class LcdControl:
  def __init__(self):
    self.lcd = rgb1602.RGB1602(16,2)
    self.lcd.cursor()
  
    # Define keys
    self.key_in  = 0
  
    self.btnRIGHT  = 0
    self.btnUP     = 1
    self.btnDOWN   = 2
    self.btnLEFT   = 3
    self.btnSELECT = 4
    self.instructions = "Scroll <-->"
    self.long_message = "this message is entirely too long to fit"
    self.scroll_offset = 0
    self.blink_ms = 800
  
    self.lcd.setCursor(0,0)
    self.lcd.printout(self.instructions)
    self.lcd.setCursor(0,1)
    self.lcd.printout(self.long_message)
    
  
    self.cursor_state = False
    self.edit_mode = False
    self.cursor_col = 0
    self.cursor_row = 0
    self.last_cursor_change = datetime.now()



  #Read the key value
  def read_LCD_buttons(self):
    key_in16 = GPIO.input(16)
    key_in17 = GPIO.input(17)
    key_in18 = GPIO.input(18)
    key_in19 = GPIO.input(19)
    key_in20 = GPIO.input(20)

    if (key_in16 == 1):
      return self.btnSELECT
    if (key_in17 == 1):
      return self.btnUP
    if (key_in18 == 1):
      return self.btnDOWN
    if (key_in19 == 1):
      return self.btnLEFT
    if (key_in20 == 1):
      return self.btnRIGHT

  def blink_cursor(self):    
    now = datetime.now()
    ms_since_last = (now - d.last_cursor_change).total_seconds() * 1000

    if ms_since_last > self.blink_ms:
      self.cursor_state = not self.cursor_state
      self.last_cursor_change = now
      if self.cursor_state:
        self.lcd.cursor_on()
      else:
        self.lcd.cursor_off()


  def move_cursor(self, lcd_key):
    if lcd_key == self.btnSELECT:
      if self.edit_mode:
        self.lcd.stopBlink()
        self.edit_mode = False
      else:
        self.edit_mode = True
        self.lcd.blink()

    if lcd_key == self.btnRIGHT:
      self.cursor_col = (self.cursor_col + 1) % 16
    elif lcd_key == self.btnLEFT:
      self.cursor_col = (self.cursor_col - 1) % 16
    elif lcd_key == self.btnUP:
      self.cursor_row = (self.cursor_row - 1) % 2
    elif lcd_key == self.btnDOWN:
      self.cursor_row = (self.cursor_row + 1) %2

    self.lcd.setCursor(self.cursor_col, self.cursor_row)

  
  def scroll_and_return_cursor(self, lcd_key):
    if (lcd_key == self.btnRIGHT):
      self.scroll_offset = max(0, self.scroll_offset + 1)
    elif (lcd_key == self.btnLEFT):
      self.scroll_offset = max(0, self.scroll_offset - 1)

    self.lcd.setCursor(0,0)
    self.lcd.printout(self.instructions + f' +{self.scroll_offset:2}')

    self.lcd.setCursor(0,1)
    self.lcd.printout(self.long_message[self.scroll_offset:])

    self.lcd.setCursor(0,0)



if __name__ == '__main__':
  d = LcdControl()
  
  while True:
    lcd_key = d.read_LCD_buttons()  #  Reading keys
    time.sleep(0.2)
    lcd_key = d.read_LCD_buttons()

    d.move_cursor(lcd_key)
    
