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
playRect = images['play1'].get_rect(center=(gameWidth//2, gameHeight//2 + 100))
playPressed = False

titleFont = pygame.font.Font("assets/pixelifySans.ttf", 70)
textFont = pygame.font.Font("assets/pixelifySans.ttf", 30)

creamColor = (255, 253, 208)

def startScreen():
    window.fill(creamColor)
    titleIcon = images['catLatte'].get_rect(center=(gameWidth//2, 120))
    window.blit(images['catLatte'], titleIcon)
    
    titleText = titleFont.render('Coffee Catcher!', True, (84, 26, 69))
    titleRect = titleText.get_rect(center=(gameWidth//2, 230))
    window.blit(titleText, titleRect)
    
    subtitleText = textFont.render('Merry Christmas, Jessica! :D', True, (84, 26, 69))
    subtitleRect = subtitleText.get_rect(center=(gameWidth//2, 290))
    window.blit(subtitleText, subtitleRect)

    currentButton = images['play2'] if playPressed else images['play1']
    window.blit(currentButton, playRect)

def draw():
    match gameState:
        case "start":
            startScreen()

while isPlaying:
    mousePos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if gameState == "start":
                if playRect.collidepoint(mousePos):
                    playPressed = True
        if event.type == pygame.MOUSEBUTTONUP:
            if gameState == "start" and playPressed:
                if playRect.collidepoint(mousePos):
                    playPressed = False
                    gameState = "play"
                    window.blit(images['play1'], playRect)

    draw()
    pygame.display.update()
    clock.tick(60)