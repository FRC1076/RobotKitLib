import pygame, sys, time    #Imports Modules

EnableBTN = 0
DisableBTN = 1
AutonBTN = 2
TeleopBTN = 3

class RectItem():
    def __init__(self, color, x,y,width,height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.selected = False

    def isSelected(self):
        return self.selected

    def setText(self, t):
        self.text = t

    def select(self):
        self.selected = True
        self.color = (0, 180, 0)
   
    def unselect(self):
        self.selected = False
        self.color = (0, 255, 0)

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

class DriverstationGUI():

    def __init__(self):
        pygame.init()#Initializes Pygame
        

    def setup(self):
        # Initialize Window
        self.screen = pygame.display.set_mode((500, 600))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 20)

        #pygame setup
        self.descriptionText = RectItem((0,255,0), 0, 0, 500,40, "PiKitLib Driverstation")
        self.enableButton = Button((0,255,0), 0,225,250,100, "Enable")
        self.disableButton = Button((0,255,0), 250,225,250,100, "Disable")
        self.autonButton = Button((0,255,0),     0,355,250,100, "Start Auton")
        self.teleopButton = Button((0,255,0), 250,355,250,100, "Start Teleop")
        self.pygame_buttons = [self.enableButton,self.disableButton,
                               self.autonButton, self.teleopButton]

    def redrawWindow(self):
        self.screen.fill((255,255,255))
        for bt in self.pygame_buttons:
            bt.draw(self.screen)

        self.descriptionText.draw(self.screen)

    def update(self):
        self.redrawWindow()
        pygame.display.update()
        #self.clock.tick(30)
        time.sleep(0.02)

    def getCurrentEvents(self):
        return pygame.event.get()

    def getPos(self):
        return pygame.mouse.get_pos()

    def getButtonPressed(self):
        """
        Returns button pressed, None if not
        """
        pos = self.getPos()
        for event in self.getCurrentEvents():
            if event.type == pygame.MOUSEMOTION:
                for b in self.pygame_buttons:
                    if not b.selected:
                        if b.isOver(pos):
                            b.color = (0, 180, 0)
                        else:
                            b.color = (0, 250, 0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.enableButton.isOver(pos):
                    self.disableButton.unselect()
                    self.enableButton.select()
                    return EnableBTN
                elif self.disableButton.isOver(pos):
                    self.disableButton.select()
                    self.enableButton.unselect()
                    return DisableBTN
                elif self.teleopButton.isOver(pos):
                    self.teleopButton.select()
                    self.autonButton.unselect()
                    return TeleopBTN
                elif self.autonButton.isOver(pos):
                    self.teleopButton.unselect()
                    self.autonButton.select() 
                    return AutonBTN
        return None

    def getQuit(self):
        for event in self.getCurrentEvents():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return True
        return False
    

    