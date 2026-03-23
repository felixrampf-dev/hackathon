# Pygame Basics

A quick guide to understanding the fundamentals of pygame.

## What is Pygame?

Pygame is a Python library for creating 2D games and multimedia applications. It's built on top of SDL (Simple DirectMedia Layer) and provides simple, intuitive functions for graphics, sound, and input handling.

## Core Concepts

### 1. Initialization

```python
pygame.init()
```
Initializes all pygame modules. Must be called before using any pygame functionality.

### 2. Display / Screen

```python
screen = pygame.display.set_mode((width, height))
```
Creates a window where everything is drawn. Think of it as a canvas.

### 3. The Game Loop

Every pygame program runs in a continuous loop:

```python
running = True
while running:
    # 1. Handle events
    # 2. Update game state
    # 3. Render/draw everything
    # 4. Control frame rate
```

This loop runs 60+ times per second, creating the illusion of movement.

### 4. Event Handling

```python
for event in pygame.event.get():
    if event.type == pygame.QUIT:
        running = False
    elif event.type == pygame.KEYDOWN:
        # Handle key press
```

Events include mouse clicks, key presses, window actions, etc. Must be processed every frame.

### 5. Drawing

Common drawing functions:
- `screen.fill((r, g, b))` - Fill screen with a color
- `pygame.draw.circle(screen, color, (x, y), radius)` - Draw a circle
- `pygame.draw.rect(screen, color, rect)` - Draw a rectangle
- `pygame.draw.line(screen, color, start_pos, end_pos)` - Draw a line

Colors are RGB tuples: `(red, green, blue)` where each value is 0-255.

### 6. Display Update

```python
pygame.display.flip()
```
Updates the entire screen with everything you've drawn. Call once per frame after all drawing is complete.

### 7. Clock / Frame Rate

```python
clock = pygame.time.Clock()
clock.tick(60)  # Limit to 60 FPS
```
Controls how fast the game loop runs, ensuring consistent speed across different computers.

## Basic Program Structure

```python
import pygame
import sys

# Initialize
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Game loop
running = True
while running:
    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update (game logic goes here)

    # Render
    screen.fill((0, 0, 0))  # Clear screen
    # ... draw things ...
    pygame.display.flip()   # Update display

    # Frame rate
    clock.tick(60)

# Cleanup
pygame.quit()
sys.exit()
```

## Key Input Methods

### Event-based (discrete actions)
```python
if event.type == pygame.KEYDOWN:
    if event.key == pygame.K_SPACE:
        # Jump, shoot, etc.
```
Good for single actions like jumping or shooting.

### State-based (continuous actions)
```python
keys = pygame.key.get_pressed()
if keys[pygame.K_LEFT]:
    x -= speed
```
Good for continuous movement.

## Coordinate System

- Origin (0, 0) is at the **top-left** corner
- X increases to the right
- Y increases **downward**

```
(0,0) -------- X+ -------->
  |
  |
  Y+
  |
  |
  v
```

## Common Pygame Constants

- **Keys**: `pygame.K_UP`, `pygame.K_DOWN`, `pygame.K_LEFT`, `pygame.K_RIGHT`, `pygame.K_SPACE`, etc.
- **Events**: `pygame.QUIT`, `pygame.KEYDOWN`, `pygame.KEYUP`, `pygame.MOUSEBUTTONDOWN`, etc.
- **Colors**: `(0, 0, 0)` = black, `(255, 255, 255)` = white, `(255, 0, 0)` = red

## Resources

- Official Docs: https://www.pygame.org/docs/
- Tutorials: https://www.pygame.org/wiki/tutorials, https://www.geeksforgeeks.org/python/pygame-tutorial/
- Examples: Check pygame's built-in examples with `python -m pygame.examples`
