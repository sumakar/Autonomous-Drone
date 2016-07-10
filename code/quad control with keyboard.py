##########################################################################################################################
# Project : Autonomous Drone												#
# Hardware: Raspberry pi ,Arducopter , laptop or desktop ,ultrasonic sensor HC-SR04					#
#	  : Arducopter(APM2.6)												#
# Author  : Keyur Rakholiya												#
# Author  : Akshit Gandhi												#
#															#
# Objective: By using this code, quadcopter can controlled by using laptop keyboard. we can also change the different   #
#             modes also												#
#															#
# Requrinment: Pre-installed Dronekit, RPIO, getch libraries								#
#########################################################################################################################
from dronekit import connect, VehicleMode ,LocationGlobalRelative #import dronekit library
import time
import getch
from RPIO import PWM

#this section will connect tho the APM via MAVProxy protocol
print "connecting to vehicle...."
vehicle = connect('/dev/ttyAMA0', baud = 57600)  #we give the port to connect and the baudrate as parameters, so that there is a connection established at that port.
print "connected"

#changing vehicle mode to stabilize
print "\nSet Vehicle.mode = (currently: %s)" % vehicle.mode.name
while not vehicle.mode=='STABILIZE':
    vehicle.mode = VehicleMode('STABILIZE')
    vehicle.commands.upload()  #writing the changes to APM

print "vehicle mode: %s" % vehicle.mode

# ARMING the vehicle
vehicle.armed = True
while not vehicle.armed:
    vehicle.armed = True #set the armed attribute to true
    vehicle.flush() #for arming sequence we write the changes to APM
    print " trying to change mode and arming ..."
    time.sleep(1)

print "its armed"

# initialize servo objects with PWM function
roll = PWM.Servo()
pitch = PWM.Servo()
throttle = PWM.Servo()
yaw = PWM.Servo()
mode = PWM.Servo()

# start PWM on servo specific GPIO no, this is not the pin no but it is the GPIO no 
roll.set_servo(17,1520)# pin 11
pitch.set_servo(18,1520)# pin 12
throttle.set_servo(27,1100)# pin 13, pin 14 is Ground
yaw.set_servo(22,1520)# pin 15
mode.set_servo(26,1200)# pin 37
# assign global min and max values
th_min = 1100
th_max = 2000
r_min = 1100
r_max = 1900
p_min = 1100
p_max = 1900
y_min = 1100
y_max = 1900
a_min = 980
a_max = 2300
th =1100
r = 1520
p = 1520
y = 1520
a = False
flag = 0

#print "\nSet Vehicle.mode =  (currently: %s)" % vehicle.mode.name

print "Taking off!"
print "controll drone from keyboard"




try:
    while True:
# waiting for key strokes
        key = getch.getch()
        if key == 'w':   #if w key is pressed increase the throttle if it is less than th_max else keep the maximum throttle and if thr is less than min keep the throttle at its minimum value
            
            th = th + 10 #increasing throttle by 10
            if (th < th_min):
                th = 1100
                throttle.set_servo(27,th) 
            elif (th > th_max):
                th = 2000
                throttle.set_servo(27,th)
            else: 
                throttle.set_servo(27,th)
            print 'th :' + str(th)
            
        elif key == 's': #if s key is pressed reduce the throttle based on th_min, th_max and the current throttle.
            th = th - 10 #reducing throttle.
            if (th < th_min):
                th = 1100
                throttle.set_servo(27,th)
            elif (th > th_max):
                th = 2000
                throttle.set_servo(27,th)
            else:
                throttle.set_servo(27,th)
            print 'th :' + str(th)

            #yaw left
        elif key == 'a': #if 'a' key is pressed yaw will be rotated left for 0.3 seconds
            yaw.set_servo(22,1350)
	    print "yaw left"
            time.sleep(0.3)
            yaw.set_servo(22,1500)

        #yaw right
        elif key == 'd': #if d key is pressed yaw will be rotated right for 0.3 seconds
            yaw.set_servo(22,1650)
	    print "yaw right"
            time.sleep(0.3)
            yaw.set_servo(22,1500)

        #roll left
        elif key == '4': #if 4 key is pressed roll movement towards right will be given for 0.3 seconds
            roll.set_servo(17,1350)
	    print "roll left"
            time.sleep(0.3)
            roll.set_servo(17,1500)

        #roll right
        elif key == '6': #if 6 key is pressed roll movement towards left will be given for 0.3 seconds
            roll.set_servo(17,1650)
	    print "roll right"
            time.sleep(0.3)
            roll.set_servo(17,1500)
            
        #pitch forward
        elif key == '8': #if 8 key is pressed pitch movement forwards will be given for 0.3 seconds
            pitch.set_servo(18,1650)
	    print "pitch forward"
            time.sleep(0.3)
            pitch.set_servo(18,1500)
            
	#pitch back
	elif key == '2': #if 2 key is pressed pitch movement backwards will be given for 0.3 seconds
		pitch.set_servo(18,1350)
		print "pitch back"
		time.sleep(0.3)
		pitch.set_servo(18,1500)

        #atlitude hold
	elif key == 'h': #if h key is pressed the APM will go into altitude hold mode
		mode.set_servo(26,1550) #setting PWM 1550 on channel 5 on APM so that we can go into alt_hold mode. We have previously configured ALT_Hold on MISSION Planner at this PWM value
		time.sleep(0.5)
		print " mode is %s" % vehicle.mode.name
		
      
	#land mode
	elif key == 'l': #if l key is pressed the quad will go into landing mode. The mode was set in MISSION PLANNER at this PWM on cannel 5
		mode.set_servo(26,1800)
		time.sleep(0.5)
		print " mode is %s " % vehicle.mode.name

	#stabilize mode
	elif key =='5' and th<1200: #if 5 key is pressed when throttle is below 1200 quad will go into STABILIZE mode.
                mode.set_servo(26,1200)
                time.sleep(0.5)
                print "mode is %s" % vehicle.mode.name
                
except KeyboardInterrupt: #if there is keyboard interrupt the throttle will reduce and will initiate a disarming sequence.
	throttle.set_servo(27,1100)
	while vehicle.armed:
		vehicle.armed = False #disarming the quad
	        print "disarming"
		time.sleep(1)
		vehicle.flush()
print "DISARMED"
vehicle.close() #close all vehicle objects
