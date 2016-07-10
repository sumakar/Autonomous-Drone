##########################################################################################################################
# Project : Autonomous Drone											                                               	#
# Hardware: Raspberry pi ,Arducopter , laptop or desktop ,ultrasonic sensor HC-SR04					                    #
#	  : Arducopter(APM2.6)												                                                #
# Author  : Keyur Rakholiya												                                                #
# Author  : Akshit Gandhi												                                                #
#															                                                            #
#Objective: By running this code, drone will go point A to point B autonomously.									    #
#															                                                            #
# Requrinment: preinstalled dronekit library.											                                #
#########################################################################################################################

#importing all the necessary library
from dronekit import connect, VehicleMode, LocationGlobalRelative
import time




print "connecting to vehicle...."
vehicle = connect('/dev/ttyAMA0', baud = 57600)             #connecting Rpi to APM on baudrte of 57600
print "connected"

#changing vehicle mode to stabilize
print "\nSet Vehicle.mode = (currently: %s)" % vehicle.mode.name
while not vehicle.mode=='GUIDED':
    vehicle.mode = VehicleMode('GUIDED')    #changing mode to guided first
    vehicle.command.upload()                #write the command in apm

print "vehicle mode: %s" % vehicle.mode     #printing current vehicle mode

# ARMING the vehicle
vehicle.armed = True
while not vehicle.armed:
    vehicle.armed = True
    vehicle.flush()         #write command to apm
    print " trying to change mode and arming ..."
    time.sleep(1)

print "its armed"





#defining a function
def arm_and_takeoff(aTargetAltitude):
    print "Taking off!"
    vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude

    # Wait until the vehicle reaches a safe height before processing the goto (otherwise the command 
    #  after Vehicle.simple_takeoff will execute immediately).
    while True:
        print " Altitude: ", vehicle.location.global_relative_frame.alt 
        #Break and return from function just below target altitude.        
        if vehicle.location.global_relative_frame.alt>=aTargetAltitude*0.95: 
            print "Reached target altitude"
            break
        time.sleep(1)

arm_and_takeoff(10) # 10 meter is target altitude here

print "Set default/target airspeed to 3"
vehicle.airspeed = 3    #speed in m/s

print "Going towards first point for 30 seconds ..."
point1 = LocationGlobalRelative(-35.361354, 149.165218, 20)  #give longitude latitude ,altitude(in meter)
vehicle.simple_goto(point1)                                 #function calling

# sleep so we can see the change in map
time.sleep(30)

print "Going towards second point for 30 seconds (groundspeed set to 10 m/s) ..."
point2 = LocationGlobalRelative(-35.363244, 149.168801, 20)     #second point location
vehicle.simple_goto(point2, groundspeed=10)

# sleep so we can see the change in map
time.sleep(30)

print "Returning to Launch"
vehicle.mode = VehicleMode("RTL")   #changing mode to Return To Launch

#Close vehicle object before exiting script
print "Close vehicle object"
vehicle.close() #disARMED the vehicle

