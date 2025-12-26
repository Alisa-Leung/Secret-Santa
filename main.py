import pygame
import os
import random
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

bgY1 = 0
bgY2 = -gameHeight

def scrollBackground():
    bgSpeed = 2
    global bgY1, bgY2

    bg = pygame.transform.scale(images['background'], (gameWidth, gameHeight))
    window.blit(bg, (0,bgY1))
    window.blit(bg, (0,bgY2))
    
    bgY1 += bgSpeed
    bgY2 += bgSpeed
    
    if bgY1 >= gameHeight:
        bgY1 = -gameHeight
    if bgY2 >= gameHeight:
        bgY2 = -gameHeight

def startScreen():
    scrollBackground()

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

def introScreen():
    window.fill(creamColor)
    introLines = [
        "Welcome to Coffee Catcher!",
        "Catch falling coffee beans and creamer.",
        "Be careful of flying plushies!",
        "Make the perfect latte!",
        "Use the left and right arrow keys to move.",
        "Good luck, and have fun!",
        "",
        "Click anywhere to begin!"
    ]

    for i, line in enumerate(introLines):
        introText = textFont.render(line, True, (84, 26, 69))
        introRect = introText.get_rect(center=(gameWidth//2, 100 + i * 50))
        window.blit(introText, introRect)

cupX = gameWidth // 2

fallingObjects = []
spawnTimer = 0
spawnDelay = 60
score = 0

objectTypes = {
    'bean': {'image': 'beans', 'points': 10, 'speed': 5},
    'creamer': {'image': 'creamer', 'points': 15, 'speed': 5},
    'chiikawa': {'image': 'chiikawa', 'points': -20, 'speed': 5},
    'kirby': {'image': 'kirby', 'points': -15, 'speed': 5}
}

class FallingObject:
    def __init__(self, x, y, objType):
        self.x = x
        self.y = y
        self.type = objType
        self.image = images[objectTypes[objType]['image']]
        self.points = objectTypes[objType]['points']
        self.speed = objectTypes[objType]['speed']

    def update(self):
        self.y += self.speed

    def isOffScreen(self):
        self.y += self.speed
    
    def getRect(self):
        return pygame.Rect(self.x - 25, self.y - 25, 50, 50)

def playScreen():
    global cupX, spawnTimer, fallingObjects, score

    scrollBackground()
    scoreText = textFont.render(f'Score: {score}', True, (84, 26, 69))
    scoreRect = scoreText.get_rect(topleft=(10, 10))
    window.blit(scoreText, scoreRect)

    cup = images['latte7'].get_rect(center=(cupX, gameHeight - 100))
    window.blit(images['latte7'], cup)

    spawnTimer += 1
    if spawnTimer >= spawnDelay:
        spawnTimer = 0
        randomX = random.randint(50, gameWidth - 50)
        randomType = random.choice(['bean', 'bean', 'bean', 'creamer', 'creamer', 'chiikawa', 'kirby'])
        fallingObjects.append(FallingObject(randomX, -50, randomType))

    for obj in fallingObjects[:]:
        obj.update()
        objRect = obj.getRect()
        if cup.colliderect(objRect):
            score += obj.points
            fallingObjects.remove(obj)
            continue
        if obj.isOffScreen():
            fallingObjects.remove(obj)
            continue
        objImage = images[objectTypes[obj.type]['image']]
        window.blit(objImage, (obj.x - 25, obj.y - 25))

def draw():
    match gameState:
        case "start":
            startScreen()
        case "intro":
            introScreen()
        case "play":
            playScreen()

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
            if gameState == "intro":
                gameState = "play"
        if event.type == pygame.MOUSEBUTTONUP:
            if gameState == "start" and playPressed:
                if playRect.collidepoint(mousePos):
                    playPressed = False
                    gameState = "intro"
                    window.blit(images['play1'], playRect)
    keys = pygame.key.get_pressed()
    if gameState == "play":
        if keys[pygame.K_LEFT]:
                cupX -= 5
        if keys[pygame.K_RIGHT]:
                cupX += 5
        if cupX < 50:
            cupX = 50
        if cupX > gameWidth - 50:
            cupX = gameWidth - 50

    draw()
    pygame.display.update()
    clock.tick(60)