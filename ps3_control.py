#!/usr/bin/env python3

import pygame, sys
from time import sleep
from networktables import NetworkTables

##########
# CONIFG #
##########

# networktables server
nt_server = "10.0.0.29"

# polling rate (num of inputs written to networktable per second)
polling_rate = 100

################################################################################

""" INIT NETWORK TABLES AND PYGAME """

#  initialize networktables w/ drive table
NetworkTables.initialize(server=nt_server)
drive_table = NetworkTables.getTable("drive")

# create network table entries
right_drive_table = drive_table.getEntry("right")
left_drive_table = drive_table.getEntry("left")
stop_drive_table = drive_table.getEntry("stop")

# set default values
right_drive_table.setValue(0)
left_drive_table.setValue(0)
stop_drive_table.setValue(False)

# setup the pygame window
pygame.init()

""" PROCESS JOYSTICKS """

# display number of joysticks
joystick_count = pygame.joystick.get_count()
print ("Joysticks: " + str(joystick_count))

# if no joysticks found, exit; else initialize first joystick
if joystick_count == 0:
    print ("ERROR: No joysticks found.")
    pygame.quit()
    sys.exit()
else:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print("STATUS: Jotstick Initialized.")

# find number of axes and buttons; display
axes = joystick.get_numaxes()
buttons = joystick.get_numbuttons()

print("---")
print ("Axes: " + str(axes))
print ("Buttons: " + str(buttons))
print("---")

""" PROCESS INPUTS """

def getAxis(number):
    # when nothing is moved on an axis, the VALUE IS NOT EXACTLY ZERO
    # so this is used not "if joystick value not zero"
    if joystick.get_axis(number) < -0.1 or joystick.get_axis(number) > 0.1:
      # value between 1.0 and -1.0
      print ("Axis value is %s" %(joystick.get_axis(number)))
      print ("Axis ID is %s" %(number))

    if (number == 1):
      if joystick.get_axis(number) < -0.1 or joystick.get_axis(number) > 0.1:
        left_drive_table.setValue(joystick.get_axis(number))
      else:
        left_drive_table.setValue(0)

    if (number == 3):
      if joystick.get_axis(number) < -0.1 or joystick.get_axis(number) > 0.1:
        right_drive_table.setValue(joystick.get_axis(number))
      else:
        right_drive_table.setValue(0)

def getButton(number):
    # returns 1 or 0 - pressed or not
    if joystick.get_button(number):
      # just prints id of button
      print ("Button ID is %s" %(number))

      # stop = true when circle pressed
      if (number == 13):
        stop_drive_table.setBoolean("true")

################################################################################

""" MAIN LOOP """

# set polling rate
polling_rate = 1 / polling_rate

# main program loop
while True:
    for event in pygame.event.get():
      # loop through events, if window shut down, quit program
      if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
    if axes != 0:
      for i in range(axes):
        getAxis(i)
    if buttons != 0:
      for i in range(buttons):
        getButton(i)
    sleep(polling_rate)