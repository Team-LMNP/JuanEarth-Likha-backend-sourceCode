import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)        # Set pinmode if BOARD or BCM
GPIO.setup(11, GPIO.OUT)        # Set pinmode of servo and make it output
pwm=GPIO.PWM(11, 50)            # Set the Hz of pwm pinouts
pwm.start(0)                    # always start 0hz

def SetAngle(angle):
	duty = angle / 18 + 2
	GPIO.output(11, True)
	pwm.ChangeDutyCycle(duty)
	sleep(1)
	GPIO.output(11, False)
	pwm.ChangeDutyCycle(0)

def servo1Open ():
        SetAngle(55)
        sleep(1)
def servo1Close():
        SetAngle(90)
        sleep(1)
	
print "Open"
servo1Open()
sleep(3)
print "Close"
servo1Close()
pwm.stop()                      # use if nothing to do
GPIO.cleanup()                  # clean all gpio pinout
