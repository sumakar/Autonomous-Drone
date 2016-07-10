This folder contains the codes which we had used for making the quadcopter autonomous.
NOTE: You need a working UART connection between Raspberry Pi and APM via MAVProxy. Refer the tutorials section for step-by-step guide.
The codes have an arming and disarming sequence which is mandatory, next is a failsafe system by which if the quadcopter goes out of your control you can get immediately land it or disarm it by pressing CTRL-C.

We have used APM firmware ACv3.2.1 with Dronekit Library v2.5.0. the api reference for the library is: http://python.dronekit.io/automodule.html , for the github repo you can visit https://github.com/dronekit/dronekit-python .