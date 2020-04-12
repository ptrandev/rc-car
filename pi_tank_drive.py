#!/usr/bin/env python3

# I'll give you the first two lines of code - you're welcome!
# we will use networktables and gpiozero modules
# specifically, we will use the NetworkTablesInstand and the PWMOutputDevice classes
import sys
from time import sleep
from networktables import NetworkTables
from gpiozero import PWMOutputDevice

##########
# CONFIG #
##########

# networktables server
nt_server = "10.0.0.29"

################################################################################

# start the networktables client, wait for connection to settle
NetworkTables.initialize(server=nt_server)
sleep(1)

# review the gpiozero documentation for PWMOutputDevice
# https://gpiozero.readthedocs.io/en/stable/api_output.html#pwmoutputdevice
# NOTE: if you find that the default frequency (100) doesn't spin your motors, 
# then increase by increments of 100 until you find a value that works

# create the left forward device on GPIO pin 17 (IN1)
# create the left reverse device on GPIO pin 27 (IN2)
# NOTE: If the car moves in the wrong direction then switch the above - left forward = 27, left reverse = 17
left_forward = PWMOutputDevice(17, frequency=100)
left_reverse = PWMOutputDevice(27, frequency=100)

# create the right forward device on GPIO pin 23 (IN3)
# create the right reverse device on GPIO pin 24 (IN4)
# NOTE: If the car moves in the wrong direction then switch the above - right forward = 24, right reverse = 23
right_forward = PWMOutputDevice(23, frequency=100)
right_reverse = PWMOutputDevice(24, frequency=100)

# get the "drive" table from the networktables instance
drive_table = NetworkTables.getTable("drive")
# get the "right" entry from the networktables table
right_drive_table = drive_table.getEntry("right")
# get the "left" entry from the networktables table
left_drive_table = drive_table.getEntry("left")
# get the "stop" entry from the networktables table
stop_drive_table = drive_table.getEntry("stop")

#create an endless loop
while True:
    # check the right value
    # if it is negative then set right forward to be the absolute value of the right value and set the right reverse to be 0
    # if it is positive then set right reverse to be the absolute value of the right value and set the right forward to be 0
    # otherwise set both the right forward and right reverse to be 0
    if right_drive_table.value > 0:
        right_forward.value = abs(right_drive_table.value)
        right_reverse.value = 0
    elif right_drive_table.value < 0:
        right_forward.value = 0
        right_reverse.value = abs(right_drive_table.value)
    else:
        right_forward.value = 0
        right_reverse.value = 0

    # check the left value
    # if it is negative then set left forward to be the absolute value of the left value and set the left reverse to be 0
    # if it is positive then set left reverse to be the absolute value of the left value and set the left forward to be 0
    # otherwise set both the left forward and left reverse to be 0
    if left_drive_table.value > 0:
        left_forward.value = abs(left_drive_table.value)
        left_reverse.value = 0
    elif left_drive_table.value < 0:
        left_forward.value = 0
        left_reverse.value = abs(left_drive_table.value)
    else:
        left_forward.value = 0
        left_reverse.value = 0

    # check the stop value
    # if it is true then break out of the loop, which will result in the program exitng
    if stop_drive_table.value == True:
        sys.exit()

# notice the indentation above, this is important in the python language and replaces the need to use "{}" like you do in java