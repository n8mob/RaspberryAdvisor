import sys
sys.path.append('/home/n8/c/DFRobot_RGB1602_RaspberryPi/python')
import rgb1602
import time

if __name__ == '__main__':
    lcd = rgb1602.RGB1602(16,2)
    lcd.printout("hello, world")
    time.sleep(1)
    i = 0
    while i < 200:
        lcd.setCursor(0, 1)
        lcd.printout(i)
        i += 1
        time.sleep(0.1)
        
