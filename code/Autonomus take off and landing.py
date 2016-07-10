##########################################################################################################################
# Project : Autonomous Drone												#
# Hardware: Raspberry pi 												#
#	  : Arducopter(APM2.6)												#
# Author  : Keyur Rakholiya												#
# Author  : Akshit Gandhi												#
#															#
# Objective: Drone will takeoff after running this code. and it will goes to certain height(adjustable) and after       #
#            certain time it                                                                                            #
# will land on the ground.												#
#															#
# Requrinment: preinstalled dronekit library, RPIO library.					                        #
#########################################################################################################################

from dronekit import connect, VehicleMode ,LocationGlobalRelative  #import dronekit library
import time
from RPIO import PWM
vehicle = connect('/dev/ttyAMA0', baud = 57600)
throttle = PWM.Servo()  #making an object to generate software PWM named throttle (for varying throttle)

#vehicle must be in guided mode because we are using dronekit library for changing vehicle's mode. NOT PWM.

print "\nSet Vehicle.mode = (currently: %s)" % vehicle.mode.name # printing current mode

#this loop will change the mode of vehicle
while not vehicle.mode=='GUIDED':
    vehicle.mode = VehicleMode('GUIDED') #setting mode to guided
    vehicle.commands.upload() #write the command in APM

print "vehicle mode: %s" % vehicle.mode

#this while loop is for arming the vehicle
vehicle.armed = True
while not vehicle.armed:
    vehicle.armed = True  #set armed vehicle attribute to True
    vehicle.flush() #write changes in APM
    print " trying to change mode and arming ..."
    time.sleep(1)

print "its armed"
print "\nSet Vehicle.mode =  (currently: %s)" % vehicle.mode.name
print "Taking off!"

vehicle.simple_takeoff(2) # Take off to target altitude,here is 2meter

try: #failsafe try catch loop
	while True:
		altitude = vehicle.location.global_relative_frame.alt
		print " Altitude: ", altitude   #print the current altitude
		print "sensors:",vehicle.attitude #print the roll, pitch and yaw values

        	if vehicle.location.global_relative_frame.alt>=2*0.95: #condition check to ensure that the altitude reaches 95% of the target and if it has reached the loop will break
	            	print "Reached target altitude"
			print "Final Altitude:", vehicle.location.global_relative_frame.alt  #print the altitude reached
        	    	break
        		time.sleep(1)

#it will hold the altitude for 2 seconds
	time.sleep(2)
	
#it will now goes to in land mode
	while not vehicle.mode=='LAND':
    		vehicle.mode = VehicleMode('LAND')
    		vehicle.commands.upload() 
except Keyboardinterrupt:
	throttle.set_servo(27,1100) #if there is a keyboard interrupt we set the throttle to minimum so that we can reduce the speed the motor in our case PWM 1100 means motors will switch off
print "\nSet Vehicle.mode =  (currently: %s)" % vehicle.mode.name
print vehicle.armed
vehicle.close() # after every code completion this should be the last step as it releases all the connections with APM.
