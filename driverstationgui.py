import pygame, sys, time    #Imports Modules

EnableBTN = 0
DisableBTN = 1
AutonBTN = 2
TeleopBTN = 3
PracticeBTN = 4
TestBTN = 5
QuitBTN = 6

class RectItem():
    def __init__(self, color, x,y,width,height,  text='', fontSize=40):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.selected = False
        self.fontSize = fontSize
        

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
            font = pygame.font.SysFont('comicsans', self.fontSize)
            text = font.render(self.text, 1, (0,0,0))
            # To center the text, add back in
            # + (self.width/2 - text.get_width()/2)
            win.blit(text, 
                (self.x ,
                 self.y + (self.height/2 - text.get_height()/2)))

    
 
class Button(RectItem):

    def __init__(self, color, x,y,width,height, text, fontSize=40, rValue=None):
        RectItem.__init__(self,color, x,y,width,height, text, fontSize)
        self.rValue = rValue
        

    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                #self.onPressed()
                return True
            
        return False

    def returnValue(self):
        return self.rValue

class DriverstationGUI():

    def __init__(self):
        pygame.init()#Initializes Pygame
        

    def setup(self):
        # Initialize Window
        self.screen = pygame.display.set_mode((500, 320))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 20)
        # lX,lY = location x, y
        # sX,sY = size x, y  
        # pygame setup                             lX  lY  sX   sY
        self.descriptionText = RectItem((0,255,0),  0,  0, 500,  40, "PiKitLib Driverstation", 50)
        self.batteryText     = RectItem((0,255,0),300, 90, 100,  30, "Voltage:", 20)
        self.batteryVal      = RectItem((0,255,0),300,110, 100,  50, "NO DATA", 30)
        self.enableButton    = Button((0,255,0),   50,220, 100,  90, "Enable",  rValue=EnableBTN)
        self.disableButton   = Button((0,255,0),  160,220, 100,  90, "Disable", rValue=DisableBTN)
        self.teleopButton    = Button((0,255,0),   50, 50, 210,  30, "TeleOperated", 30, TeleopBTN)
        self.autonButton     = Button((0,255,0),   50, 90, 210,  30, "Autonomous", 30, AutonBTN)
        self.practiceButton  = Button((0,255,0),   50, 130, 210,  30, "Practice (TODO)", 30, PracticeBTN)
        self.testButton      = Button((0,255,0),   50, 170, 210,  30, "Test     (TODO)", 30, TestBTN)
        self.control_buttons = [self.testButton,self.practiceButton,
                                self.autonButton,self.teleopButton]
        self.enable_buttons = [self.enableButton,self.disableButton]
        self.pygame_buttons  = self.enable_buttons + self.control_buttons
        self.exclusive_buttons = [self.enable_buttons, self.control_buttons]
        self.texts = [self.descriptionText, self.batteryVal, self.batteryText]
    


    def redrawWindow(self):
        self.screen.fill((255,255,255))
        for bt in self.pygame_buttons:
            bt.draw(self.screen, 1)
        for t in self.texts:
            t.draw(self.screen)
        #self.descriptionText.draw(self.screen)

    def update(self):
        self.redrawWindow()
        pygame.display.update()
        #self.clock.tick(30)
        #time.sleep(0.02)

    def setBatInfoText(self, txt: str):
        self.batteryVal.setText(txt)

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
                for btnSet in self.exclusive_buttons:
                    for btn in btnSet:
                        if btn.isOver(pos) and not btn.isSelected():
                            for jbtn in btnSet:
                                jbtn.unselect()
                            btn.select()
                            return btn.returnValue()
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                return QuitBTN   
        return None

    

    