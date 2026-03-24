import pygame
import sys
import random

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird - 2 Player")

clock = pygame.time.Clock()
FPS = 60

font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 80)

GRAVITY = 0.3
MAX_VELOCITY = 10
JUMP_STRENGTH = -6
OBSTACLE_DISTANCE = 300


class Obstacle:
    WIDTH = 50
    GAP = 150
    SPEED = 5

    def __init__(self, x):
        self.x = x
        self.passed_p1 = False
        self.passed_p2 = False
        self.gap_y = random.randint(100, SCREEN_HEIGHT - 100)
        self.update_rects()

    def update_rects(self):
        self.rect_top = pygame.Rect(self.x, 0, self.WIDTH, self.gap_y - self.GAP // 2)
        self.rect_bottom = pygame.Rect(
            self.x,
            self.gap_y + self.GAP // 2,
            self.WIDTH,
            SCREEN_HEIGHT - (self.gap_y + self.GAP // 2)
        )

    def update(self):
        self.x -= self.SPEED
        self.update_rects()

    def draw(self, surface):
        pygame.draw.rect(surface, (0, 255, 0), self.rect_top)
        pygame.draw.rect(surface, (0, 255, 0), self.rect_bottom)

    def off_screen(self):
        return self.x < -self.WIDTH


class Player:
    RADIUS = 10

    def __init__(self, x, y, color, key):
        self.x = x
        self.y = y
        self.color = color
        self.key = key
        self.vel_y = 0
        self.alive = True
        self.score = 0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == self.key:
            self.vel_y = JUMP_STRENGTH

    def update(self):
        self.vel_y = min(self.vel_y + GRAVITY, MAX_VELOCITY)
        self.y += self.vel_y

        if self.y < self.RADIUS or self.y > SCREEN_HEIGHT - self.RADIUS:
            self.alive = False

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.RADIUS)

    def get_rect(self):
        return pygame.Rect(
            self.x - self.RADIUS,
            self.y - self.RADIUS,
            self.RADIUS * 2,
            self.RADIUS * 2
        )

    def check_collision(self, obstacles):
        rect = self.get_rect()
        for obs in obstacles:
            if rect.colliderect(obs.rect_top) or rect.colliderect(obs.rect_bottom):
                self.alive = False
                return


def reset_game():
    p1 = Player(SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2, (0, 0, 255), pygame.K_SPACE)
    p2 = Player(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2, (255, 0, 0), pygame.K_UP)
    obs = [Obstacle(SCREEN_WIDTH)]
    return p1, p2, obs


def countdown():
    for i in range(3, -1, -1):
        screen.fill((0, 0, 0))

        text = big_font.render(str(i), True, (255, 255, 255))
        rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text, rect)

        pygame.display.flip()
        pygame.time.wait(1000)


def draw_end_screen(p1, p2):
    screen.fill((0, 0, 0))

    if p1.score > p2.score:
        winner = "Player 1 Wins!"
    elif p2.score > p1.score:
        winner = "Player 2 Wins!"
    else:
        winner = "Draw!"

    title = big_font.render(winner, True, (255, 255, 255))
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 100))

    s1 = font.render(f"Player 1 Score: {p1.score}", True, (0, 0, 255))
    s2 = font.render(f"Player 2 Score: {p2.score}", True, (255, 0, 0))

    screen.blit(s1, (SCREEN_WIDTH // 2 - 120, 250))
    screen.blit(s2, (SCREEN_WIDTH // 2 - 120, 300))

    button = pygame.Rect(SCREEN_WIDTH // 2 - 80, 400, 160, 50)
    pygame.draw.rect(screen, (50, 200, 50), button)

    text = font.render("RESTART", True, (0, 0, 0))
    screen.blit(text, (button.x + 25, button.y + 10))

    return button


def main():
    player1, player2, obstacles = reset_game()

    countdown()  # START COUNTDOWN HERE

    running = True
    game_over = False

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if not game_over:
                player1.handle_event(event)
                player2.handle_event(event)

            if game_over and event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.collidepoint(event.pos):
                    player1, player2, obstacles = reset_game()
                    countdown()   # COUNTDOWN ON RESTART
                    game_over = False

        if not game_over:

            # Obstacles + scoring
            for obs in obstacles[:]:
                obs.update()

                if obs.off_screen():
                    obstacles.remove(obs)

                if not obs.passed_p1 and obs.x + obs.WIDTH < player1.x and player1.alive:
                    player1.score += 1
                    obs.passed_p1 = True

                if not obs.passed_p2 and obs.x + obs.WIDTH < player2.x and player2.alive:
                    player2.score += 1
                    obs.passed_p2 = True

            if obstacles[-1].x < SCREEN_WIDTH - OBSTACLE_DISTANCE:
                obstacles.append(Obstacle(SCREEN_WIDTH))

            # Players
            if player1.alive:
                player1.update()
                player1.check_collision(obstacles)

            if player2.alive:
                player2.update()
                player2.check_collision(obstacles)

            if not player1.alive and not player2.alive:
                game_over = True

            # Draw game
            screen.fill((0, 0, 0))

            for obs in obstacles:
                obs.draw(screen)

            if player1.alive:
                player1.draw(screen)
            if player2.alive:
                player2.draw(screen)

            s1 = font.render(f"P1: {player1.score}", True, (0, 0, 255))
            s2 = font.render(f"P2: {player2.score}", True, (255, 0, 0))

            screen.blit(s1, (10, 10))
            screen.blit(s2, (10, 40))

        else:
            restart_button = draw_end_screen(player1, player2)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()