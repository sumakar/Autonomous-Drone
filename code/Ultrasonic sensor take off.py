import RPi.GPIO as GPIO
import time
import threading
from dronekit import connect, VehicleMode ,LocationGlobalRelative
import getch
from RPIO import PWM


class sonar1(threading.Thread):
        global distance
        def run(self):
                while True:
			GPIO.output(TRIG,True)
                	time.sleep(0.00001)
                	GPIO.output(TRIG,False)
                	while GPIO.input(ECHO)==0:
                        	pass
                	pulse_start = time.time()
	
                	while GPIO.input(ECHO)==1:
                        	pass
                	pulse_end = time.time()

                	pulse_duration = pulse_end - pulse_start

                	distance = pulse_duration * 17000

                	distance = round(distance, 2)
                	distance = distance/100
                #	print "Distance:",distance,"m"
             		time.sleep(0.7) 
                	return distance

                
GPIO.setmode(GPIO.BCM)
TRIG = 20 
ECHO = 16
distance = 0
th = 1200
print "Distance Measurement In Progress"

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

GPIO.output(TRIG, False)
print "Waiting For Sensor To Settle"
time.sleep(2)


####################################################
print "connecting to vehicle...."
vehicle = connect('/dev/ttyAMA0', baud = 57600)
print "connected"

print "\nSet Vehicle.mode = GUIDED (currently: %s)" % vehicle.mode.name
while not vehicle.mode=='STABILIZE':
    vehicle.mode = VehicleMode('STABILIZE')
    vehicle.flush()

print "vehicle mode: %s" % vehicle.mode

vehicle.armed = True
while not vehicle.armed:
    vehicle.armed = True
    vehicle.flush()
    print " trying to change mode and arming ..."
    time.sleep(1)

print "its armed"

##################################################
throttle = PWM.Servo()
mode = PWM.Servo()

mode.set_servo(26,1200)
throttle.set_servo(27,1200)# pin 13, pin 14 is Ground
##################################################
print "Taking off!"

t = sonar1()
distance = t.run()

print "Initial" , distance

try:
        while True:
                distance = t.run()

		print "inside"
                if distance < 0.65 and th < 1700:
                
                        th = th + 20
                        throttle.set_servo(27,th)
                        print th
                        time.sleep(1.3)
                        print "Current Height" ,distance
                elif distance > 0.65 and distance < 1.2:
			#th = th + 10
                        #throttle.set_servo(27,th)
                	#time.sleep(1.2)
                        #print th
                        #print "Current Height" ,distance
                        mode.set_servo(26,1550) #setting in alt-hold mode
                        time.sleep(0.5)
			print " mode is %s" % vehicle.mode.name
			break
                else:
                        print "decreasing"
                        th = th - 10
                        throttle.set_servo(27,th)
                        
except KeyboardInterrupt:
        mode.set_servo(26,1800)
        print "land"
	time.sleep(5)
	vehicle.armed = False
	while not vehicle.armed:
		vehicle.armed = False
		vehicle.flush()
	print "Disarmed"


time.sleep(5)
print "land"
mode.set_servo(26,1800)
GPIO.cleanup()


