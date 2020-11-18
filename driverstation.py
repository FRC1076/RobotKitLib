
#Pygame Imports
import sys, time    #Imports Modules
import pygame

#Robot kit imports
from networktables import NetworkTables
#General Imports
import threading
import logreceiver
import ctypes
import logging

import argparse

import driverstationgui

EnableBTN = 0
DisableBTN = 1
AutonBTN = 2
TeleopBTN = 3


def quit():
    mode_nt.putBoolean("Disabled", True)
    pygame.quit()
    sys.exit()


# Construct an argument parser
parser = argparse.ArgumentParser()
parser.add_argument("ip_addr", help="IP address of the server")
args = parser.parse_args()
ip = args.ip_addr
print(ip)
NetworkTables.initialize(ip)


GUI = driverstationgui.DriverstationGUI()
GUI.setup() 

pygame.joystick.init()
# Assume only 1 joystick for now
joystick = pygame.joystick.Joystick(0)
joystick.init()#Initializes Joystick


# save reference to table for each xbox controller
xbc_nt = NetworkTables.getTable('DriverStation/XboxController0')
mode_nt = NetworkTables.getTable('RobotMode')
buttons = [False] * joystick.get_numbuttons()

lg = threading.Thread(target=logreceiver.main)
lg.daemon = True
lg.start()


axis_values = [0] * joystick.get_numaxes()
mode = ""
disabled = True




loopQuit = False
while loopQuit == False:

    """
    TODO: Check if values are different for windows/linux
    TODO: Update only when there is an update event

    Look at the documentation for NetworkTables for some ideas.
         https://robotpy.readthedocs.io/projects/pynetworktables/en/latest/examples.html
    """

    for i in range(len(buttons)):
        buttons[i] = bool(joystick.get_button(i))
    for j in range(len(axis_values)):
        axis_values[j] = joystick.get_axis(j)

    xbc_nt.putBooleanArray("Buttons", buttons)
    xbc_nt.putNumberArray("Axis", list(axis_values))
    

    btn = GUI.getButtonPressed
    if btn == EnableBTN and disabled == True:
        print("Enabled")
        disabled = False
    elif btn == DisableBTN and disabled == False:
        print("Disabled")
        disabled = True
    elif btn == TeleopBTN and mode != "Teleop":
        mode = "Teleop"
        print("Starting Teleop")      
    elif btn == AutonBTN and mode != "Auton":
        print("Starting auton")
        mode = "Auton"
        
    if GUI.getQuit():
        loopQuit = True
        quit()

    mode_nt.putBoolean("Disabled", disabled)
    mode_nt.putString("Mode", mode)
    
    GUI.update()


quit()