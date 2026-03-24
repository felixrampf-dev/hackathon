import pygame
from pygame.locals import *
import sys

# Initialize pygame and its modules
pygame.init()


vec = pygame.math.Vector2 

# Screen configuration
WIDTH = 800
HEIGHT = 600
ACC = 1
FRIC = -0.05

font = pygame.font.SysFont("Arial", 30)
score = 0

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
        self.pos = vec((100, 385))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.x_mov = False
        self.rot = 0.0

        self.orig_surf = pygame.image.load("/home/aris/coding/qaware-pygame/hackathon/resources/flappy.png").convert_alpha()
        self.orig_surf = pygame.transform.scale(self.orig_surf, (40, 30))  # adjust size as needed
        self.surf = self.orig_surf.copy()
        self.rect = self.surf.get_rect()


    def move(self):
        self.acc = vec(0, 0.06)  # gravity only on player
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.midbottom = self.pos

        pressed_keys = pygame.key.get_pressed()
 
        if pressed_keys[K_SPACE]:
            self.x_mov = True
        else:
            self.x_mov = False

        for obj in map_obs:
            obj.acc.x += obj.vel.x * FRIC
            obj.vel += obj.acc
            obj.pos += obj.vel + 0.5 *  obj.acc
            obj.rect.midbottom = obj.pos


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
        

        for obj in map_obs:
            obj.acc.x = 0


        if (hits or ramp_hit) and (self.rot > 120 and self.rot < 240):
            #lost
            reset_game()
            return

        if (hits or ramp_hit) and self.x_mov:
            for obj in map_obs:
                obj.acc.x = -ACC

        elif not (hits or ramp_hit) and self.x_mov:
            self.rot += 6

            if self.rot >= 360.0:
                self.rot = 0.0
        

            self.surf = pygame.transform.rotate(self.orig_surf, self.rot)
            # re-center rect so it doesn't drift
            old_center = self.rect.center
            self.rect = self.surf.get_rect()
            self.rect.center = old_center
 
class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.pos = vec((WIDTH/2, HEIGHT))
        self.vel = vec(0,0)
        self.acc = vec(0,0)

        self.surf = pygame.Surface((WIDTH*100, 20))
        self.surf.fill((255,0,0))
        self.rect = self.surf.get_rect(center = (WIDTH/2, HEIGHT - 10))

class Ramp(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.pos = vec((x, HEIGHT-20))
        self.vel = vec(0,0)
        self.acc = vec(0,0)

        self.image = pygame.image.load("/home/aris/coding/qaware-pygame/hackathon/resources/hd-black-triangle-right-angle.png")
        self.image = pygame.transform.scale(self.image, (100, 60))
        self.surf = self.image 
        self.rect = self.surf.get_rect(center = (WIDTH/2, HEIGHT - 50))


def reset_game():
    global PT1, P1, all_sprites, platforms, ramps, map_obs

    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    ramps = pygame.sprite.Group()
    map_obs = pygame.sprite.Group()

    PT1 = Platform()
    P1 = Player()

    all_sprites.add(PT1, P1)
    platforms.add(PT1)
    map_obs.add(PT1)

    for i in range(50):
        R = Ramp(WIDTH * i)
        ramps.add(R)
        all_sprites.add(R)
        map_obs.add(R)

PT1 = Platform()
P1 = Player()
 
all_sprites = pygame.sprite.Group()
all_sprites.add(PT1)
all_sprites.add(P1)

platforms = pygame.sprite.Group()
platforms.add(PT1)

ramps = pygame.sprite.Group()

map_obs = pygame.sprite.Group()
map_obs.add(PT1)


for i in range(50):
    R = Ramp(WIDTH*i)
    ramps.add(R)
    all_sprites.add(R)
    map_obs.add(R)

# Main game loop
running = True
while running:

    score = - PT1.rect.center[0]+400



    # Event handling - process all events from the event queue
    for event in pygame.event.get():
        # Check if user wants to quit
        if event.type == pygame.QUIT:
            running = False


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
    displaysurface.fill((156, 194, 255))
 
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    displaysurface.blit(score_text, (WIDTH - score_text.get_width() - 10, 10))

    P1.move()
    P1.update()
    for entity in all_sprites:
        displaysurface.blit(entity.surf, entity.rect)
    
    pygame.display.update()
    FramePerSec.tick(FPS)

# Clean up and quit
pygame.quit()
sys.exit()
