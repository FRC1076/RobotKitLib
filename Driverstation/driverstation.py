# pylint: disable=no-member
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
import socket
import tqdm
import hashlib
import pathlib
import os
import argparse

import driverstationgui

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



s = ""
GUI = driverstationgui.DriverstationGUI()
GUI.setup() 



hasCommunication = False
hasCode = False #TODO: make some way to check for this
hasJoysticks = False

global joystick
joystick = None

buttons = [False] * 11
axis_values = [0] * 6

def tryToSetupJoystick():
    global joystick, hasJoysticks, buttons, axis_values, xbc_nt
    try:
        pygame.joystick.init()
        # Assume only 1 joystick for now
        
        joystick = pygame.joystick.Joystick(0)
        joystick.init()#Initializes Joystick
        buttons = [False] * joystick.get_numbuttons()
        axis_values = [0] * joystick.get_numaxes()
        hasJoysticks = True

        xbc_nt.putBooleanArray("Buttons", buttons)
        xbc_nt.putNumberArray("Axis", list(axis_values))
        
    except pygame.error:
        hasJoysticks = False



# save reference to table for each xbox controller
xbc_nt = NetworkTables.getTable('DriverStation/XboxController0')
mode_nt = NetworkTables.getTable('RobotMode')
status_nt = NetworkTables.getTable('Status')
batval_nt = NetworkTables.getTable('Battery')
tryToSetupJoystick()
lg = threading.Thread(target=logreceiver.main)
lg.daemon = True
lg.start()


mode = ""
disabled = True
connected = False
def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()
    
def getChecksumOfDir(path):
    checksums = []
    for filename in os.listdir(path):
        checksums.append(md5(path + filename))
    return checksums
#connect()

print("starting")
loopQuit = False

a = time.perf_counter()
b = time.perf_counter()
while loopQuit == False:

    """
    TODO: Check if values are different for windows/linux
    TODO: Update only when there is an update event

    Look at the documentation for NetworkTables for some ideas.
         https://robotpy.readthedocs.io/projects/pynetworktables/en/latest/examples.html
    """

    tryToSetupJoystick()


    remote_checksum =  status_nt.getStringArray("Checksum", [])
    local_path = os.fspath(pathlib.Path().absolute())
    local_checksum  =  getChecksumOfDir(os.fspath(pathlib.Path(__file__).parent.parent.absolute()) + "/RobotCode/") 
    
    rc = lc = ""
    for i in local_checksum: lc += i[:2]
    for i in remote_checksum: rc += i[:2]

    GUI.updateChecksum("l", lc)
    GUI.updateChecksum("r", rc)

    hasCode = status_nt.getBoolean(("Code"), False)


    if hasCommunication and hasJoysticks and hasCode:
        for i in range(len(buttons)):
            buttons[i] = bool(joystick.get_button(i))
        for j in range(len(axis_values)):
            axis_values[j] = joystick.get_axis(j)

        xbc_nt.putBooleanArray("Buttons", buttons)
        xbc_nt.putNumberArray("Axis", list(axis_values))

    
    hasCommunication = NetworkTables.getRemoteAddress() is not None
    


    #Update indicators
    

    if hasCommunication:
        bV = str(batval_nt.getValue("Voltage", "NO DATA"))[:4]
        GUI.setBatInfoText(bV)

    GUI.updateIndicator(0, hasCommunication)
    GUI.updateIndicator(1, hasCode)
    GUI.updateIndicator(2, hasJoysticks)
    
    


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
    #elif btn["action"] == "Code":
        #if hasCommunication:
    #    sendRobotCode(NetworkTables.getRemoteAddress())
        #else:
        #    logging.warning("Cant send code, no connection!")
    
    
    if hasCommunication and hasCode:
        mode_nt.putBoolean("Disabled", disabled)
        mode_nt.putString("Mode", mode)

    GUI.update()


quit()
