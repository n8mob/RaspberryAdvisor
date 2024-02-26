import sys
sys.path.append('/home/n8/c/DFRobot_RGB1602_RaspberryPi/python')
import rgb1602
import time

if __name__ == '__main__':
    lcd = rgb1602.RGB1602(16,2)
    lcd.printout(sys.argv[1])

