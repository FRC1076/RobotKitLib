
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
import os
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
    global hasCommunication
    hasCommunication = True

    global s
    s = socket.socket()

    
    sd = NetworkTables.getTable("Battery")
    sd.addEntryListener(valueChanged)

def valueChanged(table, key, value, isNew):
    """
    Check for new changes and use them
    """
    global updateFromRobot

    if(key == "Voltage"):
        updateFromRobot = True
        bV = str(value)[:4]
        GUI.setBatInfoText(bV)

        

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


updateFromRobot = False

hasCommunication = False
hasCode = False #TODO: make some way to check for this
hasJoysticks = False

global joystick
joystick = None

buttons = [False] * 11
axis_values = [0] * 6

def tryToSetupJoystick():
    global joystick, hasJoysticks, buttons, axis_values
    try:
        pygame.joystick.init()
        # Assume only 1 joystick for now
        
        joystick = pygame.joystick.Joystick(0)
        joystick.init()#Initializes Joystick
        buttons = [False] * joystick.get_numbuttons()
        axis_values = [0] * joystick.get_numaxes()
        hasJoysticks = True
        
    except pygame.error:
        hasJoysticks = False

def sendRobotCode(host):
    SEPARATOR = "/"
    BUFFER_SIZE = 4096 
    port = 5002

    global s, connected

    filename = "robot.py"
    try:
        filesize = os.path.getsize(filename)
    except FileNotFoundError:
        logging.critical("ERROR: " + filename + " not found!")
        return
    
    if not connected:
        print(f"[+] Connecting to {host}:{port}")
        s.connect((host, port))
        print("[+] Connected.")
        connected = True

    s.send(f"{filename}{SEPARATOR}{filesize}".encode())

    progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
    with open(filename, "rb") as f:
        for _ in progress:
            bytes_read = f.read(BUFFER_SIZE)
            if not bytes_read:
                break

            s.sendall(bytes_read)

            progress.update(len(bytes_read))

    s.close()


tryToSetupJoystick()


# save reference to table for each xbox controller
xbc_nt = NetworkTables.getTable('DriverStation/XboxController0')
mode_nt = NetworkTables.getTable('RobotMode')
status_nt = NetworkTables.getTable('Status')

#lg = threading.Thread(target=logreceiver.main)
#lg.daemon = True
#lg.start()


mode = ""
disabled = True
connected = False

connect()

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
    
    if status_nt.getBoolean(("Code"), False):
        hasCode = True


    if hasCommunication and hasJoysticks and hasCode:
        for i in range(len(buttons)):
            buttons[i] = bool(joystick.get_button(i))
        for j in range(len(axis_values)):
            axis_values[j] = joystick.get_axis(j)

        xbc_nt.putBooleanArray("Buttons", buttons)
        xbc_nt.putNumberArray("Axis", list(axis_values))

    
    if time.perf_counter() - b > 2.5:
        b = time.perf_counter()
        updateFromRobot = False
    #print(updateFromRobot)

    if time.perf_counter() - a > 3:
        a = time.perf_counter()
        if not updateFromRobot:
            hasCommunication = False
        else:
            hasCommunication = True
    
    
    


    #Update indicators
    
    

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
    elif btn["action"] == "Code":
        #if hasCommunication:
        sendRobotCode(NetworkTables.getRemoteAddress())
        #else:
        #    logging.warning("Cant send code, no connection!")
    
    
    if hasCommunication and hasCode:
        mode_nt.putBoolean("Disabled", disabled)
        mode_nt.putString("Mode", mode)

    GUI.update()


quit()
