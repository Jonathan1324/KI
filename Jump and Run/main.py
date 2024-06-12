import pygame
from sys import exit
import config
import components
import population
import player
import random

pygame.init()

pygame.display.set_caption("AI plays Flappy Bird")

clock = pygame.time.Clock()
population = population.Population(100)

FONT = pygame.font.Font('freesansbold.ttf', 32)

TICK_SPEED_OPTIONS = [1, 5, 15, 30, 60, 120, 240, 500, 1000, 2500, 5000, 10000, 25000, 50000, 100000, 250000, 500000, 1000000]
SIZES = [1, 10, 100, 500, 1000, 2500, 5000, 10000, 25000, 50000, 100000, 250000, 500000, 1000000, 2500000, 5000000, 10000000]

generatedPipe = True

def generatePipes(red):
    global generatedPipe

    if random.randint(0, 15) == 0 and generatedPipe:
        generatedPipe = False
        return 0
    
    number = random.randint(1, 100)
    
    width = 0

    if number <= 50:
        width = random.randint(10, 50)
        newPipe = components.Pipes(config.WIDTH)
        newPipe.width = width
        config.pipes.append(newPipe)
        generatedPipe = True

    elif number <= 75:
        width = random.randint(100, 150)
        newPipe = components.highPipes(config.WIDTH)
        newPipe.width = width
        config.pipes.append(newPipe)
        generatedPipe = True

    elif number <= 100 and red:
        width = random.randint(20, 30)
        newPipe = components.Spike(config.WIDTH)
        newPipe.width = width
        config.pipes.append(newPipe)
        generatedPipe = True

    return width

def main():
    global floorExtra
    global extraEnd

    pipesSpawnTime = 5
    tickSpeedKey = 4
    sizeKey = 2

    controlPlayer = player.Player()
    controlPlayer.ai = False
    controlPlayer.x = 75
    controlPlayer.rect = pygame.Rect(controlPlayer.x, controlPlayer.y, 20, 20)

    mouseDown = False

    while True:
        population.size = SIZES[sizeKey]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    tickSpeedKey -= 1
                    if tickSpeedKey < 0:
                        tickSpeedKey = 0
                if event.key == pygame.K_RIGHT:
                    tickSpeedKey += 1
                    if tickSpeedKey >= len(TICK_SPEED_OPTIONS):
                        tickSpeedKey = len(TICK_SPEED_OPTIONS) - 1
                if event.key == pygame.K_DOWN:
                    sizeKey -= 1
                    if sizeKey < 0:
                        sizeKey = 0
                if event.key == pygame.K_UP:
                    sizeKey += 1
                    if sizeKey >= len(SIZES):
                        sizeKey = len(SIZES) - 1
                
                if event.key == pygame.K_r:
                    population.killAll()

            elif event.type == 1025:
                mouseDown = True
            elif event.type == 1026:
                mouseDown = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] or mouseDown:
                controlPlayer.birdFlap()

        config.WINDOW.fill((0, 0, 0))

        # Draw Ground
        config.ground.draw(config.WINDOW)

        # Spawn Pipes
        if pipesSpawnTime <= 0:
            if random.randint(0, 10) < 5:
                pipesSpawnTime = generatePipes(False) + random.randint(10, 50)
            else:
                pipesSpawnTime = generatePipes(True) + random.randint(100, 200)
        pipesSpawnTime -= 1

        for p in config.pipes:
            p.draw(config.WINDOW)
            p.update()
            if p.offScreen:
                config.pipes.remove(p)

        # Draw Player
        if not population.extinct() or controlPlayer.alive:
            population.updateLivePlayers()
        else:
            config.pipes.clear()
            population.naturalSelection()
            controlPlayer.alive = True

        if controlPlayer.alive:
                controlPlayer.draw(config.WINDOW)
                controlPlayer.update(config.ground)

        # Show Text
        text = FONT.render('Generation: ' + str(population.generation), True, (255, 255, 255))
        textRect = text.get_rect()
        textRect.center = (text.get_width() / 2, 510 + text.get_height() / 2)

        text2 = FONT.render('FPS: ' + str(round(clock.get_fps(), 2)), True, (255, 255, 255))
        text2Rect = text2.get_rect()
        text2Rect.center = (text2.get_width() / 2, 510 + text.get_height() + text2.get_height() / 2)

        text3 = FONT.render('SPEED: ' + str(TICK_SPEED_OPTIONS[tickSpeedKey]), True, (255, 255, 255))
        text3Rect = text3.get_rect()
        text3Rect.center = (text3.get_width() / 2, 510 + text.get_height() + text2.get_height() + text3.get_height() / 2)

        text4 = FONT.render('POPULATION SIZE: ' + str(SIZES[sizeKey]), True, (255, 255, 255))
        text4Rect = text4.get_rect()
        text4Rect.center = (text4.get_width() / 2, 510 + text.get_height() + text2.get_height() + text3.get_height() + text4.get_height() / 2)

        text5 = FONT.render('Players: ' + str(population.playersAlive), True, (255, 255, 255))
        text5Rect = text5.get_rect()
        text5Rect.center = (text5.get_width() / 2, 510 + text.get_height() + text2.get_height() + text3.get_height() + text4.get_height() + text5.get_height() / 2)

        config.WINDOW.blit(text, textRect)
        config.WINDOW.blit(text2, text2Rect)
        config.WINDOW.blit(text3, text3Rect)
        config.WINDOW.blit(text4, text4Rect)
        config.WINDOW.blit(text5, text5Rect)


        clock.tick(TICK_SPEED_OPTIONS[tickSpeedKey])
        pygame.display.flip()

main()