from networktables import NetworkTables
import pygame, sys, time    #Imports Modules
from pygame.locals import *

def joystick_stats(joystick):
    """
    Return the number of joysticks and
    a general stats descriptor in tuple form
    """
    nsticks = pygame.joystick.get_count()
    naxes = joystick.get_numaxes()
    nbuttons = joystick.get_numbuttons()

    report = "{ sticks : {}, axes : {}, nbuttons : {} }".format(nsticks, naxes, nbuttons)
    return nsticks, report

# parse command line argument
if len(sys.argv) != 2:
    print("Error: specify robot IP to connect; Bye!")
    exit(0)

# assume the first arg is the robot IP address
ip = sys.argv[1]
NetworkTables.initialize(ip)

pygame.init()#Initializes Pygame
pygame.joystick.init()
# Assume only 1 joystick for now
joystick = pygame.joystick.Joystick(0)
joystick.init()#Initializes Joystick

# save reference to table for each xbox controller
xbc_nt = NetworkTables.getTable('DriverStation/XboxController0')


"""
XBox Controller Linux Values:

Buttons: 0-10
A, B, X, Y, L bumpter, R bumber, back, start, big shinny button, L stick button, R stick button


LHand Y, LHand X, L trigger, RHand X, RHand Y, R trigger
"""


buttons = [False] * joystick.get_numbuttons()

#
axis_values = [0] * joystick.get_numaxes()

#  AButton is button[0]
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
    print(axis_values)
    #print(joystick.get_button(0))
    for j in range(len(axis_values)):
        axis_values[j] = joystick.get_axis(j)
    
    xbc_nt.putBooleanArray("Buttons", buttons)
    xbc_nt.putNumberArray("Axis", list(axis_values))
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                loopQuit = True

        #print("Event type:", event.type) 
        # Returns Joystick Button Motion
        if event.type == pygame.JOYBUTTONDOWN:
            print("joy button down")
        if event.type == pygame.JOYBUTTONUP:
            print("joy button up")
        if event.type == pygame.JOYBALLMOTION:
            print("joy ball motion")
        # axis motion is movement of controller
        # dominates events when used
        if event.type == pygame.JOYAXISMOTION:
            pass
    #print(buttons)
    
    time.sleep(0.02)

pygame.quit()
sys.exit()
