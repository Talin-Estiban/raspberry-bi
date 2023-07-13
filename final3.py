# Done by: Talin Estiban 211376199, and Rula Abutair 206630337

import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from time import sleep
import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd

GPIO.setwarnings(False) # Disable warnings
GPIO.setmode(GPIO.BCM) # Use BCM pin numbering

# intializing the i2c communication with the ADC
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1015(i2c)
chan = AnalogIn(ads, ADS.P0)

#lcd and led
lcd_rs = digitalio.DigitalInOut(board.D26)
lcd_en = digitalio.DigitalInOut(board.D19)
lcd_d4 = digitalio.DigitalInOut(board.D13)
lcd_d5 = digitalio.DigitalInOut(board.D6)
lcd_d6 = digitalio.DigitalInOut(board.D5)
lcd_d7 = digitalio.DigitalInOut(board.D11)

GPIO.setup(27,GPIO.OUT,initial=GPIO.HIGH)   #green led
GPIO.setup(22,GPIO.OUT,initial=GPIO.HIGH)   #red led

# Modify this if you have a different sized character LCD
lcd_columns = 20
lcd_rows = 4

# Initialise the lcd 
lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6,lcd_d7, lcd_columns, lcd_rows)
# wipe LCD screen before we start
lcd.clear()

# function of blinking the led 3 times with frequency corresponding to the voltage
def blink (frequency,num_led):
    n=0
    while n < 3:
        GPIO.output(num_led,GPIO.LOW)
        sleep((1/frequency*2))
        GPIO.output(num_led,GPIO.HIGH)
        sleep((1/frequency*2))
        n+=1

# main function
while True:
    voltage=chan.voltage
    sleep(2)
	# We devide the voltage bu 0.5 so we can know the frequency such that every 0.5 volt is 1 HZ
    freq=round((voltage)/0.5)
    lcd.message=("frequency is"+str(freq)+"\n"+"voltage is"+str(voltage))
	#if the frequency is above 2.3 then we are over ranged and we blink the red light
    if voltage>2.3:
        lcd.clear()
        lcd.message = str("OVER RANGE")
        blink(freq,22)
	#if the frequency is above 2.3 then we are in range and we blink the green light
    elif freq>0:
        lcd.clear()
        lcd.message = str("RANGE OK")
        blink(freq,27)
    
