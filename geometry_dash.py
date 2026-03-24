import pygame
import random

pygame.init()

# ------------------- Konstanten -------------------
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
GREEN = (0, 200, 0)
RED = (255, 50, 50)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Geometry Dash Advanced")
clock = pygame.time.Clock()

# ------------------- Patterns für Level -------------------
PATTERNS = [
    [
        {"type": "platform", "x": 400, "y": 300, "w": 120, "h": 20},
        {"type": "spike", "x": 600, "y": 350},
    ],
    [
        {"type": "platform", "x": 400, "y": 250, "w": 100, "h": 20},
        {"type": "platform", "x": 600, "y": 200, "w": 100, "h": 20},
        {"type": "spike", "x": 750, "y": 200},
    ],
    [
        {"type": "spike", "x": 500, "y": 350},
        {"type": "spike", "x": 600, "y": 350},
        {"type": "platform", "x": 800, "y": 280, "w": 120, "h": 20},
    ],
    [
        {"type": "platform", "x": 400, "y": 320, "w": 150, "h": 20},
        {"type": "spike", "x": 600, "y": 300},
        {"type": "platform", "x": 800, "y": 260, "w": 100, "h": 20},
    ]
]

# ------------------- Level generieren -------------------
def generate_level(length=80):
    level = []
    offset = 0
    for _ in range(length):
        pattern = random.choice(PATTERNS)
        for obj in pattern:
            new_obj = obj.copy()
            new_obj["x"] += offset + random.randint(-30, 30)
            if "y" in new_obj:
                new_obj["y"] += random.randint(-20, 20)
            level.append(new_obj)
        offset += random.randint(400, 700)
    return level

LEVEL = generate_level(80)  # Länge des Levels

# ------------------- Player -------------------
class Player:
    def __init__(self):
        self.size = 40
        self.x = 100
        self.y = SCREEN_HEIGHT - self.size - 50
        self.vel_y = 0
        self.gravity = 0.8
        self.jump_strength = -15

        self.angle = 0
        self.rotation_speed = 8

    def jump(self):
        # Kein Jump-Limit, man kann jederzeit springen
        self.vel_y = self.jump_strength

    def update(self, platforms):
        self.vel_y += self.gravity
        self.y += self.vel_y

        # Rotation in der Luft
        if self.vel_y != 0:
            self.angle -= self.rotation_speed
            self.angle %= 360

        player_rect = pygame.Rect(self.x, self.y, self.size, self.size)
        LANDING_TOLERANCE = 10

        for p in platforms:
            if player_rect.colliderect(p.rect):
                if self.vel_y > 0 and player_rect.bottom - self.vel_y <= p.rect.top + LANDING_TOLERANCE:
                    self.y = p.rect.top - self.size
                    self.vel_y = 0
                    self.angle = 0

        # Boden
        ground_y = SCREEN_HEIGHT - 50
        if self.y >= ground_y - self.size:
            self.y = ground_y - self.size
            self.vel_y = 0
            self.angle = 0

    def draw(self):
        surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.rect(surf, CYAN, (0, 0, self.size, self.size))

        rotated = pygame.transform.rotate(surf, self.angle)
        rect = rotated.get_rect(center=(self.x + self.size // 2, self.y + self.size // 2))
        screen.blit(rotated, rect.topleft)

# ------------------- Plattformen -------------------
class Platform:
    def __init__(self, x, y, w, h, speed):
        self.rect = pygame.Rect(x, y, w, h)
        self.speed = speed

    def update(self):
        self.rect.x -= self.speed

    def draw(self):
        pygame.draw.rect(screen, GREEN, self.rect)

# ------------------- Spikes -------------------
class Spike:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.size = 40
        self.speed = speed

    def update(self):
        self.x -= self.speed

    def draw(self):
        points = [
            (self.x, self.y),
            (self.x + self.size, self.y),
            (self.x + self.size // 2, self.y - self.size)
        ]
        pygame.draw.polygon(screen, RED, points)

    def get_rect(self):
        return pygame.Rect(self.x, self.y - self.size, self.size, self.size)

# ------------------- Game Loop -------------------
def main():
    player = Player()
    platforms = []
    spikes = []

    level_index = 0
    level_offset = 0
    speed = 6

    running = True
    while running:
        screen.fill(BLACK)

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()

        # Level scroll
        level_offset += speed

        # Objekte spawnen
        while level_index < len(LEVEL) and LEVEL[level_index]["x"] <= level_offset + SCREEN_WIDTH:
            obj = LEVEL[level_index]
            if obj["type"] == "platform":
                platforms.append(Platform(SCREEN_WIDTH, obj["y"], obj["w"], obj["h"], speed))
            elif obj["type"] == "spike":
                spikes.append(Spike(SCREEN_WIDTH, obj["y"], speed))
            level_index += 1

        # Update Plattformen
        for p in platforms[:]:
            p.update()
            p.draw()
            if p.rect.right < 0:
                platforms.remove(p)

        # Update Spikes
        for s in spikes[:]:
            s.update()
            s.draw()

            # Kollision
            if player.x < s.x + s.size and player.x + player.size > s.x:
                if player.y < s.y and player.y + player.size > s.y - s.size:
                    print("Game Over")
                    running = False

            if s.x < -50:
                spikes.remove(s)

        # Player
        player.update(platforms)
        player.draw()

        # Boden
        pygame.draw.line(screen, WHITE, (0, SCREEN_HEIGHT - 50), (SCREEN_WIDTH, SCREEN_HEIGHT - 50), 2)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()