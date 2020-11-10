
#Pygame Imports
import pygame, sys, time    #Imports Modules
from pygame.locals import *

#Robot kit imports
from networktables import NetworkTables
#General Imports
import threading
import logreceiver
import ctypes
import logging

import argparse

class RectItem():
    def __init__(self, color, x,y,width,height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def setText(self, t):
        self.text = t

    def draw(self,win,outline=None):
        #Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
            
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, 
                (self.x + (self.width/2 - text.get_width()/2),
                 self.y + (self.height/2 - text.get_height()/2)))
 
class Button(RectItem):


    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                #self.onPressed()
                return True
            
        return False
        


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
#if len(sys.argv) != 2:
#    print("Error: specify robot IP to connect; Bye!")
#    exit(0)

# Construct an argument parser
parser = argparse.ArgumentParser()
parser.add_argument("ip_addr", help="IP address of the server")
args = parser.parse_args()
ip = args.ip_addr
print(ip)
NetworkTables.initialize(ip)




pygame.init()#Initializes Pygame
pygame.joystick.init()
# Assume only 1 joystick for now
joystick = pygame.joystick.Joystick(0)
joystick.init()#Initializes Joystick

# Initialize Window
screen = pygame.display.set_mode((500, 600))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)

#pygame setup
descriptionText = RectItem((0,255,0), 0, 0, 500,40, "PiKitLib Driverstation")
enableButton = Button((0,255,0), 0,225,250,100, "Enable")
disableButton = Button((0,255,0), 250,225,250,100, "Disable")
autonButton = Button((0,255,0),     0,355,250,100, "Start Auton")
teleopButton = Button((0,255,0), 250,355,250,100, "Start Teleop")
pygame_buttons = [enableButton,disableButton, autonButton, teleopButton]

def redrawWindow():
    screen.fill((255,255,255))
    for bt in pygame_buttons:
        bt.draw(screen)
        
        

    descriptionText.draw(screen)

redrawWindow()
pygame.display.update()



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
    #print(axis_values)
    #print(joystick.get_button(0))
    for j in range(len(axis_values)):
        axis_values[j] = joystick.get_axis(j)
    
    #print(axis_values)

    xbc_nt.putBooleanArray("Buttons", buttons)
    xbc_nt.putNumberArray("Axis", list(axis_values))

    redrawWindow()
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                loopQuit = True
                quit()
        if event.type == pygame.QUIT:
                loopQuit = True
                quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if enableButton.isOver(pos) and disabled == True:
                print("Enabled")
                disabled = False
            elif disableButton.isOver(pos) and disabled == False:
                print("Disabled")
                disabled = True
            elif teleopButton.isOver(pos) and mode != "Teleop":
                mode = "Teleop"
                print("Starting Teleop")
            elif autonButton.isOver(pos) and mode != "Auton":
                print("Starting auton")
                mode = "Auton"

        if event.type == pygame.MOUSEMOTION:
            for b in pygame_buttons:
                if b.isOver(pos):
                    b.color = (0, 220, 0)
                else:
                    b.color = (0, 255, 0)

    mode_nt.putBoolean("Disabled", disabled)
    mode_nt.putString("Mode", mode)
    pygame.display.update()
    clock.tick(30)
    time.sleep(0.02)

def quit():
    mode_nt.putBoolean("Disabled", True)
    pygame.quit()
    sys.exit()

quit()