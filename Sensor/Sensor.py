1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
33
34
35
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
 
TRIG = 23
ECHO = 24
 
print "Distance Measurement In Progress"
 
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
 
GPIO.output(TRIG, False)
print "Waiting For Sensor To Settle"
time.sleep(2)
 
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
 
print "Distance:",distance,"cm"
 
GPIO.cleanup()