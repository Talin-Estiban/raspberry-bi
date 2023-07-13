import RPi.GPIO as GPIO 
from time import sleep
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
# ROWS
GPIO.setup(40,  GPIO.OUT, initial=GPIO.HIGH) # Set pin 7 as  row 1
GPIO.setup(11, GPIO.OUT, initial=GPIO.HIGH) # Set pin 11 as row 2
GPIO.setup(13, GPIO.OUT, initial=GPIO.HIGH) # Set pin 13 as row 3
GPIO.setup(15, GPIO.OUT, initial=GPIO.HIGH) # Set pin 15 as row 4

#--------------------------------------------------------------------------

#----------------------Inputs---------------------------------------------
GPIO.setup(31, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pin 31 as column 5
GPIO.setup(33, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pin 33 as column 6
GPIO.setup(35, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pin 35 as column 7
GPIO.setup(37, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Set pin 37 as column 8
#-------------------------LED---------------------------------------------
GPIO.setup(12,GPIO.OUT,initial=GPIO.LOW)
# FUNCTION
def ReadKeyPad():
    
    #-------------------------------------------------------
    GPIO.output(40,GPIO.LOW) # Set 7 - Low check 1,2,3,A
    if(GPIO.input(31) == 0):
        sleep(0.5)
        return("1")
    elif(GPIO.input(33) == 0):
        sleep(0.5)
        return("2")
    elif(GPIO.input(35) == 0):
        sleep(0.5)
        return("3")
    elif(GPIO.input(37) == 0):
        sleep(0.5)
        return("A")
    GPIO.output(40,GPIO.HIGH) # Set 7 - High
    #-------------------------------------------------------
  
    #-------------------------------------------------------
    GPIO.output(11,GPIO.LOW) # Set 11 - Low check 4,5,6,B
    if(GPIO.input(31) == 0):
        sleep(0.5)
        return("4")
    elif(GPIO.input(33) == 0):
        sleep(0.5)
        return("5")
    elif(GPIO.input(35) == 0):
        sleep(0.5)
        return("6")
    elif(GPIO.input(37) == 0):
        sleep(0.5)
        return("B")
    GPIO.output(11,GPIO.HIGH) # Set 11 - High
    #-------------------------------------------------------

    #-------------------------------------------------------
    GPIO.output(13,GPIO.LOW) # Set 13 - Low check 7,8,9,C
    if(GPIO.input(31) == 0):
        sleep(0.5)
        return("7")
    elif(GPIO.input(33) == 0):
        sleep(0.5)
        return("8")
    elif(GPIO.input(35) == 0):
        sleep(0.5)
        return("9")
    elif(GPIO.input(37) == 0):
        sleep(0.5)
        return("C")
    GPIO.output(13,GPIO.HIGH) # Set 13 - High
    #-------------------------------------------------------

    #-------------------------------------------------------
    GPIO.output(15,GPIO.LOW) # Set 15 - Low check *,0,#,D
    if(GPIO.input(31) == 0):
        sleep(0.2)
        return("*")
    elif(GPIO.input(33) == 0):
        sleep(0.2)
        return("0")
    elif(GPIO.input(35) == 0):
        sleep(0.2)
        return("#")
    elif(GPIO.input(37) == 0):
        sleep(0.2)
        return("D" )
    GPIO.output(15,GPIO.HIGH) # Set 15 - High
# OPERATION
times=0
while True:
    
    def three_times ():
        print("you've entered the wrong code more than 3 times please try again in 10 sec")
        n=0
        while n<5:
            GPIO.output(12,GPIO.HIGH)
            n+=1
            sleep(2)
            GPIO.output(12,GPIO.LOW)
            sleep(2)
        
        return("you can try again now")  
        
    pin=["1","2","3","A"]
    x=[]
    i=0
    while i<4 :
         x.append(ReadKeyPad()) 
         if x[i]==None:
             x.pop(i)
         else :
             i+=1
    print("The code you intered is:")
    print(x)
    for i in range(4):
        if x[i]==pin[i]:
            result=True
        else :
            result=False
            break
    if result:
        print("correct pin")
        GPIO.output(12,GPIO.HIGH)
        sleep(3)
        GPIO.output(12,GPIO.LOW)
        result=False
    else:
        
        if times<3:
            times+=1
            print(str(times) + " incorrect pin")
            
        else :
            print(three_times())
            times=0
            
            
    
    

       
             
             
             
            
                  
	    
	














