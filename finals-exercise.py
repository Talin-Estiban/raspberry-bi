#Final exercise by: Talin Estiban & Rula Abu Tair 

# importing libraries 
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from time import sleep
import board
import busio
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import adafruit_mcp4725

GPIO.setwarnings(False) # Disable warnings
GPIO.setmode(GPIO.BCM) # Use BCM pin numbering


#lcd configuration bits 
lcd_rs = digitalio.DigitalInOut(board.D26)
lcd_en = digitalio.DigitalInOut(board.D19)
lcd_d4 = digitalio.DigitalInOut(board.D13)
lcd_d5 = digitalio.DigitalInOut(board.D6)
lcd_d6 = digitalio.DigitalInOut(board.D5)
lcd_d7 = digitalio.DigitalInOut(board.D11)
GPIO.setup(17,GPIO.OUT,initial=GPIO.HIGH)
lcd_columns = 20
lcd_rows = 4

# Initialise the lcd 
lcd = characterlcd.Character_LCD_Mono(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6,lcd_d7, lcd_columns, lcd_rows)
lcd.clear()
i2c = busio.I2C(board.SCL, board.SDA)
# Create a ADC instance.
ads = ADS.ADS1015(i2c)
# Create a DAC instance.
dac = adafruit_mcp4725.MCP4725(i2c,address=0x60)
op = AnalogIn(ads, ADS.P0)   # the operation type
num1 = AnalogIn(ads, ADS.P1) # the first number --> A
num2 = AnalogIn(ads, ADS.P2) # the second number -->B

# function that prints on the lcd
def print (A,B,op,result='none'):
    lcd.message = "A    B  op    result"+"\n"+str(A)+" "+str(B)+" "+str(op)+"   "+str(result)
    sleep(2)
    
while True:
    # reading the opcode + A + B
    operation=round(op.voltage,1)
    A=round(num1.voltage,1)
    B=round(num2.voltage,1)
    result='none' #default value of the result(no result from the operations)

    # addition 

    if (0.2<operation and operation<0.4):
        lcd.clear()
        GPIO.output(17,GPIO.HIGH)
        operation='sum'
        result=round(A+B,1)
        if result>3.3:	# the DAC maximum voltage is 3.3
            result=3.3
        dac.raw_value = int(((result)*4095)/3.3)  # normalizing voltage to be processed by DAC 
        print(A,B,operation,result)

    # substraction

    elif (0.5<operation and operation<0.7):
        lcd.clear()
        GPIO.output(17,GPIO.HIGH)
        operation='sub'
        if B>A :
            result=round(B-A,1)
            dac.raw_value = int(((result)*4095)/3.3)
        else :
            result=round(A-B,1)
            dac.raw_value = int(((result)*4095)/3.3)
        print(A,B,operation,result)

    # multiplication 

    elif (0.9<operation and operation<1.2):
        lcd.clear()
        GPIO.output(17,GPIO.HIGH)
        operation='mult'
        result=round(A*B,1)
        if result>3.3: # the DAC maximum voltage is 3.3
            result=3.3
        dac.raw_value = int(((result)*4095)/3.3)
        print(A,B,operation,result)

    # division

    elif (1.3<operation and operation<1.7):
        lcd.clear()
        GPIO.output(17,GPIO.HIGH)
        operation='div'
        if (A==0 or B==0): # if either of the numbers=0 then that's an arror
            result='error'
            dac.raw_value = 0
            GPIO.output(17,GPIO.LOW)
        else:
            result=round(A/B,1)
            if result>3.3: # the DAC maximum voltage is 3.3
                result=3.3
                dac.raw_value = 4095 
            dac.raw_value = int(((result)*4095)/3.3)
        print(A,B,operation,result)

    # division without remainder

    elif (1.9<operation and operation<2.2):
        lcd.clear()
        GPIO.output(17,GPIO.HIGH)
        operation='fdiv'
        if (A==0 or B==0):
            result='error'
            dac.raw_value = 0
            GPIO.output(17,GPIO.LOW)
        else:
            result=round(A//B,1)
            if result>3.3:
                result=3.3
                dac.raw_value = 4095 
            dac.raw_value = int(((result)*4095)/3.3)
        print(A,B,operation,result)

    # power

    elif (2.4<operation and operation<2.6):
        lcd.clear()
        GPIO.output(17,GPIO.HIGH)
        operation='pow'
        result=round(A**B,1)
        if result>3.3:
            result=3.3
        dac.raw_value = int(((result)*4095)/3.3)
        print(A,B,operation,result)

    # modulo = remainder of division 

    elif (2.7<operation and operation<3):
        lcd.clear()
        GPIO.output(17,GPIO.HIGH)
        operation='mod'
        result=round(A%B,1)
        dac.raw_value = int(((result)*4095)/3.3)
        print(A,B,operation,result)

    # comparing A and B 

    elif (3.1<operation and operation<3.3):
        lcd.clear()
        GPIO.output(17,GPIO.HIGH)
        operation='>'
        if B>A :
            result=B
            dac.raw_value = int(((result)*4095)/3.3)
        else :
            result=A
            dac.raw_value = int(((result)*4095)/3.3)
        print(A,B,operation,result)

# voltage isn't in any ranges --> no operation
    else:
        lcd.clear()
        GPIO.output(17,GPIO.LOW) # turning on the led (in other operations we turn it off)
        dac.raw_value = 0
        result=0
        operation="no op"
        print(A,B,operation,result)


    
