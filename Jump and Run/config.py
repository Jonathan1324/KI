import pygame
import components

HEIGHT = 720
WIDTH = 550
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

ground = components.Ground(WIDTH)
pipes = []