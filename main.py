import pygame
import sys
import random
import math
import array as arr


def show_start_screen(screen, clock):
    """Zeigt den Startbildschirm und gibt 'player' oder 'auto' zurück."""
    SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
    font_title = pygame.font.SysFont(None, 80)
    font_btn   = pygame.font.SysFont(None, 40)
    font_sub   = pygame.font.SysFont(None, 26)

    stars = [(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT),
              random.randint(1, 3), random.randint(80, 220)) for _ in range(150)]

    btn_w, btn_h = 280, 60
    btn_player = pygame.Rect(SCREEN_WIDTH // 2 - btn_w - 20, SCREEN_HEIGHT // 2 + 30, btn_w, btn_h)
    btn_auto   = pygame.Rect(SCREEN_WIDTH // 2 + 20,          SCREEN_HEIGHT // 2 + 30, btn_w, btn_h)

    frame = 0
    while True:
        frame += 1
        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_player.collidepoint(mx, my):
                    return 'player'
                if btn_auto.collidepoint(mx, my):
                    return 'auto'

        # Hintergrund
        for y in range(0, SCREEN_HEIGHT, 4):
            t = y / SCREEN_HEIGHT
            pygame.draw.rect(screen, (int(5 + t * 10), int(5 + t * 15), int(30 + t * 40)), (0, y, SCREEN_WIDTH, 4))

        # Sterne
        for sx, sy, size, b in stars:
            tw = math.sin(frame * 0.05 + sx) * 30
            br = int(max(40, min(255, b + tw)))
            pygame.draw.circle(screen, (br, br, 255), (sx, sy), size)

        # Titel
        t_shadow = font_title.render("Stellar Surfer", True, (20, 10, 60))
        t_text   = font_title.render("Stellar Surfer", True, (255, 233, 80))
        screen.blit(t_shadow, t_shadow.get_rect(center=(SCREEN_WIDTH // 2 + 3, SCREEN_HEIGHT // 2 - 90 + 3)))
        screen.blit(t_text,   t_text.get_rect(center=(SCREEN_WIDTH // 2,       SCREEN_HEIGHT // 2 - 90)))

        sub = font_sub.render("Wähle einen Spielmodus:", True, (160, 160, 220))
        screen.blit(sub, sub.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))

        # Buttons
        for btn, label, base_col, hover_col in [
            (btn_player, "Selbst spielen",       (40, 30, 100), (70, 55, 170)),
            (btn_auto,   "Automatisiert spielen", (20, 60, 40),  (35, 110, 65)),
        ]:
            hovered = btn.collidepoint(mx, my)
            color = hover_col if hovered else base_col
            pygame.draw.rect(screen, color, btn, border_radius=12)
            pygame.draw.rect(screen, (150, 140, 255) if not hovered else (255, 255, 255), btn, 2, border_radius=12)
            lbl = font_btn.render(label, True, (255, 255, 255))
            screen.blit(lbl, lbl.get_rect(center=btn.center))

        pygame.display.flip()
        clock.tick(60)


def create_swoosh_sound():
    """Kurzer Swoosh-Sound beim Sprung: schneller Hochfrequenz-Sweep mit Rauschen."""
    try:
        sample_rate, size, channels = pygame.mixer.get_init()
        duration = 0.18
        n = int(sample_rate * duration)
        max_val = 2 ** (abs(size) - 1) - 1
        buf = arr.array('h')
        for i in range(n):
            t = i / sample_rate
            p = t / duration
            # Sehr schneller Sweep von 800 → 200 Hz (abwärts = Swoosh-Gefühl)
            freq = 800 * math.exp(-p * 2.5) + 200
            env  = math.exp(-p * 6) * min(1.0, p * 60)
            # Reines Sinussignal + etwas Rauschen für Luft-Textur
            wave = math.sin(2 * math.pi * freq * t) * 0.7 + random.uniform(-1, 1) * 0.3
            sample = int(max_val * 0.45 * env * wave)
            sample = max(-max_val, min(max_val, sample))
            for _ in range(channels):
                buf.append(sample)
        return pygame.mixer.Sound(buffer=buf)
    except Exception:
        return None


def create_ambient_sound():
    """Generiert einen loopbaren kosmischen Ambient-Drone als Hintergrundmusik."""
    try:
        sample_rate, size, channels = pygame.mixer.get_init()
        duration = 4.0          # 4 Sekunden Loop (nahtlos)
        n = int(sample_rate * duration)
        max_val = 2 ** (abs(size) - 1) - 1
        buf = arr.array('h')
        for i in range(n):
            t = i / sample_rate
            # Sehr langsame LFO-Modulation für lebendiges Pulsieren
            lfo1 = 0.5 + 0.5 * math.sin(2 * math.pi * 0.18 * t)
            lfo2 = 0.5 + 0.5 * math.sin(2 * math.pi * 0.07 * t + 1.2)
            # Mehrere tiefe Schichten: Grundton + Quinte + Oktave
            layer1 = math.sin(2 * math.pi * 55  * t) * 0.40 * lfo1
            layer2 = math.sin(2 * math.pi * 82  * t) * 0.25 * lfo2
            layer3 = math.sin(2 * math.pi * 110 * t) * 0.20 * lfo1
            layer4 = math.sin(2 * math.pi * 27  * t) * 0.15        # Subbass
            # Sehr leises kosmisches Rauschen
            noise  = random.uniform(-1, 1) * 0.04
            wave   = layer1 + layer2 + layer3 + layer4 + noise
            sample = int(max_val * 0.30 * wave)
            sample = max(-max_val, min(max_val, sample))
            for _ in range(channels):
                buf.append(sample)
        return pygame.mixer.Sound(buffer=buf)
    except Exception:
        return None


def create_explosion_sound():
    """Generiert einen tiefen kosmischen Explosions-Boom."""
    try:
        sample_rate, size, channels = pygame.mixer.get_init()
        duration = 1.1
        n = int(sample_rate * duration)
        max_val = 2 ** (abs(size) - 1) - 1
        buf = arr.array('h')
        for i in range(n):
            t = i / sample_rate
            p = t / duration
            # Tiefer Boom: starker Attack, langer Abfall
            env = math.exp(-p * 3.5) * min(1.0, p * 60)
            # Weißes Rauschen als Basis für Explosion
            noise = random.uniform(-1.0, 1.0)
            # Tiefer Sinuston (50 Hz) der schnell abklingt — der "Boom"
            boom = math.sin(2 * math.pi * 55 * t) * math.exp(-p * 6)
            # Mittlerer Rumble (120 Hz)
            rumble = math.sin(2 * math.pi * 120 * t) * math.exp(-p * 8)
            wave = noise * 0.35 + boom * 0.45 + rumble * 0.20
            sample = int(max_val * 0.6 * env * wave)
            sample = max(-max_val, min(max_val, sample))
            for _ in range(channels):
                buf.append(sample)
        return pygame.mixer.Sound(buffer=buf)
    except Exception:
        return None


def do_jump(dot_x, dot_y, jump_particles, jump_sound=None):
    """Führt einen Sprung aus, spielt Sound und spawnt Partikel. Gibt velocity_y zurück."""
    if jump_sound:
        jump_sound.play()
    for _ in range(12):
        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(1.5, 5.0)
        color = random.choice([(255, 220, 50), (255, 180, 30), (255, 255, 150), (200, 160, 255)])
        jump_particles.append([dot_x, dot_y,
                                math.cos(angle) * speed, math.sin(angle) * speed,
                                22, 22, color])
    return -45


def main():
    score = -1
    pygame.init()

    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Stellar Surfer")

    clock = pygame.time.Clock()
    FPS = 60

    auto_play = show_start_screen(screen, clock) == 'auto'
    character = show_character_select(screen, clock)
    jump_sound      = create_swoosh_sound()
    explosion_sound = create_explosion_sound()
    ambient_sound   = create_ambient_sound()
    if ambient_sound:
        ambient_sound.play(-1)   # -1 = unendlicher Loop

    dot_x = SCREEN_WIDTH // 2 - 300
    dot_y = SCREEN_HEIGHT // 2

    velocity_x = 0
    velocity_y = 0
    gravity    = -1.8
    block_pos   = 300
    block_pos2  = 10
    block_speed = 2.5

    # --- Parallax-Sternschichten (3 Ebenen) ---
    # Jede Ebene: Liste von (base_x, y, size, brightness, twinkle_offset)
    layer_far  = [(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT),
                   1, random.randint(40, 110), random.uniform(0, math.pi * 2)) for _ in range(120)]
    layer_mid  = [(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT),
                   2, random.randint(90, 180), random.uniform(0, math.pi * 2)) for _ in range(70)]
    layer_near = [(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT),
                   3, random.randint(150, 230), random.uniform(0, math.pi * 2)) for _ in range(35)]
    scroll_far  = 0.0
    scroll_mid  = 0.0
    scroll_near = 0.0

    # --- Planet / Mond ---
    planet_x = 660.0
    planet_y = 90
    planet_r = 55

    # Shooting stars / Embers
    shooting_stars = []
    shoot_timer = 0

    # --- Welten ---
    world = 1
    WORLD2_SCORE = 10
    transition_alpha = 0      # 0-255 für Überblend-Flash
    transitioning   = False

    # Theme-Werte pro Welt
    THEMES = {
        1: dict(bg_top=(5,5,30),   bg_bot=(15,20,70),
                star=(lambda b: (b, b, 255)),
                block_fill=(60,40,120), block_edge=(100,70,200), block_glow=(120,80,255),
                streak=(220,220,255)),
        2: dict(bg_top=(35,5,0),   bg_bot=(80,20,0),
                star=(lambda b: (255, max(0,int(b*0.55)), 0)),
                block_fill=(110,20,5), block_edge=(210,80,0), block_glow=(255,100,20),
                streak=(255,160,40)),
    }

    running = True

    h = random.randint(150, 400)
    hh = 600 - h - 95
    h2 = random.randint(150, 400)
    h2h = 600 - h2 - 95

    shield_blocks_remaining = 0

    pickup_x = 600
    pickup_y = shield_challenge_y(hh, SCREEN_HEIGHT - h)
    pickup_type = 'shield'
    pickup_on_screen = True
    pickup_blocks_until_spawn = 0

    font_score = pygame.font.SysFont(None, 32)

    frame = 0
    star_rotation = 0.0
    star_spin = 0.0

    # --- Sprung-Partikel ---
    jump_particles = []  # [x, y, vx, vy, life, max_life, color]
    auto_jump_cooldown = 0

    while running:
        frame += 1

        # Parallax-Scroll-Positionen
        scroll_far  += 0.25
        scroll_mid  += 0.6
        scroll_near += 1.1

        if block_pos <= 10:
            score += 1
            h = random.randint(150, 400)
            hh = random.randint(600 - h - 110, 600 - h - 95)
            block_pos = 800
            block_speed = 2.5 + (score // 3) * 0.5
            if shield_blocks_remaining > 0:
                shield_blocks_remaining -= 1
            if not pickup_on_screen:
                pickup_blocks_until_spawn -= 1
                if pickup_blocks_until_spawn <= 0:
                    pickup_x = 820
                    pickup_y = shield_challenge_y(hh, SCREEN_HEIGHT - h)
                    pickup_type = random.choice(['shield', 'trap'])
                    pickup_on_screen = True
                    pickup_blocks_until_spawn = random.randint(3, 7)

        if block_pos2 <= 10:
            score += 1
            h2 = random.randint(150, 500)
            h2h = random.randint(600 - h2 - 110, 600 - h2 - 95)
            block_pos2 = 800
            block_speed = 2.5 + (score // 3) * 0.5
            if shield_blocks_remaining > 0:
                shield_blocks_remaining -= 1
            if not pickup_on_screen:
                pickup_blocks_until_spawn -= 1
                if pickup_blocks_until_spawn <= 0:
                    pickup_x = 820
                    pickup_y = shield_challenge_y(h2h, SCREEN_HEIGHT - h2)
                    pickup_type = random.choice(['shield', 'trap'])
                    pickup_on_screen = True
                    pickup_blocks_until_spawn = random.randint(3, 7)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and not auto_play:
                if event.key == pygame.K_SPACE:
                    velocity_y = do_jump(dot_x, dot_y, jump_particles, jump_sound)
                    star_spin += 25

        # --- Bot-Logik ---
        if auto_play:
            if auto_jump_cooldown > 0:
                auto_jump_cooldown -= 1

            # Schritt 1: Freie Zone (Gap) des relevanten Blocks bestimmen.
            # "Am Spieler" = block_pos <= dot_x (linke Kante hat Spieler-X erreicht)
            # "Kommend"    = block_pos > dot_x  (noch nicht am Spieler)
            blocks = [(block_pos, h, hh), (block_pos2, h2, h2h)]
            at_player = [(bhh, SCREEN_HEIGHT - bh)
                         for bx, bh, bhh in blocks if bx <= dot_x]
            upcoming  = [(bx, bhh, SCREEN_HEIGHT - bh)
                         for bx, bh, bhh in blocks if bx > dot_x]

            if at_player:
                # Block liegt gerade am Spieler — dessen Gap ist die freie Zone
                gap_top, gap_bottom = at_player[0]
            elif upcoming:
                # Nächsten kommenden Block nehmen
                _, gap_top, gap_bottom = min(upcoming, key=lambda b: b[0])
            else:
                gap_top, gap_bottom = hh, SCREEN_HEIGHT - h

            # Schritt 2: Wo ist der Spieler in LOOKAHEAD Frames ohne Sprung?
            LOOKAHEAD = 30
            predicted_y = dot_y + 1.8 * LOOKAHEAD

            # Schritt 3: Sprungentscheidung
            # Springe wenn der Spieler aus der freien Zone fällt UND
            # der Sprung nicht in den oberen Block führt
            will_exit_bottom = predicted_y > gap_bottom - 8
            wont_hit_top     = dot_y - 45 > gap_top + 8

            # Notfall: sofort springen wenn bereits zu tief
            emergency = dot_y >= gap_bottom - 5 and dot_y - 45 > gap_top

            if (will_exit_bottom and wont_hit_top and auto_jump_cooldown == 0) or emergency:
                velocity_y = do_jump(dot_x, dot_y, jump_particles, jump_sound)
                star_spin += 25
                auto_jump_cooldown = 15

        dot_x += velocity_x
        dot_y += velocity_y
        velocity_y = 0
        dot_y -= gravity
        block_pos -= block_speed
        block_pos2 -= block_speed
        planet_x -= 0.18  # Planet scrollt sehr langsam
        if planet_x < -planet_r - 10:
            planet_x = SCREEN_WIDTH + planet_r + 10

        # Sprung-Partikel updaten
        for p in jump_particles[:]:
            p[0] += p[2]
            p[1] += p[3]
            p[3] += 0.15  # leichte Schwerkraft auf Partikel
            p[4] -= 1
            if p[4] <= 0:
                jump_particles.remove(p)

        # Pickup bewegen und einsammeln
        if pickup_on_screen:
            pickup_x -= block_speed
            if pickup_x < -20:
                pickup_on_screen = False
                pickup_blocks_until_spawn = random.randint(3, 7)
            elif math.hypot(dot_x - pickup_x, dot_y - pickup_y) < 20:
                if pickup_type == 'shield':
                    shield_blocks_remaining = 3
                else:
                    score = max(0, score - 3)
                pickup_on_screen = False
                pickup_blocks_until_spawn = random.randint(3, 7)

        if shield_blocks_remaining == 0:
            if (dot_x >= block_pos and dot_x <= SCREEN_WIDTH - 700) and dot_y > (SCREEN_HEIGHT - h) or \
               (dot_x >= block_pos2 and dot_x <= SCREEN_WIDTH - 700) and dot_y > (SCREEN_HEIGHT - h2):
                running = False
            if ((dot_x >= block_pos and dot_x <= SCREEN_WIDTH - 700) and dot_y < hh) or \
               ((dot_x >= block_pos2 and dot_x <= SCREEN_WIDTH - 700) and dot_y < h2h):
                running = False

        if dot_x < 0:
            dot_x = SCREEN_WIDTH
        elif dot_x > SCREEN_WIDTH:
            dot_x = 0
        if dot_y < 0:
            dot_y = SCREEN_HEIGHT
        elif dot_y > SCREEN_HEIGHT:
            dot_y = 0

        # --- Welten-Wechsel prüfen ---
        if world == 1 and max(score, 0) >= WORLD2_SCORE and not transitioning:
            transitioning = True
            transition_alpha = 0

        if transitioning:
            transition_alpha += 6
            if transition_alpha >= 255:
                world = 2
                transitioning = False
                transition_alpha = 255
        elif world == 2 and transition_alpha > 0:
            transition_alpha = max(0, transition_alpha - 6)

        theme = THEMES[world]

        # --- Rendering ---

        # Hintergrund-Farbverlauf (weltabhängig)
        r0, g0, b0 = theme['bg_top']
        r1, g1, b1 = theme['bg_bot']
        for y in range(0, SCREEN_HEIGHT, 4):
            tf = y / SCREEN_HEIGHT
            pygame.draw.rect(screen,
                (int(r0 + tf*(r1-r0)), int(g0 + tf*(g1-g0)), int(b0 + tf*(b1-b0))),
                (0, y, SCREEN_WIDTH, 4))

        # Himmelskörper
        if world == 1:
            draw_planet(screen, int(planet_x), planet_y, planet_r, frame)
        else:
            draw_red_giant(screen, int(planet_x), planet_y, planet_r, frame)

        # Parallax-Sterne / Glut
        t = frame / 60.0
        star_fn = theme['star']
        for base_x, sy, size, brightness, tw in layer_far:
            sx = int((base_x - scroll_far) % SCREEN_WIDTH)
            b = int(max(30, min(130, brightness + math.sin(t * 1.5 + tw) * 20)))
            pygame.draw.circle(screen, star_fn(b), (sx, sy), size)
        for base_x, sy, size, brightness, tw in layer_mid:
            sx = int((base_x - scroll_mid) % SCREEN_WIDTH)
            b = int(max(60, min(200, brightness + math.sin(t * 2 + tw) * 35)))
            pygame.draw.circle(screen, star_fn(b), (sx, sy), size)
        for base_x, sy, size, brightness, tw in layer_near:
            sx = int((base_x - scroll_near) % SCREEN_WIDTH)
            b = int(max(100, min(255, brightness + math.sin(t * 3 + tw) * 55)))
            pygame.draw.circle(screen, star_fn(b), (sx, sy), size)

        # Sternschnuppen / Glutfunken
        shoot_timer += 1
        if shoot_timer > random.randint(90, 180):
            shoot_timer = 0
            shooting_stars.append([random.randint(0, SCREEN_WIDTH),
                                    random.randint(0, SCREEN_HEIGHT // 2),
                                    random.uniform(6, 12)])
        streak_col = theme['streak']
        for ss in shooting_stars[:]:
            ss[0] += ss[2] * 1.5
            ss[1] += ss[2]
            pygame.draw.line(screen, streak_col,
                             (int(ss[0]), int(ss[1])),
                             (int(ss[0] - ss[2] * 3), int(ss[1] - ss[2] * 2)), 2)
            if ss[0] > SCREEN_WIDTH or ss[1] > SCREEN_HEIGHT:
                shooting_stars.remove(ss)

        # Obstacle blocks (weltabhängig)
        bf = theme['block_fill']
        be = theme['block_edge']
        bg = theme['block_glow']
        block_w = SCREEN_WIDTH - 700
        for bx, bh, bhh in [(block_pos, h, hh), (block_pos2, h2, h2h)]:
            alpha = int(min(255, max(0, (SCREEN_WIDTH - bx) / 120 * 255)))
            block_surf = pygame.Surface((block_w, SCREEN_HEIGHT), pygame.SRCALPHA)
            pygame.draw.rect(block_surf, (*bf, alpha), (0, SCREEN_HEIGHT - bh, block_w, bh + 100))
            pygame.draw.rect(block_surf, (*be, alpha), (0, SCREEN_HEIGHT - bh, block_w, 4))
            pygame.draw.rect(block_surf, (*bf, alpha), (0, 0, block_w, bhh))
            pygame.draw.rect(block_surf, (*be, alpha), (0, bhh - 4, block_w, 4))
            screen.blit(block_surf, (bx, 0))
            glow_surf = pygame.Surface((block_w + 6, SCREEN_HEIGHT), pygame.SRCALPHA)
            ga = alpha // 6
            pygame.draw.rect(glow_surf, (*bg, ga), (0, SCREEN_HEIGHT - bh - 3, block_w + 6, 10))
            pygame.draw.rect(glow_surf, (*bg, ga), (0, bhh - 3, block_w + 6, 10))
            screen.blit(glow_surf, (bx - 3, 0))

        # Übergangs-Flash + Welt-Label
        if transition_alpha > 0:
            flash = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            flash.fill((255, 200, 100, min(transition_alpha, 180)))
            screen.blit(flash, (0, 0))
            if transitioning or transition_alpha > 100:
                font_w = pygame.font.SysFont(None, 72)
                lbl = font_w.render("Welt 2 — Lavahölle", True, (255, 80, 0))
                screen.blit(lbl, lbl.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))

        # Pickup
        if pickup_on_screen:
            if pickup_type == 'shield':
                draw_shield_icon(screen, int(pickup_x), int(pickup_y), 16, frame)
            else:
                draw_trap_icon(screen, int(pickup_x), int(pickup_y), 16, frame)

        # Sprung-Partikel zeichnen
        for p in jump_particles:
            life_ratio = p[4] / p[5]
            alpha = int(life_ratio * 200)
            size = max(1, int(life_ratio * 4))
            psurf = pygame.Surface((size * 2 + 2, size * 2 + 2), pygame.SRCALPHA)
            pygame.draw.circle(psurf, (*p[6], alpha), (size + 1, size + 1), size)
            screen.blit(psurf, (int(p[0]) - size - 1, int(p[1]) - size - 1))

        # Stern-Rotation
        star_rotation += star_spin
        star_spin *= 0.88

        # Spieler
        if shield_blocks_remaining > 0:
            shield_aura = pygame.Surface((80, 80), pygame.SRCALPHA)
            pulse = int(30 + math.sin(frame * 0.15) * 15)
            pygame.draw.circle(shield_aura, (50, 180, 255, pulse + 40), (40, 40), 28)
            pygame.draw.circle(shield_aura, (100, 220, 255, 180), (40, 40), 28, 3)
            screen.blit(shield_aura, (int(dot_x) - 40, int(dot_y) - 40))
        draw_character(screen, character, dot_x, dot_y, star_rotation, frame)

        # HUD
        score_surf = font_score.render(f"Score: {max(score, 0)}", True, (200, 200, 255))
        screen.blit(score_surf, (10, 10))
        if shield_blocks_remaining > 0:
            shield_text = font_score.render(f"Schild: {shield_blocks_remaining}", True, (80, 200, 255))
            screen.blit(shield_text, (10, 38))

        pygame.display.flip()
        clock.tick(FPS)

    # --- Explosion beim Game Over ---
    if explosion_sound:
        explosion_sound.play()
    explosion_particles = []
    for _ in range(35):
        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(2, 9)
        color = random.choice([(255, 233, 0), (255, 180, 30), (255, 120, 50), (200, 160, 255), (255, 255, 200)])
        explosion_particles.append([dot_x, dot_y,
                                     math.cos(angle) * speed, math.sin(angle) * speed,
                                     60, 60, color])

    for _ in range(60):
        # Hintergrund
        for y in range(0, SCREEN_HEIGHT, 4):
            t = y / SCREEN_HEIGHT
            pygame.draw.rect(screen, (int(5 + t * 10), int(5 + t * 15), int(30 + t * 40)), (0, y, SCREEN_WIDTH, 4))
        draw_planet(screen, int(planet_x), planet_y, planet_r, frame)
        for base_x, sy, size, brightness, tw in layer_far:
            sx = int((base_x - scroll_far) % SCREEN_WIDTH)
            pygame.draw.circle(screen, (brightness, brightness, brightness), (sx, sy), size)

        # Partikel updaten + zeichnen
        for p in explosion_particles[:]:
            p[0] += p[2]
            p[1] += p[3]
            p[3] += 0.2
            p[4] -= 1
            if p[4] <= 0:
                explosion_particles.remove(p)
                continue
            life_ratio = p[4] / p[5]
            alpha = int(life_ratio * 230)
            size = max(1, int(life_ratio * 5))
            psurf = pygame.Surface((size * 2 + 2, size * 2 + 2), pygame.SRCALPHA)
            pygame.draw.circle(psurf, (*p[6], alpha), (size + 1, size + 1), size)
            screen.blit(psurf, (int(p[0]) - size - 1, int(p[1]) - size - 1))

        pygame.display.flip()
        clock.tick(FPS)

    # --- Game Over Screen ---
    while True:
        for y in range(0, SCREEN_HEIGHT, 4):
            t = y / SCREEN_HEIGHT
            pygame.draw.rect(screen, (int(5 + t * 10), int(5 + t * 15), int(30 + t * 40)), (0, y, SCREEN_WIDTH, 4))
        draw_planet(screen, int(planet_x), planet_y, planet_r, frame)
        for base_x, sy, size, brightness, _ in layer_far:
            sx = int((base_x - scroll_far) % SCREEN_WIDTH)
            pygame.draw.circle(screen, (brightness, brightness, 255), (sx, sy), size)

        font  = pygame.font.SysFont(None, 72)
        font2 = pygame.font.SysFont(None, 36)
        font3 = pygame.font.SysFont(None, 24)

        shadow = font.render("Game Over", True, (80, 0, 0))
        screen.blit(shadow, shadow.get_rect(center=(SCREEN_WIDTH // 2 + 3, SCREEN_HEIGHT // 2 - 47)))
        text = font.render("Game Over", True, (220, 50, 80))
        screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)))

        score_text = font2.render(f"Score: {max(score, 0)}", True, (200, 200, 255))
        screen.blit(score_text, score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)))

        hint = font3.render("Drücke eine Taste zum Beenden", True, (120, 120, 180))
        screen.blit(hint, hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70)))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                pygame.quit()
                sys.exit()


def show_character_select(screen, clock):
    """Charakter-Auswahl: Stern, Meteorit oder Erde. Gibt 'stern', 'meteor' oder 'erde' zurück."""
    SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()
    font_title = pygame.font.SysFont(None, 56)
    font_name  = pygame.font.SysFont(None, 36)
    font_hint  = pygame.font.SysFont(None, 24)
    stars = [(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT),
              random.randint(1, 3), random.randint(80, 220)) for _ in range(150)]

    characters = ['stern', 'meteor', 'erde']
    labels     = ['Stern', 'Meteorit', 'Erde']
    card_w, card_h = 180, 220
    spacing = 40
    total_w = len(characters) * card_w + (len(characters) - 1) * spacing
    start_x = (SCREEN_WIDTH - total_w) // 2

    cards = [pygame.Rect(start_x + i * (card_w + spacing),
                         SCREEN_HEIGHT // 2 - card_h // 2 + 20, card_w, card_h)
             for i in range(len(characters))]

    frame = 0
    while True:
        frame += 1
        mx, my = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i, card in enumerate(cards):
                    if card.collidepoint(mx, my):
                        return characters[i]

        # Hintergrund
        for y in range(0, SCREEN_HEIGHT, 4):
            t = y / SCREEN_HEIGHT
            pygame.draw.rect(screen, (int(5 + t * 10), int(5 + t * 15), int(30 + t * 40)),
                             (0, y, SCREEN_WIDTH, 4))
        for sx, sy, size, b in stars:
            br = int(max(40, min(255, b + math.sin(frame * 0.05 + sx) * 30)))
            pygame.draw.circle(screen, (br, br, 255), (sx, sy), size)

        title = font_title.render("Wähle deinen Charakter", True, (200, 200, 255))
        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 130)))

        for i, (card, char, label) in enumerate(zip(cards, characters, labels)):
            hovered = card.collidepoint(mx, my)
            bg = (55, 45, 120) if hovered else (30, 25, 70)
            border = (200, 180, 255) if hovered else (80, 70, 160)
            pygame.draw.rect(screen, bg, card, border_radius=16)
            pygame.draw.rect(screen, border, card, 2, border_radius=16)

            # Charakter-Vorschau in der Mitte der Karte
            cx = card.centerx
            cy = card.top + card_h // 2 - 20
            draw_character(screen, char, cx, cy, frame * 2, frame)

            name_surf = font_name.render(label, True, (255, 255, 255))
            screen.blit(name_surf, name_surf.get_rect(center=(card.centerx, card.bottom - 30)))

        hint = font_hint.render("Klicke um auszuwählen", True, (120, 120, 180))
        screen.blit(hint, hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 40)))

        pygame.display.flip()
        clock.tick(60)


def draw_character(screen, character, x, y, rotation, frame):
    """Zeichnet den gewählten Charakter an Position (x, y)."""
    if character == 'stern':
        glow = pygame.Surface((60, 60), pygame.SRCALPHA)
        pygame.draw.circle(glow, (255, 220, 50, 60), (30, 30), 22)
        screen.blit(glow, (int(x) - 30, int(y) - 30))
        pts = stern(x, y, 5, 5, 12, rotation)
        pygame.draw.polygon(screen, (255, 233, 0), pts)

    elif character == 'meteor':
        # Unregelmäßige Felsform
        base_pts = [(13, 0), (9, -9), (2, -13), (-7, -10),
                    (-13, -3), (-11, 7), (-4, 13), (7, 11), (12, 5)]
        pts = []
        for px, py in base_pts:
            angle = math.atan2(py, px) + math.radians(rotation)
            dist  = math.hypot(px, py)
            pts.append((x + math.cos(angle) * dist, y + math.sin(angle) * dist))
        # Glühender Schweif-Glow
        glow = pygame.Surface((60, 60), pygame.SRCALPHA)
        pygame.draw.circle(glow, (255, 120, 30, 50), (30, 30), 22)
        screen.blit(glow, (int(x) - 30, int(y) - 30))
        pygame.draw.polygon(screen, (100, 80, 65), pts)
        pygame.draw.polygon(screen, (160, 130, 100), pts, 2)
        # Krater
        for cx2, cy2, cr in [(3, -3, 3), (-5, 4, 2), (6, 5, 2)]:
            angle = math.atan2(cy2, cx2) + math.radians(rotation)
            dist  = math.hypot(cx2, cy2)
            rx = int(x + math.cos(angle) * dist)
            ry = int(y + math.sin(angle) * dist)
            pygame.draw.circle(screen, (70, 55, 45), (rx, ry), cr)

    elif character == 'erde':
        r = 13
        ix, iy = int(x), int(y)
        # Glow
        glow = pygame.Surface((60, 60), pygame.SRCALPHA)
        pygame.draw.circle(glow, (50, 150, 255, 45), (30, 30), 22)
        screen.blit(glow, (ix - 30, iy - 30))
        # Ozean
        pygame.draw.circle(screen, (25, 80, 200), (ix, iy), r)
        # Kontinente (drehen mit rotation)
        continents = [(-4, -5, 5, 4), (4, 2, 4, 3), (-3, 4, 3, 2)]
        cont_surf = pygame.Surface((r * 4, r * 4), pygame.SRCALPHA)
        for cx2, cy2, cw, ch in continents:
            angle = math.atan2(cy2, cx2) + math.radians(rotation * 0.4)
            dist  = math.hypot(cx2, cy2)
            rx = int(r * 2 + math.cos(angle) * dist)
            ry = int(r * 2 + math.sin(angle) * dist)
            pygame.draw.ellipse(cont_surf, (40, 160, 60), (rx - cw, ry - ch, cw * 2, ch * 2))
        # Clip auf Kreis
        mask = pygame.Surface((r * 4, r * 4), pygame.SRCALPHA)
        pygame.draw.circle(mask, (255, 255, 255, 255), (r * 2, r * 2), r)
        cont_surf.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
        screen.blit(cont_surf, (ix - r * 2, iy - r * 2))
        # Wolken
        cloud_surf = pygame.Surface((r * 4, r * 4), pygame.SRCALPHA)
        for cx2, cy2 in [(-3, -8), (6, -4), (-7, 3), (2, 7)]:
            angle = math.atan2(cy2, cx2) + math.radians(rotation * 0.2)
            dist  = math.hypot(cx2, cy2)
            rx = int(r * 2 + math.cos(angle) * dist)
            ry = int(r * 2 + math.sin(angle) * dist)
            pygame.draw.circle(cloud_surf, (220, 230, 255, 120), (rx, ry), 3)
        cloud_surf.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
        screen.blit(cloud_surf, (ix - r * 2, iy - r * 2))
        # Rand
        pygame.draw.circle(screen, (60, 120, 220), (ix, iy), r, 2)


def draw_red_giant(screen, x, y, r, frame):
    """Zeichnet einen pulsierenden roten Riesenstern für Welt 2."""
    pad = r + 25
    surf = pygame.Surface((pad * 2, pad * 2), pygame.SRCALPHA)
    cx, cy = pad, pad
    pulse = math.sin(frame * 0.04) * 4   # langsames Pulsieren

    # Äußerer Coronaglow (mehrere Schichten)
    for i in range(7, 0, -1):
        a = int(12 * i)
        pygame.draw.circle(surf, (255, 60, 0, a), (cx, cy), int(r + pulse + i * 5))

    # Hauptkörper — glühend rot-orange
    rr = int(r + pulse)
    pygame.draw.circle(surf, (200, 40, 0),  (cx, cy), rr)
    pygame.draw.circle(surf, (240, 80, 10), (cx, cy), int(rr * 0.75))
    pygame.draw.circle(surf, (255, 140, 30),(cx, cy), int(rr * 0.45))

    # Heller Kern
    pygame.draw.circle(surf, (255, 220, 120), (cx, cy), int(rr * 0.18))

    # Sonnenflecken (dunkle Flecken)
    for fx, fy, fr in [(-14, -10, 7), (16, 8, 5), (-5, 16, 4)]:
        pygame.draw.circle(surf, (140, 20, 0), (cx + fx, cy + fy), fr)

    screen.blit(surf, (x - pad, y - pad))


def draw_planet(screen, x, y, r, frame):
    """Zeichnet einen realistischen Mond mit Licht/Schatten und Kratern."""
    pad = r + 20
    surf = pygame.Surface((pad * 2, pad * 2), pygame.SRCALPHA)
    cx, cy = pad, pad

    # --- Äußerer Glow ---
    for i in range(5, 0, -1):
        glow_alpha = 8 * i
        pygame.draw.circle(surf, (200, 210, 255, glow_alpha), (cx, cy), r + i * 4)

    # --- Mondoberfläche (helles Grau) ---
    pygame.draw.circle(surf, (210, 210, 195), (cx, cy), r)

    # --- Leichte Farbvarianz auf der Oberfläche ---
    pygame.draw.circle(surf, (195, 198, 182), (cx + r // 5, cy + r // 4), r * 2 // 3)

    # --- Krater mit realistischem Schattenwurf ---
    # Format: (offset_x, offset_y, radius)
    craters = [(-16, -14, 11), (18,  6,  8), (-4,  18,  6),
               (24, -20,  7), (-24, 12,  5), (8, -28, 4), (-10, -2, 3)]
    for cx2, cy2, cr in craters:
        # Krater-Boden (etwas dunkler)
        pygame.draw.circle(surf, (175, 175, 162), (cx + cx2, cy + cy2), cr)
        # Schatten-Rand unten-rechts
        pygame.draw.arc(surf, (145, 145, 132),
                        (cx + cx2 - cr, cy + cy2 - cr, cr * 2, cr * 2),
                        math.radians(30), math.radians(210), 2)
        # Licht-Rand oben-links
        pygame.draw.arc(surf, (230, 230, 218),
                        (cx + cx2 - cr, cy + cy2 - cr, cr * 2, cr * 2),
                        math.radians(210), math.radians(30), 1)

    # --- Nachtseite: dunkle Überlagerung von rechts (Halbmond-Effekt) ---
    shadow = pygame.Surface((pad * 2, pad * 2), pygame.SRCALPHA)
    pygame.draw.circle(shadow, (8, 12, 28, 0), (cx, cy), r)   # transparenter Basis-Clip
    # Überlappender Kreis leicht versetzt → erzeugt Sichel / Dreiviertelmond
    offset = int(r * 0.35)
    pygame.draw.circle(shadow, (8, 12, 28, 210), (cx + offset, cy), r)
    surf.blit(shadow, (0, 0))

    # --- Terminator-Weichzeichnung (sanfter Übergang hell→dunkel) ---
    for i in range(1, 5):
        term_alpha = 30 - i * 6
        pygame.draw.circle(surf, (8, 12, 28, term_alpha),
                           (cx + offset - i * 3, cy), r - i * 2)

    # --- Glanzpunkt oben links ---
    highlight = pygame.Surface((r, r), pygame.SRCALPHA)
    pygame.draw.ellipse(highlight, (255, 255, 245, 45), (0, 0, r, r // 2))
    surf.blit(highlight, (cx - r + r // 5, cy - r + r // 6))

    screen.blit(surf, (x - pad, y - pad))


def shield_challenge_y(gap_top, gap_bottom):
    gap_size = gap_bottom - gap_top
    margin = 18
    third = gap_size // 3
    if random.random() < 0.5:
        return random.randint(gap_top + margin, gap_top + third)
    else:
        return random.randint(gap_bottom - third, gap_bottom - margin)


def draw_trap_icon(screen, x, y, size, frame):
    s = size
    glow_surf = pygame.Surface((s * 4, s * 4), pygame.SRCALPHA)
    pulse = int(40 + math.sin(frame * 0.12) * 20)
    pygame.draw.circle(glow_surf, (200, 30, 30, pulse), (s * 2, s * 2), s + 6)
    screen.blit(glow_surf, (x - s * 2, y - s * 2))
    tri = [(x, y - s), (x + s, y + s), (x - s, y + s)]
    pygame.draw.polygon(screen, (180, 20, 20), tri)
    pygame.draw.polygon(screen, (255, 80, 80), tri, 2)
    pygame.draw.line(screen, (255, 220, 50), (x, y - s // 2 + 2), (x, y + s // 3), 3)
    pygame.draw.circle(screen, (255, 220, 50), (x, y + s // 2 - 2), 2)


def draw_shield_icon(screen, x, y, size, frame):
    s = size
    points = [
        (x,     y - s),
        (x + s, y - s // 2),
        (x + s, y + s // 3),
        (x,     y + s),
        (x - s, y + s // 3),
        (x - s, y - s // 2),
    ]
    glow_surf = pygame.Surface((s * 4, s * 4), pygame.SRCALPHA)
    pulse = int(40 + math.sin(frame * 0.1) * 20)
    pygame.draw.circle(glow_surf, (50, 180, 255, pulse), (s * 2, s * 2), s + 6)
    screen.blit(glow_surf, (x - s * 2, y - s * 2))
    pygame.draw.polygon(screen, (30, 120, 220), points)
    pygame.draw.polygon(screen, (150, 230, 255), points, 2)
    pygame.draw.line(screen, (200, 240, 255), (x, y - s // 2), (x, y + s // 3), 2)
    pygame.draw.line(screen, (200, 240, 255), (x - s // 2, y), (x + s // 2, y), 2)


def stern(x, y, rays, r1, r2, rotation=0):
    points = []
    for i in range(rays * 2):
        angle = math.radians(i * 360 / (rays * 2) - 90 + rotation)
        radius = r2 if i % 2 == 0 else r1
        points.append((x + math.cos(angle) * radius, y + math.sin(angle) * radius))
    return points


main()