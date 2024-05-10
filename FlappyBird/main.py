import pygame
from sys import exit
import config
import components
import population

pygame.init()

pygame.display.set_caption("AI plays Flappy Bird")

clock = pygame.time.Clock()
population = population.Population(100)

FONT = pygame.font.Font('freesansbold.ttf', 32)

TICK_SPEED_OPTIONS = [1, 5, 15, 30, 60, 120, 240, 500, 1000, 2500, 5000, 10000, 25000, 50000, 100000, 250000, 500000, 1000000]
SIZES = [1, 10, 100, 500, 1000, 2500, 5000, 10000, 25000, 50000, 100000, 250000, 500000, 1000000, 2500000, 5000000, 10000000]

def generatePipes():
    config.pipes.append(components.Pipes(config.WIDTH))

def main():
    pipesSpawnTime = 10
    tickSpeedKey = 4
    sizeKey = 2

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

        config.WINDOW.fill((0, 0, 0))

        # Draw Ground
        config.ground.draw(config.WINDOW)

        # Spawn Pipes
        if pipesSpawnTime <= 0:
            generatePipes()
            pipesSpawnTime = 200
        pipesSpawnTime -= 1

        for p in config.pipes:
            p.draw(config.WINDOW)
            p.update()
            if p.offScreen:
                config.pipes.remove(p)

        # Draw Player
        if not population.extinct():
            population.updateLivePlayers()
        else:
            config.pipes.clear()
            population.naturalSelection()

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