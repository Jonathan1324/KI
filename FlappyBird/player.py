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
            return pygame.Rect.colliderect(self.rect, p.topRect) or \
                   pygame.Rect.colliderect(self.rect, p.bottomRect)
        
    def update(self, ground):
        if not (self.groundCollision(ground) or self.pipeCollision()):
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

    def birdFlap(self):
        if not self.flap and not self.skyCollision():
            self.flap = True
            self.vel = -5
        if self.vel >= 3:
            self.flap = False

    @staticmethod
    def closestPipe():
        for p in config.pipes:
            if not p.passed:
                return p

    # AI

    def look(self):
        if config.pipes:

            # Line to top pipe
            self.vision[0] = max(0, self.rect.center[1] - self.closestPipe().topRect.bottom) / 500
            pygame.draw.line(config.WINDOW, self.color, self.rect.center,
                             (self.rect.center[0], config.pipes[0].topRect.bottom))

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
        if self.decision > 0.73:
            self.birdFlap()

    def calculateFitness(self):
        self.fitness = self.lifespan

    def clone(self):
        clone = Player()
        clone.fitness = self.fitness
        clone.brain = self.brain.clone()
        clone.brain.generateNet()
        return clone