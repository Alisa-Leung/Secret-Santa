import pygame
import os
import random
from sys import exit
import asyncio

pygame.init()

gameWidth = 1000
gameHeight = 600
isPlaying = True
gameState = "start"

window = pygame.display.set_mode((gameWidth, gameHeight))
pygame.display.set_caption("Coffee Catcher")
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
winLatte = None

objectTypes = {
    'bean': {'image': 'beans', 'points': 10, 'speed': 5, 'size': 80},
    'creamer': {'image': 'creamer', 'points': 15, 'speed': 5, 'size': 70},
    'chiikawa': {'image': 'chiikawa', 'points': -20, 'speed': 5, 'size': 90},
    'kirby': {'image': 'kirby', 'points': -15, 'speed': 5, 'size': 85}
}

class FallingObject:
    def __init__(self, x, y, objType):
        self.x = x
        self.y = y
        self.type = objType
        self.image = images[objectTypes[objType]['image']]
        self.points = objectTypes[objType]['points']
        self.speed = objectTypes[objType]['speed']
        self.size = objectTypes[objType]['size']

    def update(self):
        self.y += self.speed

    def isOffScreen(self):
        return self.y > gameHeight
    
    def getRect(self):
        halfSize = self.size // 2
        return pygame.Rect(self.x - halfSize, self.y - halfSize, self.size, self.size)

def playScreen():
    global cupX, spawnTimer, fallingObjects, score, gameState, winLatte

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
        objImage = pygame.transform.scale(obj.image, (obj.size, obj.size))
        halfSize = obj.size // 2
        window.blit(objImage, (obj.x - halfSize, obj.y - halfSize))
    
    if score >= 100:
        winLatte = random.choice(['catLatte', 'heartLatte', 'tulipLatte'])
        gameState = "win"

def winScreen():
    window.fill(creamColor)
    
    if winLatte and winLatte in images:
        latteImage = pygame.transform.scale(images[winLatte], (200, 200))
        latteRect = latteImage.get_rect(center=(gameWidth//2, 200))
        window.blit(latteImage, latteRect)
    
    winText = titleFont.render('Perfect Latte!', True, (84, 26, 69))
    winRect = winText.get_rect(center=(gameWidth//2, 380))
    window.blit(winText, winRect)
    
    finalScoreText = textFont.render(f'Final Score: {score}', True, (84, 26, 69))
    finalScoreRect = finalScoreText.get_rect(center=(gameWidth//2, 450))
    window.blit(finalScoreText, finalScoreRect)
    
    replayText = textFont.render("Press 'R' to replay!", True, (220, 20, 60))
    replayRect = replayText.get_rect(center=(gameWidth//2, 520))
    window.blit(replayText, replayRect)

def draw():
    match gameState:
        case "start":
            startScreen()
        case "intro":
            introScreen()
        case "play":
            playScreen()
        case "win":
            winScreen()

async def main():
    global isPlaying, gameState, playPressed, cupX, score, fallingObjects, winLatte
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
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and gameState == "win":
                    score = 0
                    fallingObjects = []
                    cupX = gameWidth // 2
                    winLatte = None
                    gameState = "intro"
        
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
        await asyncio.sleep(0)

asyncio.run(main())