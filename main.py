import pygame
from sys import exit

pygame.init()

gameWidth = 1000
gameHeight = 600

window = pygame.display.set_mode((gameWidth, gameHeight))
pygame.display.set_caption("game for jessica! :)")
clock = pygame.time.Clock()

plainLatte = pygame.image.load('assets/plainLatte.png')
pygame.display.set_icon(plainLatte)

def draw():
    window.blit(plainLatte, (0, 0))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    draw()
    pygame.display.update()
    clock.tick(60)