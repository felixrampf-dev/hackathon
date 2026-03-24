import pygame
import sys
import random
    
def drawPlayer():
    global playerRect
    playerRect = pygame.draw.rect(screen, (255,255,255), (width/2-10, playerY-10, 20, 20))

class pipe:
    def __init__(self):
        self.width = 30
        self.posX = width + self.width/2
        self.gapStart = random.randint(int(height/3), int(height/2))
        self.gapEnd = self.gapStart + random.randint(int(height/5), int(height/3))
        self.checked = False
        self.bonus = False
        if(random.randint(1, 20) == 1):
            self.bonus = True
        self.bonusPos = random.randint(int(self.gapStart + 0.5*self.width), int(self.gapEnd - 0.5*self.width))
        self.drawPipe()
    
    def drawPipe(self):
        self.upperPipe = pygame.draw.rect(screen, (255,255,255), (self.posX-self.width/2, 0, self.width, self.gapStart))
        self.lowerPipe = pygame.draw.rect(screen, (255,255,255), (self.posX-self.width/2, self.gapEnd, self.width, height-self.gapEnd))
        if(self.bonus):
            self.bonusRect = pygame.draw.rect(screen, (0,0,255), (self.posX - self.width/4, self.bonusPos, self.width/2, self.width/2))

    def movePipe(self):
        self.posX -= pipeSpeed


# Initialize
pygame.init()
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
pipeSpeed = 5

playerY = height/2
playerSpeed = 0
playerAcc = 0.5
playerRect = pygame.draw.rect(screen, (255,255,255), (width/2-10, playerY-10, 20, 20))

pipes = [pipe()]

score = 0
schrift = pygame.font.SysFont("Arial", 50)

# Game loop
running = True
game = True
auto = False

while running:
    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game:
                    playerSpeed = -5
                else:
                    game = True
                    pipes = [pipe()]
                    score = 0
                    playerY = height/2
                    playerSpeed = 0
                    playerAcc = 0.5
                    pipeSpeed = 5
            if event.key == pygame.K_a:
                auto = not auto

    if(auto):
        curr = 0
        while pipes[curr].checked:
            curr += 1
        if playerY + 40 > pipes[curr].gapEnd:
            playerSpeed = -5
        elif playerY - 40 > pipes[curr].gapStart:
            if pipes[curr].bonus:
                if playerY - 30 > pipes[curr].bonusPos:
                    playerSpeed = -5
            elif playerY > pipes[curr].gapStart + (0.5*(pipes[curr].gapEnd - pipes[curr].gapStart)):
                playerSpeed = -5

    # Update (game logic goes here)
    if game:
        playerY += playerSpeed
        playerSpeed += playerAcc
        if playerY > height or playerY < 0:
            game = False
        pipeSpeed += 0.01
        for i in pipes:  
            i.movePipe()
            if(i.posX < width/2 and not i.checked):
                i.checked = True
                score += 1
            if(playerRect.colliderect(i.upperPipe) or playerRect.colliderect(i.lowerPipe)):
                game = False
            if(i.bonus and playerRect.colliderect(i.bonusRect)):
                i.bonus = False
                pipeSpeed = 5
        if(pipes[-1].posX < width-(5*pipes[-1].width)):
            pipes.append(pipe())
        while(pipes[0].posX < 0):
            pipes = pipes[1:]

    # Render
    screen.fill((0, 0, 0))  # Clear screen
    # ... draw things ...
    if game:
        text_surface = schrift.render(str(score), True, (255,255,255))
        screen.blit(text_surface, (10, 10))
        for i in pipes:
            i.drawPipe()
        drawPlayer()
    else:
        text_surface = schrift.render(str(score), True, (255,255,255))
        screen.blit(text_surface, (width/2, height/2))
    pygame.display.flip()   # Update display

    # Frame rate
    clock.tick(60) 

# Cleanup
pygame.quit()
sys.exit()