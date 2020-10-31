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
Initially the AButton is up
Probably we need an object that contains all of the state
for the joystick?
"""
# A, B, X, Y, L bumpter, R bumber, back, start, big shinny button
buttons = [0,0,0,0,0,0,0,0]

# LHand Y, LHand X, L trigger, RHand X, RHand Y, R trigger
axis_values = [0,0,0,0,0,0]

#  AButton is button[0]
loopQuit = False
while loopQuit == False:

    """
    First, let's see what we need to do about the AButton
    Let's just read the button from the controller and publish
    the state in NetworkTables
    I think, instead, we could store all of the buttons in a boolean array
    e.g. getBooleanArray().   That would takes less code. Keep in mind that pygame library might
    return different orders for the button array, so we might need
    to permute them based Window/Mac/Linux.

    Look at the documentation for NetworkTables for some ideas.
         https://robotpy.readthedocs.io/projects/pynetworktables/en/latest/examples.html
    """

    for i in range(len(buttons)):
        buttons[i] = joystick.get_button(i)
        

    for j in range(len(axis_values)):
        axis_values[j] = joystick.get_axis(j)
    
    xbc_nt.putNumberArray("Buttons", buttons)
    xbc_nt.putNumberArray("Axis", axis_values)

    print(buttons)

    """
    AButton = joystick.get_button(0)           #  get button from joystick
    xbc_nt.putBoolean('Button0', AButton)      #  publish to NetworkTables
    BButton = joystick.get_button(1)
    xbc_nt.putBoolean('Button1', BButton)
    #
    # We can likely be more efficient by only updating the button
    # state when there is a button event.   Until things work at all,
    # it is not necessary.    But we should be doing it.
    #"""
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                loopQuit = True

        print("Event type:", event.type) 
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
    
    time.sleep(0.5)

pygame.quit()
sys.exit()
