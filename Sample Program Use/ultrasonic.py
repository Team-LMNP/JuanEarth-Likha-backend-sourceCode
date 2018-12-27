import RPi.GPIO as GPIO
import time



TRIG = 35 
ECHO = 37

TRIG2 = 33 
ECHO2 = 31

print "Distance Measurement In Progress"
GPIO.setmode(GPIO.BOARD)
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

GPIO.setup(TRIG2,GPIO.OUT)
GPIO.setup(ECHO2,GPIO.IN)

def read1 () :
  GPIO.output(TRIG, False)
  GPIO.output(TRIG, True)
  time.sleep(0.00001)
  GPIO.output(TRIG, False)
  while GPIO.input(ECHO)==0:
    pulse_start = time.time()
  while GPIO.input(ECHO)==1:
    pulse_end = time.time()
  pulse_duration = pulse_end - pulse_start
  distance = pulse_duration * 17150
  distance = round(distance, 2)
  print "Distance1:",distance,"cm"

  if distance < 13 :
    print "Open"
  

def read2 () :
  GPIO.output(TRIG2, False)
  GPIO.output(TRIG2, True)
  time.sleep(0.00001)
  GPIO.output(TRIG2, False)
  while GPIO.input(ECHO2)==0:
    pulse_start = time.time()
  while GPIO.input(ECHO2)==1:
    pulse_end = time.time()
  pulse_duration = pulse_end - pulse_start
  distance = pulse_duration * 17150
  distance = round(distance, 2)
  print "Distance2:",distance,"cm"

while True:
  read1()
  
  #read2()
  time.sleep(1)


