
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

def quit():
    mode_nt.putBoolean("Disabled", True)
    pygame.quit()
    sys.exit()

def connect():
        """
        Connect to robot NetworkTables server
        """
        NetworkTables.initialize()
        NetworkTables.addConnectionListener(connectionListener, immediateNotify=True)


def connectionListener(connected, info):
    """
    Setup the listener to detect any changes to the robotmode table
    """
    #print(info, "; Connected=%s" % connected)
    logging.info("%s; Connected=%s", info, connected)
    sd = NetworkTables.getTable("Battery")
    sd.addEntryListener(valueChanged)

def valueChanged(table, key, value, isNew):
    """
    Check for new changes and use them
    """
    #print("valueChanged: key: '%s'; value: %s; isNew: %s" % (key, value, isNew))
    if(key == "Voltage"):
        #print("Voltage: " + str(value))
        GUI.setBatInfoText(str(value)[:4])

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

#lg = threading.Thread(target=logreceiver.main)
#lg.daemon = True
#lg.start()


axis_values = [0] * joystick.get_numaxes()
mode = ""
disabled = True

connect()

print("starting")
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
    
    #TODO: Fix

    # {"action": "Enable", "value": False}
    # {"action": "Mode", "value": "Auton"}
    btn = GUI.getButtonPressed()

    if btn["action"] == "Enable":
        disabled = not btn["value"]
        print("Enabled" if not disabled else "Disabled")
    elif btn["action"] == "Mode":
        mode = btn["value"]
        print("Starting " + mode)
    elif btn["action"] == "Quit":
        loopQuit = True
    elif btn["action"] == "ESTOP":
        mode_nt.putString("ESTOP", True)
    
    

    mode_nt.putBoolean("Disabled", disabled)
    mode_nt.putString("Mode", mode)
    
    GUI.update()


quit()
