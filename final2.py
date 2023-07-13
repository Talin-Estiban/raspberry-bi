# Done by: Tain Estiban 211376199, and Rula abu tair 206630337
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from time import sleep


import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd

GPIO.setwarnings(False) # Disable warnings
GPIO.setmode(GPIO.BCM) # Use BCM pin numbering

lcd_rs = digitalio.DigitalInOut(board.D26)
lcd_en = digitalio.DigitalInOut(board.D19)
lcd_d4 = digitalio.DigitalInOut(board.D13)
lcd_d5 = digitalio.DigitalInOut(board.D6)
lcd_d6 = digitalio.DigitalInOut(board.D5)
lcd_d7 = digitalio.DigitalInOut(board.D11)

# buttons and LED
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP) #time set up
GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP) # hour adjustment
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_UP) #minute adjustment
GPIO.setup(21, GPIO.OUT, initial=GPIO.LOW)

# Modify this if you have a different sized character LCD
lcd_columns = 20
lcd_rows = 4


# Initialise the lcd and the clock variables
lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6,lcd_d7, lcd_columns, lcd_rows)
second=0
minute=0
hour=0
minute_al=0
hour_al=0
flag=True		#we added this flag so we can set more than once the alarm and also so that the alarm just rings in the first 3 seconds
lcd.clear()

# function for changing the clock
def clock_change (hour,minute,second,hour_al,minute_al,second_al):
    lcd.message="Current time "+ str(hour)+":"+str(minute)+":"+str(second)+"\n"+"ALarm at "+ str(hour_al)+":"+str(minute_al)
    
# using this function we can set the current time at the beginning of the run time 
def setting_clock (hour,minute):
    print("set current time")
    while (GPIO.input(17)==0) or hour==0 or minute==0:
        if (GPIO.input(27)==0):
            sleep(0.5)
            hour+=1
            clock_change(hour,minute,second,hour_al,minute_al,second_al)
        if (GPIO.input(22)==0):
            sleep(0.5)
            minute+=1
            clock_change(hour,minute,second,hour_al,minute_al,second_al)
    return (hour,minute)
    
    
    
hour,minute=setting_clock(hour,minute)
while True:

# running the current time 
    sleep(1)
    second+=1
    clock_change (hour,minute,second,hour_al,minute_al,second_al)
    if second==60:
        minute+=1
        second=0
        lcd.clear()
        clock_change (hour,minute,second,hour_al,minute_al,second_al)
    if minute==60:
        hour=+1
        minute=0
        clock_change (hour,minute,second,hour_al,minute_al,second_al)

# change the alarm clock
    while (GPIO.input(17)==0):
        flag=True
        if (GPIO.input(27)==0):
            sleep(0.5)
            hour_al+=1
            clock_change(hour,minute,second,hour_al,minute_al,second_al)
        if (GPIO.input(22)==0):
            sleep(0.5)
            minute_al+=1
            clock_change(hour,minute,second,hour_al,minute_al,second_al)

#checking if the alarm set is equal to the actual time
    if hour==hour_al and minute==minute_al and flag:
        GPIO.output(21,GPIO.HIGH)
        sleep(3)
        second=0
        flag=False
        GPIO.output(21,GPIO.LOW)
    
    
    
    

