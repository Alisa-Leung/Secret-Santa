import pygame
import os
from sys import exit

pygame.init()

gameWidth = 1000
gameHeight = 600
isPlaying = True
gameState = "start"

window = pygame.display.set_mode((gameWidth, gameHeight))
pygame.display.set_caption("game for jessica! :)")
clock = pygame.time.Clock()

icon = pygame.image.load('assets/catLatte.png')
pygame.display.set_icon(icon)

def loadImages():
    images = {}
    for fileName in os.listdir("assets/"):
        if fileName.endswith('.png'):
            path = os.path.join("assets/", fileName)
            image = pygame.image.load(path).convert_alpha()
            key = os.path.splitext(fileName)[0]
            images[key] = image
    return images

images = loadImages()

titleFont = pygame.font.Font("assets/pixelifySans.ttf", 70)
textFont = pygame.font.Font("assets/pixelifySans.ttf", 30)

def draw():
    print(images)

while isPlaying:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    draw()
    pygame.display.update()
    clock.tick(60)