import pygame
import sys
import random
import math

# ---------------------------------------------------------------------------
# Init
# ---------------------------------------------------------------------------
pygame.init()
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

# ---------------------------------------------------------------------------
# Colors
# ---------------------------------------------------------------------------
SKY_TOP      = (30,  120, 200)
SKY_BOT      = (135, 206, 235)
GROUND_DIRT  = (83,  56,  71)
GROUND_GRASS = (124, 180, 60)
GROUND_GRASS2= (100, 160, 50)
PIPE_GREEN   = (83,  180, 50)
PIPE_DARK    = (56,  130, 30)
BIRD_BODY    = (255, 220,  0)
BIRD_WING    = (255, 160,  0)
BIRD_EYE_W   = (255, 255, 255)
BIRD_PUPIL   = (  0,   0,   0)
BIRD_BEAK    = (255, 100,   0)
WHITE        = (255, 255, 255)
BLACK        = (  0,   0,   0)
PANEL_BG     = ( 40,  40,  60)
PANEL_BORDER = (255, 200,  50)
RED_TEXT     = (255,  80,  80)
GOLD         = (255, 220,   0)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
PIPE_SPEED_INIT = 3.0
PIPE_WIDTH      = 58
PIPE_CAP_H      = 22
PIPE_CAP_EXTRA  = 8
GAP_MIN         = 145
GAP_MAX         = 175
GROUND_H        = 80
PLAYER_X        = WIDTH // 3
GRAVITY         = 0.38
JUMP_SPEED      = -3.0

# ---------------------------------------------------------------------------
# Fonts
# ---------------------------------------------------------------------------
font_xl  = pygame.font.SysFont("Arial", 64, bold=True)
font_lg  = pygame.font.SysFont("Arial", 48, bold=True)
font_md  = pygame.font.SysFont("Arial", 32, bold=True)
font_sm  = pygame.font.SysFont("Arial", 22)
font_xs  = pygame.font.SysFont("Arial", 18)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def draw_text_shadow(surface, font, text, color, shadow_col, cx, y):
    s = font.render(text, True, shadow_col)
    t = font.render(text, True, color)
    surface.blit(s, (cx - s.get_width() // 2 + 3, y + 3))
    surface.blit(t, (cx - t.get_width() // 2, y))


def draw_sky(surface):
    for y in range(HEIGHT - GROUND_H):
        t = y / (HEIGHT - GROUND_H)
        r = int(SKY_TOP[0] + (SKY_BOT[0] - SKY_TOP[0]) * t)
        g = int(SKY_TOP[1] + (SKY_BOT[1] - SKY_TOP[1]) * t)
        b = int(SKY_TOP[2] + (SKY_BOT[2] - SKY_TOP[2]) * t)
        pygame.draw.line(surface, (r, g, b), (0, y), (WIDTH, y))


def draw_ground(surface, offset):
    pygame.draw.rect(surface, GROUND_DIRT, (0, HEIGHT - GROUND_H, WIDTH, GROUND_H))
    pygame.draw.rect(surface, GROUND_GRASS, (0, HEIGHT - GROUND_H, WIDTH, 22))
    step = 42
    off = int(-offset % step)
    for x in range(off - step, WIDTH + step, step):
        pygame.draw.rect(surface, GROUND_GRASS2, (x, HEIGHT - GROUND_H, step // 2, 22))

# ---------------------------------------------------------------------------
# Cloud
# ---------------------------------------------------------------------------
class Cloud:
    def __init__(self, x=None):
        self.x     = x if x is not None else random.randint(0, WIDTH)
        self.y     = random.randint(40, 180)
        self.speed = random.uniform(0.25, 0.7)
        self.r     = random.randint(28, 55)

    def move(self):
        self.x -= self.speed
        if self.x < -self.r * 3:
            self.x = WIDTH + self.r * 3
            self.y = random.randint(40, 180)

    def draw(self, surface):
        r = self.r
        cx, cy = int(self.x), self.y
        for dx, dy, scale in [(0, 0, 1.0), (-r*0.7, r*0.25, 0.7),
                               (r*0.65, r*0.2, 0.75), (0, -r*0.45, 0.65)]:
            rr = int(r * scale)
            pygame.draw.ellipse(surface, WHITE,
                                (cx + int(dx) - rr, cy + int(dy) - rr//2,
                                 rr * 2, rr))

clouds = [Cloud() for _ in range(6)]

# ---------------------------------------------------------------------------
# Bird
# ---------------------------------------------------------------------------
class Bird:
    def __init__(self):
        self.x        = PLAYER_X
        self.y        = float(HEIGHT // 2)
        self.speed    = 0.0
        self.angle    = 0.0
        self.wing_t   = 0.0

    def jump(self):
        self.speed  = JUMP_SPEED
        self.wing_t = 0.0

    def update(self):
        self.speed += GRAVITY
        self.y     += self.speed
        target      = max(-30.0, min(90.0, self.speed * 6))
        self.angle += (target - self.angle) * 0.18
        self.wing_t += 0.25

    def get_rect(self):
        return pygame.Rect(int(self.x) - 14, int(self.y) - 11, 28, 22)

    def draw(self, surface):
        surf = pygame.Surface((50, 50), pygame.SRCALPHA)
        # wing (behind body)
        wing_dy = int(math.sin(self.wing_t) * 8)
        pygame.draw.ellipse(surf, BIRD_WING, (8, 22 + wing_dy, 22, 9))
        # body
        pygame.draw.ellipse(surf, BIRD_BODY, (6, 13, 32, 22))
        # eye white
        pygame.draw.circle(surf, BIRD_EYE_W, (32, 17), 7)
        # pupil
        pygame.draw.circle(surf, BIRD_PUPIL, (34, 17), 3)
        # beak
        pygame.draw.polygon(surf, BIRD_BEAK, [(38, 18), (48, 22), (38, 25)])

        rotated = pygame.transform.rotate(surf, -self.angle)
        rect    = rotated.get_rect(center=(int(self.x), int(self.y)))
        surface.blit(rotated, rect)

# ---------------------------------------------------------------------------
# Pipe
# ---------------------------------------------------------------------------
class Pipe:
    def __init__(self):
        self.x         = float(WIDTH + PIPE_WIDTH)
        self.gap_start = random.randint(int(HEIGHT * 0.22), int(HEIGHT * 0.48))
        self.gap_end   = self.gap_start + random.randint(GAP_MIN, GAP_MAX)
        self.checked   = False
        self.bonus     = random.randint(1, 12) == 1
        self.bonus_y   = random.randint(self.gap_start + 15, self.gap_end - 20)
        self.bonus_hit = False

    def move(self, speed):
        self.x -= speed

    def get_rects(self):
        hw    = PIPE_WIDTH // 2
        upper = pygame.Rect(int(self.x) - hw, 0, PIPE_WIDTH,
                            self.gap_start - PIPE_CAP_H)
        lower = pygame.Rect(int(self.x) - hw, self.gap_end + PIPE_CAP_H,
                            PIPE_WIDTH, HEIGHT - self.gap_end - PIPE_CAP_H - GROUND_H)
        upper_cap = pygame.Rect(int(self.x) - hw - PIPE_CAP_EXTRA,
                                self.gap_start - PIPE_CAP_H,
                                PIPE_WIDTH + PIPE_CAP_EXTRA * 2, PIPE_CAP_H)
        lower_cap = pygame.Rect(int(self.x) - hw - PIPE_CAP_EXTRA,
                                self.gap_end,
                                PIPE_WIDTH + PIPE_CAP_EXTRA * 2, PIPE_CAP_H)
        bonus = None
        if self.bonus and not self.bonus_hit:
            bonus = pygame.Rect(int(self.x) - 12, self.bonus_y - 12, 24, 24)
        return upper, lower, upper_cap, lower_cap, bonus

    def draw(self, surface):
        hw   = PIPE_WIDTH // 2
        ce   = PIPE_CAP_EXTRA
        ch   = PIPE_CAP_H

        # Upper shaft
        r = pygame.Rect(int(self.x) - hw, 0, PIPE_WIDTH, self.gap_start - ch)
        pygame.draw.rect(surface, PIPE_GREEN, r)
        pygame.draw.rect(surface, PIPE_DARK, r, 3)
        # highlight stripe
        pygame.draw.rect(surface, (130, 220, 90),
                         (int(self.x) - hw + 5, 0, 8, self.gap_start - ch))

        # Upper cap
        cr = pygame.Rect(int(self.x) - hw - ce, self.gap_start - ch,
                         PIPE_WIDTH + ce * 2, ch)
        pygame.draw.rect(surface, PIPE_GREEN, cr)
        pygame.draw.rect(surface, PIPE_DARK, cr, 3)

        # Lower cap
        cr2 = pygame.Rect(int(self.x) - hw - ce, self.gap_end,
                          PIPE_WIDTH + ce * 2, ch)
        pygame.draw.rect(surface, PIPE_GREEN, cr2)
        pygame.draw.rect(surface, PIPE_DARK, cr2, 3)

        # Lower shaft
        r2 = pygame.Rect(int(self.x) - hw, self.gap_end + ch,
                         PIPE_WIDTH, HEIGHT - self.gap_end - ch - GROUND_H)
        pygame.draw.rect(surface, PIPE_GREEN, r2)
        pygame.draw.rect(surface, PIPE_DARK, r2, 3)
        pygame.draw.rect(surface, (130, 220, 90),
                         (int(self.x) - hw + 5, self.gap_end + ch, 8,
                          HEIGHT - self.gap_end - ch - GROUND_H))

        # Bonus orb
        if self.bonus and not self.bonus_hit:
            t    = pygame.time.get_ticks() / 500.0
            pulse= int(abs(math.sin(t)) * 40)
            col  = (180 + pulse, 200, 255)
            cx   = int(self.x)
            cy   = self.bonus_y
            pygame.draw.circle(surface, col,         (cx, cy), 13)
            pygame.draw.circle(surface, (220, 240, 255), (cx, cy), 13, 2)
            star = font_xs.render("★", True, GOLD)
            surface.blit(star, (cx - star.get_width() // 2,
                                cy - star.get_height() // 2))

# ---------------------------------------------------------------------------
# Screens
# ---------------------------------------------------------------------------
def draw_start_screen(surface, best_score, bird_obj):
    draw_sky(surface)
    for c in clouds:
        c.draw(surface)
    draw_ground(surface, 0)

    # Decorative demo bird
    bird_obj.draw(surface)

    # Title
    draw_text_shadow(surface, font_xl, "FLAPPY",  GOLD,       (120, 80, 0), WIDTH // 2, 95)
    draw_text_shadow(surface, font_xl, "BIRD",    BIRD_BODY,  (120, 80, 0), WIDTH // 2, 158)

    # Subtitle box
    box = pygame.Rect(WIDTH // 2 - 140, 240, 280, 44)
    pygame.draw.rect(surface, (0, 0, 0, 0), box)   # transparent fill handled below
    s = pygame.Surface((280, 44), pygame.SRCALPHA)
    s.fill((0, 0, 0, 100))
    surface.blit(s, (WIDTH // 2 - 140, 240))
    pygame.draw.rect(surface, PANEL_BORDER, box, 2, border_radius=8)
    hint = font_sm.render("LEERTASTE  –  Abspringen", True, WHITE)
    surface.blit(hint, (WIDTH // 2 - hint.get_width() // 2, 249))

    # Blinking start prompt
    if (pygame.time.get_ticks() // 550) % 2 == 0:
        start = font_md.render("Drücke LEERTASTE!", True, WHITE)
        surface.blit(start, (WIDTH // 2 - start.get_width() // 2, 320))

    # Best score
    if best_score > 0:
        bs = font_sm.render(f"Rekord: {best_score}", True, GOLD)
        surface.blit(bs, (WIDTH // 2 - bs.get_width() // 2, 385))

    # Auto hint
    auto_h = font_xs.render("[A]  Auto-Pilot umschalten", True, (190, 190, 190))
    surface.blit(auto_h, (WIDTH // 2 - auto_h.get_width() // 2,
                           HEIGHT - GROUND_H - 36))


def draw_gameover_screen(surface, score, best_score):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    surface.blit(overlay, (0, 0))

    pw, ph = 300, 290
    px, py = WIDTH // 2 - pw // 2, HEIGHT // 2 - ph // 2 - 20
    panel  = pygame.Rect(px, py, pw, ph)
    ps     = pygame.Surface((pw, ph), pygame.SRCALPHA)
    ps.fill((40, 40, 70, 230))
    surface.blit(ps, (px, py))
    pygame.draw.rect(surface, PANEL_BORDER, panel, 3, border_radius=14)

    draw_text_shadow(surface, font_lg, "GAME OVER", RED_TEXT, (100, 0, 0),
                     WIDTH // 2, py + 18)

    # Divider
    pygame.draw.line(surface, PANEL_BORDER,
                     (px + 20, py + 80), (px + pw - 20, py + 80), 2)

    # Score
    sc_label = font_xs.render("PUNKTE", True, (180, 180, 180))
    sc_val   = font_lg.render(str(score), True, WHITE)
    surface.blit(sc_label, (WIDTH // 2 - sc_label.get_width() // 2, py + 90))
    surface.blit(sc_val,   (WIDTH // 2 - sc_val.get_width() // 2,   py + 110))

    # Divider 2
    pygame.draw.line(surface, (100, 100, 130),
                     (px + 20, py + 170), (px + pw - 20, py + 170), 1)

    # Best score / new record
    new_record = score > 0 and score >= best_score
    if new_record:
        nr = font_md.render("★  NEUER REKORD  ★", True, GOLD)
        surface.blit(nr, (WIDTH // 2 - nr.get_width() // 2, py + 180))
    else:
        rl = font_xs.render("REKORD", True, (180, 180, 180))
        rv = font_md.render(str(best_score), True, GOLD)
        surface.blit(rl, (WIDTH // 2 - rl.get_width() // 2, py + 182))
        surface.blit(rv, (WIDTH // 2 - rv.get_width() // 2, py + 205))

    # Restart hint (blinking)
    if (pygame.time.get_ticks() // 550) % 2 == 0:
        restart = font_xs.render("LEERTASTE  –  Neustart", True, WHITE)
        surface.blit(restart, (WIDTH // 2 - restart.get_width() // 2, py + ph - 28))

# ---------------------------------------------------------------------------
# Game state
# ---------------------------------------------------------------------------
STATE_START    = 0
STATE_PLAYING  = 1
STATE_GAMEOVER = 2
STATE_AD       = 3

state       = STATE_START
bird        = Bird()
pipes       = []
score       = 0
best_score  = 0
pipe_speed  = PIPE_SPEED_INIT
auto        = False
ground_off  = 0.0

# Demo-bird on start screen hovers gently
demo_t = 0.0

# ---------------------------------------------------------------------------
# Easter-Egg Ad
# ---------------------------------------------------------------------------
AD_DURATION    = 7.0          # Sekunden bis Auto-Skip
AD_SKIP_AFTER  = 3.0          # Sekunden bis manueller Skip erlaubt ist
ad_start_time  = 0.0          # pygame.time.get_ticks() beim Ad-Start (ms)

AD_LINES = [
    ("WERBUNG",            font_lg,  (255, 80,  80),  True),
    ("",                   font_xs,  WHITE,            False),
    ("Du bist pleite?",    font_md,  WHITE,            False),
    ("Vögel machen dich",  font_md,  WHITE,            False),
    ("wahnsinnig?",        font_md,  WHITE,            False),
    ("",                   font_xs,  WHITE,            False),
    ("Dann brauchst du…",  font_sm,  (200, 200, 200),  False),
]
AD_PRODUCT     = "FLAPPY FINANCE™"
AD_SLOGAN      = "Weil auch du endlich Geld\n verdienen willst!"
AD_CTA         = "jetzt unter flappy-finance.de"
AD_BADGE_TEXT  = ["NUR", "9,99 €", "/ Monat"]


def draw_ad_screen(surface, elapsed_sec):
    """Animierter Pre-Roll-Werbespot (YouTube-Style Easter Egg)."""
    t = elapsed_sec

    # --- Hintergrund: sattes Marketing-Lila/Blau-Gradient ---
    for yy in range(HEIGHT):
        frac = yy / HEIGHT
        r = int(20  + frac * 40)
        g = int(0   + frac * 10)
        b = int(80  + frac * 80)
        pygame.draw.line(surface, (r, g, b), (0, yy), (WIDTH, yy))

    # --- Animierter Hintergrund-Shimmer ---
    shimmer_x = int((math.sin(t * 1.8) * 0.5 + 0.5) * WIDTH)
    shimmer_surf = pygame.Surface((120, HEIGHT), pygame.SRCALPHA)
    shimmer_surf.fill((255, 255, 255, 18))
    surface.blit(shimmer_surf, (shimmer_x - 60, 0))

    # --- Slide-in Texte ---
    slide = min(1.0, t / 0.6)           # 0→1 in 0.6s

    # "WERBUNG"-Banner oben links (echtes YouTube-Feeling)
    wb = font_xs.render("Werbung", True, BLACK)
    wb_bg = pygame.Rect(8, 8, wb.get_width() + 14, wb.get_height() + 6)
    pygame.draw.rect(surface, (255, 200, 0), wb_bg, border_radius=4)
    surface.blit(wb, (15, 11))

    # Skip-Countdown oben rechts
    skip_after = AD_SKIP_AFTER
    if elapsed_sec < skip_after:
        remaining = int(skip_after - elapsed_sec) + 1
        sk = font_xs.render(f"Überspringen in {remaining} …", True, (200, 200, 200))
        surface.blit(sk, (WIDTH - sk.get_width() - 10, 11))
    else:
        sk_bg = pygame.Rect(WIDTH - 170, 6, 162, 28)
        pygame.draw.rect(surface, (60, 60, 60), sk_bg, border_radius=6)
        pygame.draw.rect(surface, WHITE, sk_bg, 2, border_radius=6)
        sk = font_xs.render("► LEERTASTE  –  Skip Ad", True, WHITE)
        surface.blit(sk, (WIDTH - sk.get_width() - 14, 12))

    # --- Produkt-Logo (zentriert, slides in) ---
    logo_y = int(55 - (1 - slide) * 60)
    logo_surf = font_lg.render(AD_PRODUCT, True, (255, 220, 0))
    # Schatten
    logo_sh   = font_lg.render(AD_PRODUCT, True, (80, 60, 0))
    surface.blit(logo_sh, (WIDTH // 2 - logo_surf.get_width() // 2 + 4, logo_y + 4))
    surface.blit(logo_surf, (WIDTH // 2 - logo_surf.get_width() // 2, logo_y))

    # Trennlinie
    lw = int(slide * 260)
    pygame.draw.line(surface, (255, 220, 0),
                     (WIDTH // 2 - lw // 2, logo_y + 56),
                     (WIDTH // 2 + lw // 2, logo_y + 56), 2)

    # --- Werbetext-Lines ---
    base_y = 135
    for i, (text, fnt, col, _bold) in enumerate(AD_LINES):
        delay = i * 0.12
        alpha_t = max(0.0, min(1.0, (t - delay) / 0.35))
        if alpha_t <= 0:
            continue
        offset_x = int((1 - alpha_t) * 30)
        rendered = fnt.render(text, True, col)
        surface.blit(rendered,
                     (WIDTH // 2 - rendered.get_width() // 2 + offset_x, base_y + i * 34))

    # --- Preis-Badge (pulsierend, rotiert reingedreht) ---
    badge_t = max(0.0, t - 1.5)
    badge_scale = min(1.0, badge_t / 0.4)
    if badge_scale > 0:
        pulse = 1.0 + math.sin(t * 4) * 0.04
        bsz   = int(72 * badge_scale * pulse)
        bx, by = WIDTH - 80, 160
        pygame.draw.circle(surface, (220, 0, 0),   (bx, by), bsz)
        pygame.draw.circle(surface, (255, 80, 80), (bx, by), bsz, 3)
        for ii, bt in enumerate(AD_BADGE_TEXT):
            bf = font_xs if ii != 1 else font_sm
            bs = bf.render(bt, True, WHITE)
            surface.blit(bs, (bx - bs.get_width() // 2,
                               by - 22 + ii * 17))

    # --- Slogan ---
    slogan_t = max(0.0, t - 2.0)
    if slogan_t > 0:
        alpha = min(1.0, slogan_t / 0.5)
        for ii, sl in enumerate(AD_SLOGAN.split("\n")):
            ss = font_sm.render(sl.strip(), True,
                                (int(255 * alpha), int(255 * alpha), int(200 * alpha)))
            surface.blit(ss, (WIDTH // 2 - ss.get_width() // 2,
                               390 + ii * 30))

    # --- CTA-Banner unten ---
    cta_t = max(0.0, t - 3.0)
    if cta_t > 0:
        cta_alpha = min(1.0, cta_t / 0.4)
        cta_surf  = pygame.Surface((WIDTH, 42), pygame.SRCALPHA)
        cta_surf.fill((255, 220, 0, int(220 * cta_alpha)))
        surface.blit(cta_surf, (0, HEIGHT - GROUND_H - 42))
        cta_text = font_xs.render(AD_CTA, True, BLACK)
        surface.blit(cta_text,
                     (WIDTH // 2 - cta_text.get_width() // 2,
                      HEIGHT - GROUND_H - 42 + 12))

    # --- Fortschrittsbalken unten ---
    bar_w = int(WIDTH * min(1.0, elapsed_sec / AD_DURATION))
    pygame.draw.rect(surface, (60, 60, 60), (0, HEIGHT - 5, WIDTH, 5))
    pygame.draw.rect(surface, (255, 0, 0),  (0, HEIGHT - 5, bar_w, 5))

# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------
running = True
while running:

    # --- Events ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if state == STATE_START:
                    state      = STATE_PLAYING
                    bird       = Bird()
                    pipes      = [Pipe()]
                    score      = 0
                    pipe_speed = PIPE_SPEED_INIT
                    ground_off = 0.0

                elif state == STATE_PLAYING:
                    bird.jump()

                elif state == STATE_GAMEOVER:
                    # Easter Egg: erst Werbung, dann Neustart
                    state         = STATE_AD
                    ad_start_time = pygame.time.get_ticks()

                elif state == STATE_AD:
                    elapsed = (pygame.time.get_ticks() - ad_start_time) / 1000.0
                    if elapsed >= AD_SKIP_AFTER:
                        state = STATE_START

            elif event.key == pygame.K_a:
                auto = not auto

    # --- Auto-pilot ---
    if state == STATE_PLAYING and auto:
        curr = 0
        while curr < len(pipes) and pipes[curr].checked:
            curr += 1
        if curr < len(pipes):
            p   = pipes[curr]
            mid = (p.gap_start + p.gap_end) // 2
            if bird.y > mid + 15:
                bird.jump()

    # --- Update ---
    if state == STATE_PLAYING:
        bird.update()
        ground_off = (ground_off + pipe_speed) % 42

        # Out of bounds
        if bird.y > HEIGHT - GROUND_H - 11 or bird.y < 0:
            state = STATE_GAMEOVER
            if score > best_score:
                best_score = score

        pipe_speed += 0.004

        for p in pipes:
            p.move(pipe_speed)
            upper, lower, ucap, lcap, bonus = p.get_rects()
            br = bird.get_rect()

            if not p.checked and p.x < PLAYER_X:
                p.checked = True
                score    += 1

            if (br.colliderect(upper) or br.colliderect(lower)
                    or br.colliderect(ucap) or br.colliderect(lcap)):
                state = STATE_GAMEOVER
                if score > best_score:
                    best_score = score

            if bonus and br.colliderect(bonus):
                p.bonus_hit = True
                pipe_speed  = max(PIPE_SPEED_INIT, pipe_speed - 1.5)

        # Spawn / remove pipes
        if not pipes or pipes[-1].x < WIDTH - 195:
            pipes.append(Pipe())
        while pipes and pipes[0].x < -PIPE_WIDTH - PIPE_CAP_EXTRA:
            pipes.pop(0)

    # Update clouds always (also on start/gameover)
    for c in clouds:
        c.move()

    # Demo bird hover on start screen
    if state == STATE_START:
        demo_t    += 0.05
        bird.x     = WIDTH // 2
        bird.y     = HEIGHT // 2 - 60 + math.sin(demo_t) * 12
        bird.angle = math.sin(demo_t) * 8
        bird.wing_t += 0.2

    # --- Render ---
    draw_sky(screen)
    for c in clouds:
        c.draw(screen)

    if state == STATE_START:
        draw_start_screen(screen, best_score, bird)

    elif state == STATE_PLAYING:
        draw_ground(screen, ground_off)
        for p in pipes:
            p.draw(screen)
        bird.draw(screen)

        # Score display
        sc_shadow = font_xl.render(str(score), True, BLACK)
        sc_surf   = font_xl.render(str(score), True, WHITE)
        cx        = WIDTH // 2
        screen.blit(sc_shadow, (cx - sc_shadow.get_width() // 2 + 3, 18))
        screen.blit(sc_surf,   (cx - sc_surf.get_width()   // 2,     15))

        if auto:
            a_txt = font_xs.render("AUTO-PILOT", True, (80, 255, 120))
            screen.blit(a_txt, (8, 8))

    elif state == STATE_GAMEOVER:
        draw_ground(screen, ground_off)
        for p in pipes:
            p.draw(screen)
        bird.draw(screen)
        draw_gameover_screen(screen, score, best_score)

    elif state == STATE_AD:
        elapsed_ad = (pygame.time.get_ticks() - ad_start_time) / 1000.0
        draw_ad_screen(screen, elapsed_ad)
        # Auto-Skip nach AD_DURATION Sekunden
        if elapsed_ad >= AD_DURATION:
            state = STATE_START

    pygame.display.flip()
    clock.tick(60)

# ---------------------------------------------------------------------------
# Cleanup
# ---------------------------------------------------------------------------
pygame.quit()
sys.exit()
