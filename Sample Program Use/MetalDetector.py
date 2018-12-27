import RPi.GPIO as GPIO
import time

polPin = 36
detPin = 38
resetPin = 40

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(polPin, GPIO.IN)
GPIO.setup(detPin, GPIO.IN)
GPIO.setup(resetPin, GPIO.OUT), GPIO.output(resetPin, GPIO.HIGH)

time.sleep(1)
GPIO.output(resetPin, GPIO.HIGH)      # Reset No Detect
GPIO.output(resetPin, GPIO.LOW)       # Reset No Detect
time.sleep(1)

while True :
    
    DET = GPIO.input(detPin)
    POT = GPIO.input(polPin)

    #print "DET", DET, "POT", POT
    #print "POT", POT

    if DET == 0 and POT == 1 :
        print "ALUMINUM DETECTED"
        while DET == 0 and POT == 1 :
            DET = GPIO.input(detPin)
            POT = GPIO.input(polPin)
        
    elif DET == 0 and POT == 0 :
        print "METAL DETECTED"
        while DET == 0 and POT == 0 :
            DET = GPIO.input(detPin)
            POT = GPIO.input(polPin)
