import pygame
import sys

# Initialize pygame and its modules
pygame.init()

# Screen configuration
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Moving Dot Game")

# Clock to control frame rate
clock = pygame.time.Clock()
FPS = 60

# Dot properties
dot_x = SCREEN_WIDTH // 2  # Start at center x
dot_y = SCREEN_HEIGHT // 2  # Start at center y
dot_radius = 10
dot_color = (255, 255, 255)  # White

# Movement properties - velocity-based movement for smooth controls
velocity_x = 0
velocity_y = 0
SPEED = 5  # Pixels per frame when moving

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
        dot_x = SCREEN_WIDTH
    elif dot_x > SCREEN_WIDTH:
        dot_x = 0

    if dot_y < 0:
        dot_y = SCREEN_HEIGHT
    elif dot_y > SCREEN_HEIGHT:
        dot_y = 0

    # Rendering - draw everything to the screen
    screen.fill((0, 0, 0))  # Clear screen with black background
    pygame.draw.circle(screen, dot_color, (int(dot_x), int(dot_y)), dot_radius)  # Draw the dot
    pygame.display.flip()  # Update the display with everything we drew

    # Cap the frame rate to ensure consistent speed across different machines
    clock.tick(FPS)

# Clean up and quit
pygame.quit()
sys.exit()
