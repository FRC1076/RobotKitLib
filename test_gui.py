import pygame
 
pygame.init()
screen = pygame.display.set_mode((500, 600))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)


class Rect():
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
 
class Button(Rect):


    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                #self.onPressed()
                return True
            
        return False
        



    






descriptionText = Rect((0,255,0), 0, 0, 500,40, "PiKitLib Driverstation")
enableButton = Button((0,255,0), 0,225,250,100, "Enable")
disableButton = Button((0,255,0), 250,225,250,100, "Disable")
autonButton = Button((0,255,0),     0,355,250,100, "Start Auton")
teleopButton = Button((0,255,0), 250,355,250,100, "Start Teleop")

buttons = [enableButton,disableButton, autonButton, teleopButton]




def redrawWindow():
    screen.fill((255,255,255))
    for b in buttons:
        b.draw(screen)

    descriptionText.draw(screen)
        


 
loop = 1
while loop:
    redrawWindow()
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            loop = 0
        if event.type == pygame.MOUSEBUTTONDOWN:
            if enableButton.isOver(pos):
                print("Enabled")

        if event.type == pygame.MOUSEMOTION:
            for b in buttons:
                if b.isOver(pos):
                    b.color = (0, 220, 0)
                else:
                    b.color = (0, 255, 0)

    
    pygame.display.update()
    clock.tick(30)
 
pygame.quit()