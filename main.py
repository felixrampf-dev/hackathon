import pygame
from pygame.locals import *
import sys

# Initialize pygame and its modules
pygame.init()


vec = pygame.math.Vector2 

# Screen configuration
WIDTH = 800
HEIGHT = 600
ACC = 2
FRIC = -0.12
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Dot Game")


displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))

# Clock to control frame rate
FPS = 60
FramePerSec = pygame.time.Clock()

# Dot properties
dot_x = WIDTH // 2  # Start at center x
dot_y = HEIGHT // 2  # Start at center y
dot_radius = 10
dot_color = (255, 255, 255)  # White

# Movement properties - velocity-based movement for smooth controls
velocity_x = 0
velocity_y = 0
SPEED = 5  # Pixels per frame when moving


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((128,255,40))
        self.rect = self.surf.get_rect()
   
        self.pos = vec((10, 385))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
 
    def move(self):
        self.acc = vec(0,0.05)
    
        pressed_keys = pygame.key.get_pressed()            
        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC
             
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
         
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
            
        self.rect.midbottom = self.pos 


    def update(self):
        hits = pygame.sprite.spritecollide(P1 , platforms, False)
        if hits:
            self.pos.y = hits[0].rect.top + 1
            self.vel.y = 0


        ramp_hit = pygame.sprite.spritecollide(P1, ramps, False)
        if ramp_hit:
            self.vel.y = 0
            
            
            D_rect = ramp_hit[0].rect
            my_rect = P1.rect

            dia_height = D_rect.height * (my_rect.right-D_rect.left) / D_rect.width
            D_rect_top = D_rect.bottom - round(dia_height)
            self.pos.y = D_rect_top
        
 
class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((WIDTH, 20))
        self.surf.fill((255,0,0))
        self.rect = self.surf.get_rect(center = (WIDTH/2, HEIGHT - 10))

class Ramp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((100, 60))
        self.surf.fill((255,255,0))
        self.rect = self.surf.get_rect(center = (WIDTH/2, HEIGHT - 50))


PT1 = Platform()
R1 = Ramp()
P1 = Player()
 
all_sprites = pygame.sprite.Group()
all_sprites.add(PT1)
all_sprites.add(R1)
all_sprites.add(P1)

platforms = pygame.sprite.Group()
platforms.add(PT1)

ramps = pygame.sprite.Group()
ramps.add(R1)


# Main game loop
running = True
while running:
    # Event handling - process all events from the event queue
    for event in pygame.event.get():
        # Check if user wants to quit
        if event.type == pygame.QUIT:
            running = False

        # Key press events - set velocity when arrow key is pressed
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                velocity_x = -SPEED
            elif event.key == pygame.K_RIGHT:
                velocity_x = SPEED
            elif event.key == pygame.K_UP:
                velocity_y = -SPEED
            elif event.key == pygame.K_DOWN:
                velocity_y = SPEED

        # Key release events - stop movement when arrow key is released
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT and velocity_x < 0:
                velocity_x = 0
            elif event.key == pygame.K_RIGHT and velocity_x > 0:
                velocity_x = 0
            elif event.key == pygame.K_UP and velocity_y < 0:
                velocity_y = 0
            elif event.key == pygame.K_DOWN and velocity_y > 0:
                velocity_y = 0

    # Update dot position based on current velocity
    dot_x += velocity_x
    dot_y += velocity_y

    # Wrap around screen edges - dot reappears on opposite side
    if dot_x < 0:
        dot_x = WIDTH
    elif dot_x > WIDTH:
        dot_x = 0

    if dot_y < 0:
        dot_y = HEIGHT
    elif dot_y > HEIGHT:
        dot_y = 0


    #rendering 
    displaysurface.fill((0,0,0))
 
    P1.update()
    P1.move()
    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)
    
    pygame.display.update()
    FramePerSec.tick(FPS)

# Clean up and quit
pygame.quit()
sys.exit()
