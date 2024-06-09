import random
import pygame
import config
import brain

class Player:
    def __init__(self):
        # Bird
        self.x, self.y = 50, 200
        self.rect = pygame.Rect(self.x, self.y, 20, 20)
        self.color = random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)
        self.vel = 0
        self.flap = False
        self.alive = True
        self.lifespan = 0

        # AI
        self.decision = None
        self.vision = [0.5, 1, 0.5]
        self.fitness = 0
        self.inputs = 3
        self.brain = brain.Brain(self.inputs)
        self.brain.generateNet()

    def draw(self, window):
        pygame.draw.rect(window, self.color, self.rect)

    def groundCollision(self, ground):
        return pygame.Rect.colliderect(self.rect, ground)
    
    def skyCollision(self):
        return bool(self.rect.y < 30)
    
    def pipeCollision(self):
        for p in config.pipes:
            r1 = pygame.Rect.colliderect(self.rect, p.bottomRect)

            if not p.canLandOn and r1 == True:
                return True
            
            self.rect.y -= 5

            r = pygame.Rect.colliderect(self.rect, p.bottomRect)
            
            self.rect.y += 5

            if r == False and r1 == True:
                while pygame.Rect.colliderect(self.rect, p.bottomRect):
                    self.rect.y -= 1
                self.vel = 0
                return False
            elif r1 == False:
                return False
            
            return True
        
    def update(self, ground):
        if self.pipeCollision():
            self.alive = False
            self.flap = False
            self.vel = 0
            return
        
        if not (self.groundCollision(ground)):
            # Gravity
            self.vel += 0.25
            self.rect.y += self.vel
            if self.vel > 5:
                self.vel = 5

            self.lifespan += 1
        else:
            self.alive = False
            self.flap = False
            self.vel = 0

        if self.skyCollision():
            self.alive = False

        if self.groundCollision(ground):
            self.flap = False
            self.rect.y = 480
        else:
            self.flap = True

    def birdFlap(self):
        if not self.flap and not self.skyCollision():
            self.flap = True
            self.vel = -6

    def goUp(self):
        self.rect.y += 2

    def goDown(self):
        self.rect.y -= 2

    @staticmethod
    def closestPipe():
        for p in config.pipes:
            if not p.passed:
                return p
            
        return None

    # AI

    def look(self):
        if config.pipes and self.closestPipe() != None:

            # Line to top pipe
            self.vision[0] = max(0, self.rect.center[1] - 0) / 500
            pygame.draw.line(config.WINDOW, self.color, self.rect.center,
                             (self.rect.center[0], 0))

            # Line to mid pipe
            self.vision[1] = max(0, self.closestPipe().x - self.rect.center[0]) / 500
            pygame.draw.line(config.WINDOW, self.color, self.rect.center,
                             (config.pipes[0].x, self.rect.center[1]))

            # Line to bottom pipe
            self.vision[2] = max(0, self.closestPipe().bottomRect.top - self.rect.center[1]) / 500
            pygame.draw.line(config.WINDOW, self.color, self.rect.center,
                             (self.rect.center[0], config.pipes[0].bottomRect.top))

    def think(self):
        self.decision = self.brain.feedForward(self.vision)
        if self.decision > 0.73 and not self.skyCollision():
            self.birdFlap()
            #self.goUp()
        #else:
            #self.goDown()

    def calculateFitness(self):
        self.fitness = self.lifespan

    def clone(self):
        clone = Player()
        clone.fitness = self.fitness
        clone.brain = self.brain.clone()
        clone.brain.generateNet()
        return clone