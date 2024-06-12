import pygame
import random

class Ground:
    groundLevel = 500

    def __init__(self, winWidth):
        self.x, self.y = 0, Ground.groundLevel
        self.rect = pygame.Rect(self.x, self.y, winWidth, 5)
    
    def draw(self, window):
        pygame.draw.rect(window, (255, 255, 255), self.rect)

class Pipes:
    width = 15
    opening = 100

    def __init__(self, winWidth):
        self.canLandOn = True
        self.x = winWidth
        self.bottomHeight = random.randint(15, 30)
        self.bottomRect = pygame.Rect(0, 0, 0, 0)
        self.passed = False
        self.offScreen = False

    def draw(self, window):
        self.bottomRect = pygame.Rect(self.x, Ground.groundLevel - self.bottomHeight, self.width, self.bottomHeight)

        pygame.draw.rect(window, (255, 255, 255), self.bottomRect)

    def update(self):
        self.x -= 2
        if self.x + Pipes.width <= 50:
            self.passed = True
        if self.x <= -self.width:
            self.offScreen = True

class highPipes:
    width = 15
    opening = 100

    def __init__(self, winWidth):
        self.canLandOn = True
        self.x = winWidth
        self.bottomHeight = random.randint(30, 70)
        self.bottomRect = pygame.Rect(0, 0, 0, 0)
        self.passed = False
        self.offScreen = False

    def draw(self, window):
        self.bottomRect = pygame.Rect(self.x, Ground.groundLevel - self.bottomHeight, self.width, self.bottomHeight)

        pygame.draw.rect(window, (255, 255, 255), self.bottomRect)

    def update(self):
        self.x -= 2
        if self.x + Pipes.width <= 50:
            self.passed = True
        if self.x <= -self.width:
            self.offScreen = True

class Spike:
    width = 15
    opening = 100

    def __init__(self, winWidth):
        self.canLandOn = False
        self.x = winWidth
        self.bottomHeight = random.randint(10, 20)
        self.bottomRect = pygame.Rect(0, 0, 0, 0)
        self.passed = False
        self.offScreen = False

    def draw(self, window):
        self.bottomRect = pygame.Rect(self.x, Ground.groundLevel - self.bottomHeight, self.width, self.bottomHeight)

        pygame.draw.rect(window, (255, 0, 0), self.bottomRect)

    def update(self):
        self.x -= 2
        if self.x + Pipes.width <= 50:
            self.passed = True
        if self.x <= -self.width:
            self.offScreen = True