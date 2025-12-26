import pygame
from sys import exit

pygame.init()

gameWidth = 1000
gameHeight = 600
isPlaying = True

window = pygame.display.set_mode((gameWidth, gameHeight))
pygame.display.set_caption("game for jessica! :)")
clock = pygame.time.Clock()

icon = pygame.image.load('assets/heartLatte.png')
pygame.display.set_icon(icon)
pygame.font.Font("assets/pixelifySans.ttf", 50)

def draw():
    print("test")

while isPlaying:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    draw()
    pygame.display.update()
    clock.tick(60)