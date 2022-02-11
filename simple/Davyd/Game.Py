import pygame


class TRect():
    def __init__(self, aWidth: int = 0, aHeight: int = 0, aColor: tuple = (255,10,10)):
        self.Width = aWidth
        self.Height = aHeight
        self.Color = aColor
        self.Speed = 10
        self.X = 0
        self.Y = 0
        self.ScreenWidth, self.ScreenHeight = pygame.display.get_window_size()
        self.ScreenSurf = pygame.display.get_surface()

    def SetCenter(self):
        self.X = (self.ScreenHeight - self.Width) / 2
        self.Y = (self.ScreenHeight - self.Height) / 2

    def SetPos(self, aX: int, aY: int):
            if (aX > 0) and (aX < self.ScreenWidth - self.Width):
                self.X = aX

            if (aY > 0) and (aY < self.ScreenHeight - self.Height):
                self.Y = aY

    def OnKey(self, aKeys):
        if (aKeys[pygame.K_LEFT]) and (self.X > 0):
            self.SetPos(self.X - self.Speed, self.Y)
        elif (aKeys[pygame.K_RIGHT]) and (self.X < self.ScreenWidth - self.Width):
            self.SetPos(self.X + self.Speed, self.Y)

    def Draw(self):
        pygame.draw.rect(self.ScreenSurf, self.Color, (self.X, self.Y, self.Width, self.Height)) 


def Run():
    ScreenColor = (200,200,20)
    ScreenWidth = 1024
    ScreenHeight = 768

    pygame.init()
    pygame.display.set_caption('Snake')
    Screen = pygame.display.set_mode([ScreenWidth, ScreenHeight])

    BallWidth = 40
    BallHeight = 20
    BallX = (ScreenWidth - BallWidth) / 2
    BallY = (ScreenHeight - BallHeight) / 2
    BallSpeed = 5

    Rect1 = TRect(20, 20, (255,10,10))
    Rect1.Speed = 6
    Rect1.SetCenter()
    Rect1.Y += 50

    Screen.fill(ScreenColor)
    pygame.display.update()

    IsRun = True
    while (IsRun):
        pygame.time.delay(10)
        Screen.fill(ScreenColor)

        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                IsRun = False
            #if (event.type in [pygame.KEYDOWN, pygame.KEYUP]):

        Keys = pygame.key.get_pressed()
        if (Keys[pygame.K_ESCAPE]):
            IsRun = False
        elif (Keys[pygame.K_LEFT]) and (BallX > 0):
            BallX -= BallSpeed
        elif (Keys[pygame.K_RIGHT]) and (BallX < ScreenWidth - BallWidth):
            BallX += BallSpeed

        pygame.draw.rect(Screen, (255, 0, 0), (BallX, BallY, BallWidth, BallHeight))

        Rect1.OnKey(Keys)
        Rect1.Draw()

        pygame.display.update()

    pygame.quit()


Run()
