import pygame
import random
import os
import pygame.surfarray
import numpy as np
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

pygame.init()

# -----------------------------
# CONFIGURACIÓN GENERAL
# -----------------------------

WIDTH = 800
HEIGHT = 400

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Little Grey Adventure")

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)

blink_timer = 0
glow_timer = 0

instructions_timer = 0
instructions_duration = 180  # ~3 segundos (a 60 FPS)

GROUND_Y = 320
GROUND_HEIGHT = 80

ground_x1 = 0
ground_x2 = 800

overlay_alpha = 0
overlay_active = False
game_over_time = 0
death_screen = None
flash_alpha = 0
shake_timer = 0
shake_intensity = 0

bg_x = 0
far_x = 0
mid_x = 0

bg_speed = 0.1
far_speed = 0.3
mid_speed = 0.5

game_speed = 6

spawn_timer = 0
spawn_delay = 120

distance_since_spawn = 0
spawn_distance = 250

pattern_queue = []
force_gap = False

MAX_JUMP_DISTANCE = 300

jump_distance = 0
max_jump_distance = 0

particles = []

was_on_ground = True

squash_timer = 0

duck_hold_timer = 0

duck_frame = 0
duck_anim_timer = 0
duck_anim_speed = 4  # frames por cambio

ufos = []

# -------------------------
# JUMP IMPROVEMENTS
# -------------------------

coyote_timer = 0
coyote_time_max = 8   # frames (~0.13s)

jump_buffer_timer = 0
jump_buffer_max = 8

# -----------------------------
# COLORES
# -----------------------------

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# -----------------------------
# PLAYER CONFIG
# -----------------------------

PLAYER_SIZE = 96

player_x = 120
player_y = 260

velocity_y = 0
gravity = 0.8
jump_strength = -15

on_ground = True

is_ducking = False
duck_frame = 0
duck_releasing = False

duck_frame = 0
duck_entering = False
duck_releasing = False
is_ducking = False

GROUND_LEVEL = GROUND_Y - PLAYER_SIZE

# -----------------------------
# LOAD PLAYER SPRITES
# -----------------------------

screen = pygame.display.set_mode((WIDTH, HEIGHT))

menu_bg = pygame.image.load(resource_path("assets/menu.png")).convert()
menu_bg = pygame.transform.scale(menu_bg, (WIDTH, HEIGHT))

title_img = pygame.image.load(resource_path("assets/title.png")).convert_alpha()
gameover_img = pygame.image.load(resource_path("assets/gameover.png")).convert_alpha()

title_img = pygame.transform.scale(title_img, (255, 180))
gameover_img = pygame.transform.scale(gameover_img, (225, 150))

run_frames = []
for i in range(1, 9):
    img = pygame.image.load(resource_path(f"assets/player/run{i}.png")).convert_alpha()
    img = pygame.transform.scale(img, (PLAYER_SIZE, PLAYER_SIZE))
    run_frames.append(img)

jump_prepare = pygame.image.load(resource_path("assets/player/jump_prepare.png")).convert_alpha()
jump_up = pygame.image.load(resource_path("assets/player/jump_up.png")).convert_alpha()
jump_peak = pygame.image.load(resource_path("assets/player/jump_peak.png")).convert_alpha()
jump_down = pygame.image.load(resource_path("assets/player/jump_down.png")).convert_alpha()
jump_land = pygame.image.load(resource_path("assets/player/jump_land.png")).convert_alpha()

jump_prepare = pygame.transform.scale(jump_prepare,(PLAYER_SIZE,PLAYER_SIZE))
jump_up = pygame.transform.scale(jump_up,(PLAYER_SIZE,PLAYER_SIZE))
jump_peak = pygame.transform.scale(jump_peak,(PLAYER_SIZE,PLAYER_SIZE))
jump_down = pygame.transform.scale(jump_down,(PLAYER_SIZE,PLAYER_SIZE))
jump_land = pygame.transform.scale(jump_land,(PLAYER_SIZE,PLAYER_SIZE))

bg = pygame.image.load(resource_path("assets/bg.png")).convert()
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))

fog = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
pygame.draw.rect(fog, (20, 30, 60, 40), (0, 0, WIDTH, 250))
fog.fill((20, 30, 60, 15))  # azul muy suave

far = pygame.image.load(resource_path("assets/mountains_far.png")).convert_alpha()
far_height = far.get_height()
far_width = far.get_width()

scale_factor = WIDTH / far_width
new_height = int(far_height * scale_factor)

far = pygame.transform.scale(far, (WIDTH, new_height))

mid = pygame.image.load(resource_path("assets/mountains_mid.png")).convert_alpha()
mid_height = mid.get_height()
mid_width = mid.get_width()

scale_factor = WIDTH / mid_width
new_height = int(mid_height * scale_factor)

mid = pygame.transform.scale(mid, (WIDTH, new_height))

ground_img = pygame.image.load(resource_path("assets/ground.png")).convert_alpha()
ground_img = pygame.transform.scale(ground_img, (800, 80))

small_font = pygame.font.Font(None, 24)

ufo_img = pygame.image.load(resource_path("assets/ufo.png")).convert_alpha()
ufo_img = pygame.transform.scale(ufo_img, (80, 40))  # ajusta a tu gusto

# -----------------------------
# LOAD OBSTACLE SPRITES
# -----------------------------

# rocas
rock_small = pygame.image.load(resource_path("assets/obstacles/rock_small.png")).convert_alpha()
rock_big = pygame.image.load(resource_path("assets/obstacles/rock_big.png")).convert_alpha()
rock_low = pygame.image.load(resource_path("assets/obstacles/rock_low.png")).convert_alpha()

# escalado
rock_small = pygame.transform.scale(rock_small,(50,50))
rock_big = pygame.transform.scale(rock_big,(70,70))
rock_low = pygame.transform.scale(rock_low,(60,35))

# monstruos animados
monster_small_frames = []
monster_big_frames = []
monster_low_frames = []
monster_fly_frames = []

duck_frames = []

for i in range(1,6):
    img = pygame.image.load(resource_path(f"assets/player/duck{i}.png")).convert_alpha()
    duck_frames.append(pygame.transform.scale(img,(PLAYER_SIZE,PLAYER_SIZE)))

for i in range(1,5):
    img = pygame.image.load(resource_path(f"assets/obstacles/monster_fly_{i}.png")).convert_alpha()
    monster_fly_frames.append(pygame.transform.scale(img,(60,60)))

for i in range(1,5):

    img = pygame.image.load(resource_path(f"assets/obstacles/monster_small_{i}.png")).convert_alpha()
    monster_small_frames.append(pygame.transform.scale(img,(70,70)))

    img = pygame.image.load(resource_path(f"assets/obstacles/monster_big_{i}.png")).convert_alpha()
    monster_big_frames.append(pygame.transform.scale(img,(90,90)))

    img = pygame.image.load(resource_path(f"assets/obstacles/monster_low_{i}.png")).convert_alpha()
    monster_low_frames.append(pygame.transform.scale(img,(80,50)))

# -----------------------------
# ANIMACIÓN
# -----------------------------

run_index = 0
animation_timer = 0
animation_speed = 6

# -----------------------------
# OBSTÁCULOS
# -----------------------------

obstacles = []
obstacle_width = 40
obstacle_height = 40
obstacle_speed = 6

# -----------------------------
# SCORE
# -----------------------------

score = 0

if not os.path.exists("highscore.txt"):
    with open("highscore.txt", "w") as f:
        f.write("0")

with open("highscore.txt", "r") as f:
    highscore = int(f.read())

# -----------------------------
# GAME STATE
# -----------------------------

MENU = 0
PLAYING = 1
GAME_OVER = 2

game_state = MENU

# -----------------------------
# FUNCIONES
# -----------------------------

def spawn_obstacle():

    obstacle_type = random.choice([
        "rock_small","rock_big","rock_low",
        "monster_small","monster_big","monster_low","monster_fly"
    ])

    x = WIDTH

    if obstacle_type == "rock_small":
        create_obstacle(x, [rock_small], (50,50), (30,30))

    elif obstacle_type == "rock_big":
        create_obstacle(x, [rock_big], (70,70), (40,60))

    elif obstacle_type == "rock_low":
        create_obstacle(x, [rock_low], (60,35), (40,20))

    elif obstacle_type == "monster_small":
        create_obstacle(x, monster_small_frames, (70,70), (40,50))

    elif obstacle_type == "monster_big":
        create_obstacle(x, monster_big_frames, (90,90), (50,70))

    elif obstacle_type == "monster_low":
        create_obstacle(x, monster_low_frames, (80,50), (50,25))
    
    elif obstacle_type == "monster_fly":
         create_obstacle(x, monster_fly_frames, (60,60), (50,50))
         obstacles[-1]["rect"].y -= 60

def spawn_pattern():

    x = WIDTH

    # -------- FASE 1 (inicio) --------
    if score < 800:
        pattern = random.choice(["single","gap"])

    # -------- FASE 2 --------
    elif score < 2000:
        pattern = random.choice(["single","low","gap"])

    # -------- FASE 3 --------
    elif score < 4000:
        pattern = random.choice(["single","low","double_safe"])

    # -------- FASE 4 --------
    else:
        pattern = random.choice(["single","low_big","double_safe","fly_safe"])

    # ---------------- PATTERNS ----------------

    if pattern == "single":
        spawn_obstacle()


    elif pattern == "low":
        create_obstacle(x, [rock_low], (60,35), (40,20))


    elif pattern == "double_safe":
        # 👇 separación REALMENTE saltable
        spacing = get_spacing(180)

        create_obstacle(x, monster_small_frames, (70,70), (40,40))
        create_obstacle(x+ spacing, monster_small_frames, (70,70), (40,40))


    elif pattern == "low_big":

        spacing = get_spacing(200)

        create_obstacle(x, [rock_low], (60,35), (40,20))
        create_obstacle(x+ spacing, monster_big_frames, (90,90), (50,50))


    elif pattern == "fly_safe":
        create_obstacle(x, monster_fly_frames, (80,80), (50,30))
        obstacles[-1]["rect"].y -= 80


    elif pattern == "gap":
        pass

def get_spacing(base=180):

    spacing = base + game_speed * 10

    # usar salto real medido
    if max_jump_distance > 0:
        max_spacing = max_jump_distance * 0.9
    else:
        max_spacing = 300  # fallback por si aún no ha saltado

    return int(min(spacing, max_spacing))

def reset_game():
    global obstacles, player_y, velocity_y, score

    obstacles = []
    player_y = GROUND_Y
    velocity_y = 0
    score = 0

def create_obstacle(x, sprite_frames, sprite_size, hitbox_size):

    sprite_w, sprite_h = sprite_size
    hitbox_w, hitbox_h = hitbox_size

    rect = pygame.Rect(
        x + (sprite_w - hitbox_w)//2,
        GROUND_Y - hitbox_h,
        hitbox_w,
        hitbox_h
    )

    obstacles.append({
        "rect": rect,
        "frames": sprite_frames,
        "frame": 0,
        "sprite_size": sprite_size
    })

# =========================
# SPAWN SYSTEM
# =========================

def get_spacing(base=180):
    return int(base + game_speed * 12)


def get_next_spawn_distance():
    base = 220
    distance = base - game_speed * 5
    return max(140, int(distance))


def generate_sequence():
    global force_gap

    if force_gap:
        force_gap = False
        return ["gap"]

    if score < 800:
        return random.choice([
            ["single"],
            ["single", "gap"],
            ["gap"],
        ])

    elif score < 2000:
        return random.choice([
            ["single", "low"],
            ["low"],
            ["gap"],
        ])

    elif score < 4000:
        return random.choice([
            ["double_safe"],
            ["low", "single"],
        ])

    else:
        return random.choice([
            ["low_big"],
            ["double_safe"],
            ["fly_safe"],
            ["low", "double_safe"],
        ])

def run_next_pattern():
    global pattern_queue

    if not pattern_queue:
        pattern_queue = generate_sequence()

    pattern = pattern_queue.pop(0)
    spawn_pattern(pattern)


def update_spawn():
    global distance_since_spawn, spawn_distance

    distance_since_spawn += game_speed

    if distance_since_spawn >= spawn_distance:

        if len(obstacles) == 0 or obstacles[-1]["rect"].x < WIDTH - 200:

            run_next_pattern()

            distance_since_spawn = 0
            spawn_distance = get_next_spawn_distance()


def spawn_pattern(pattern):
    global force_gap

    x = WIDTH

    if pattern == "single":
        spawn_obstacle()


    elif pattern == "low":
        create_obstacle(x, [rock_low], (60,35), (40,20))


    elif pattern == "double_safe":

        spacing = get_spacing(180)

        create_obstacle(x, monster_small_frames, (70,70), (40,40))
        create_obstacle(x + spacing, monster_small_frames, (70,70), (40,40))

        force_gap = True


    elif pattern == "low_big":

        spacing = get_spacing(200)

        create_obstacle(x, [rock_low], (60,35), (40,20))
        create_obstacle(x + spacing, monster_big_frames, (90,90), (50,50))

        force_gap = True


    elif pattern == "fly_safe":

        create_obstacle(x, monster_fly_frames, (80,80), (50,30))
        obstacles[-1]["rect"].y -= 80


    elif pattern == "gap":
        pass

# -----------------------------
# GAME LOOP
# -----------------------------

running = True

spawn_timer = 0

while running:

    clock.tick(60)

    blink_timer += 1

    glow_timer += 1

    # -------------------------
    # EVENTOS
    # -------------------------

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False


        if event.type == pygame.KEYDOWN:

            # -------- MENU --------
            if game_state == MENU:

                if event.key == pygame.K_SPACE:
                    game_state = PLAYING
                    reset_game()
                    instructions_timer = instructions_duration
            # -------- PLAYING --------
            elif game_state == PLAYING:

                if event.key == pygame.K_SPACE and not is_ducking:
                    jump_buffer_timer = jump_buffer_max

                if event.key == pygame.K_DOWN:
                    if not is_ducking:  
                        is_ducking = True
                        duck_entering = True
                        duck_releasing = False
                        duck_frame = 0

                        if on_ground:
                            for _ in range(3):
                                particles.append([
                                    player_x + 10,
                                    player_y + PLAYER_SIZE - 5,
                                    random.randint(-3, -1),
                                    random.randint(-2, -1)
                                ])

            # -------- GAME OVER --------
            elif game_state == GAME_OVER:

                if event.key == pygame.K_r:
                    game_state = MENU
                    overlay_active = False


        if event.type == pygame.KEYUP:

            if game_state == PLAYING:

                if event.key == pygame.K_SPACE:
                    if velocity_y < 0:
                        velocity_y *= 0.5

                if event.key == pygame.K_DOWN:
                    is_ducking = False
                    duck_entering = False
                    duck_releasing = True
                    duck_frame = 2
                    duck_anim_timer = 0

    if overlay_active:
        overlay_alpha = min(overlay_alpha + 40, 70)

    # -------------------------
    # SHAKE
    # -------------------------
    shake_x = 0
    shake_y = 0

    if shake_timer > 0:
        shake_x = random.randint(-shake_intensity, shake_intensity)
        shake_y = random.randint(-shake_intensity, shake_intensity)
        shake_timer -= 1
    # -------------------------
    # LÓGICA DEL JUEGO
    # -------------------------

    if game_state == PLAYING:

        # SPAWN UFO
        if len(ufos) == 0 and random.randint(0, 200) == 0:

            y = random.randint(30, 120)  # más arriba

            scale = random.uniform(0.4, 0.8)
            size = int(80 * scale), int(40 * scale)

            ufo_scaled = pygame.transform.scale(ufo_img, size)

            # oscuridad del ovni dependiendo de la distancia (tamaño)
            brightness = int(255 * scale)
            dark_surface = pygame.Surface(ufo_scaled.get_size()).convert_alpha()
            dark_surface.fill((brightness, brightness, brightness, 255))
            ufo_scaled.blit(dark_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

            ufos.append({
                "x": WIDTH,
                "y": y,
                "speed": 0.5 + scale * 6,  # 👈 CLAVE
                "img": ufo_scaled
            })
        
        # MOVER UFO 
        for ufo in ufos:
            ufo["x"] -= ufo["speed"]

        # ELIMINAR UFO 
        ufos = [u for u in ufos if u["x"] > -100]


        if instructions_timer > 0:
            instructions_timer -= 1

        # GRAVEDAD
        velocity_y += gravity

        # caída más rápida al agacharse en el aire
        if not on_ground and is_ducking:
            velocity_y += 2

        # partículas continuas de slide
        if is_ducking and on_ground:
            if random.randint(0, 3) == 0:  # no siempre
                particles.append([
                    player_x + 10,
                    player_y + PLAYER_SIZE - 5,
                    random.randint(-5, 1),
                    random.randint(-1, 0)
                ])
        
        player_y += velocity_y

        if not on_ground:
            jump_distance += game_speed

        if player_y >= GROUND_Y - PLAYER_SIZE:

            # detectar aterrizaje (solo 1 frame)
            just_landed = not on_ground

            if just_landed:
                squash_timer = 6

            player_y = GROUND_Y - PLAYER_SIZE
            velocity_y = 0
            on_ground = True
            coyote_timer = coyote_time_max

        else:
            just_landed = False
            on_ground = False
            coyote_timer -= 1


        if jump_buffer_timer > 0 and coyote_timer > 0 and not is_ducking:
            velocity_y = jump_strength
            on_ground = False
            jump_buffer_timer = 0
            coyote_timer = 0

            # -------------------------
            # PARTICULAS DE SALTO
            # -------------------------
            for _ in range(5):
                particles.append([
                    player_x + PLAYER_SIZE // 2,
                    player_y + PLAYER_SIZE,
                    random.randint(-2, 2),
                    random.randint(-3, -1)
                ])

        if jump_distance > max_jump_distance:
           max_jump_distance = jump_distance

        jump_distance = 0

        if jump_buffer_timer > 0:
            jump_buffer_timer -= 1

        if squash_timer > 0:
            squash_timer -= 1

        # -------------------------
        # MOVIMIENTO DEL SUELO
        # -------------------------

        ground_x1 -= game_speed
        ground_x2 -= game_speed

        if ground_x1 <= -800:
            ground_x1 = ground_x2 + 800

        if ground_x2 <= -800:
            ground_x2 = ground_x1 + 800

        # SCROLL BACKGROUND
        bg_x -= bg_speed
        far_x -= far_speed
        mid_x -= mid_speed

        if bg_x <= -WIDTH:
            bg_x = 0
        if far_x <= -WIDTH:
            far_x = 0
        if mid_x <= -WIDTH:
            mid_x = 0

        # PLAYER RECT
        if is_ducking:

            player_rect = pygame.Rect(
                player_x + 25,
                player_y + 45,
                PLAYER_SIZE - 50,
                PLAYER_SIZE - 65
            )

        else:

            player_rect = pygame.Rect(
                player_x + 25,
                player_y + 25,
                PLAYER_SIZE - 50,
                PLAYER_SIZE - 35
            )

        # RUN ANIMATION
        animation_timer += 1

        if animation_timer >= animation_speed:
            run_index = (run_index + 1) % len(run_frames)
            animation_timer = 0

        # -------------------------
        # SELECCIÓN DEL SPRITE
        # -------------------------

        # entrada agacharse (duck)
        if duck_entering:

            if duck_hold_timer > 0:
                duck_hold_timer -= 1
            else:
                duck_frame += 0.3

            if duck_frame >= 2:
                duck_frame = 2
                duck_entering = False

            player_sprite = duck_frames[int(duck_frame)]

        # salida duck (agacharse)
        elif duck_releasing:

            duck_anim_timer += 1

            if duck_anim_timer >= duck_anim_speed:
                duck_frame += 1
                duck_anim_timer = 0

            if duck_frame >= len(duck_frames):
                duck_frame = 0
                duck_releasing = False

            player_sprite = duck_frames[int(duck_frame)]

        # mantener duck
        elif is_ducking:

            player_sprite = duck_frames[2]

        # en el aire
        elif not on_ground:

            if velocity_y < -6:
                player_sprite = jump_up
            elif -6 <= velocity_y <= 3:
                player_sprite = jump_peak
            else:
                player_sprite = jump_down

        # PRIORIDAD 5: correr
        else:

            player_sprite = run_frames[run_index]

        # GENERAR OBSTÁCULOS
        update_spawn()

        # -------------------------
        # MOVER OBSTÁCULOS
        # -------------------------

        for obstacle in obstacles:

            obstacle["rect"].x -= game_speed

            # animación de monstruos
            if len(obstacle["frames"]) > 1:
                obstacle["frame"] += 0.2
                if obstacle["frame"] >= len(obstacle["frames"]):
                    obstacle["frame"] = 0


        # ELIMINAR OBSTÁCULOS FUERA DE PANTALLA
        obstacles = [o for o in obstacles if o["rect"].x > -100]
        # ELIMINAR OVNIS
        ufos = [u for u in ufos if u["x"] > -100]

        # COLISIONES
        for obstacle in obstacles:
            if player_rect.colliderect(obstacle["rect"]):
                game_state = GAME_OVER

                # capturar pantalla al "morir"
                death_screen = screen.copy()

                flash_alpha = 120

                shake_timer = 5
                shake_intensity = 3

                # convertir a blanco y negro
                arr = pygame.surfarray.array3d(death_screen)
                gray = arr.mean(axis=2, keepdims=True)
                gray_arr = gray.repeat(3, axis=2)
                death_screen = pygame.surfarray.make_surface(gray_arr)

                if score > highscore:
                    highscore = score
                    with open("highscore.txt", "w") as f:
                        f.write(str(highscore))

        # SCORE
        score += 1

        # VELOCIDAD PROGRESIVA
        game_speed = 6 + (score / 1000)

    # -------
    # DIBUJAR 
    # -------

    if game_state == MENU:

        screen.blit(menu_bg, (0, 0))

        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(0)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        screen.blit(title_img, (WIDTH // 2 - 120, 15))

        credits = small_font.render("Created by danigatoR", True, (0, 0, 0))
        credits.set_alpha(140)
        screen.blit(credits, (8, HEIGHT - 25))

        credits = small_font.render("v1.0", True, (0, 0, 0))
        credits.set_alpha(140)
        screen.blit(credits, (760, HEIGHT - 25))
        
        if (blink_timer // 30) % 2 == 0:
            text = font.render("Press SPACE to start", True, WHITE)
            screen.blit(text, (WIDTH // 2 - 130, 195))


    elif game_state == PLAYING:

        # BACKGROUND
        screen.blit(bg, (bg_x, 0))
        screen.blit(bg, (bg_x + WIDTH, 0))

        # OVNIS
        for ufo in ufos:
            screen.blit(ufo["img"], (ufo["x"], ufo["y"]))

        screen.blit(fog, (0, 0))

        screen.blit(far, (far_x, GROUND_Y - far.get_height()))
        screen.blit(far, (far_x + WIDTH, GROUND_Y - far.get_height()))

        screen.blit(mid, (mid_x, GROUND_Y - mid.get_height()))
        screen.blit(mid, (mid_x + WIDTH, GROUND_Y - mid.get_height()))

        # SUELO
        screen.blit(ground_img, (ground_x1, GROUND_Y))
        screen.blit(ground_img, (ground_x2, GROUND_Y))

        # PLAYER 
        sprite = player_sprite
        base_sprite = player_sprite
        draw_x = player_x
        draw_y = player_y

        # partículas
        for p in particles:
            p[0] += p[2]
            p[1] += p[3]
            p[3] += 0.2
            pygame.draw.circle(screen, (200, 200, 200), (int(p[0]), int(p[1])), 3)

        particles = [p for p in particles if p[1] < GROUND_Y]

        if not on_ground:
            sprite = pygame.transform.scale(base_sprite, (PLAYER_SIZE, PLAYER_SIZE + 10))
            draw_y = player_y - 10

        elif squash_timer > 0 and not is_ducking:
            progress = squash_timer / 6
            width = PLAYER_SIZE + int(10 * progress)
            height = PLAYER_SIZE - int(10 * progress)
            sprite = pygame.transform.scale(base_sprite, (width, height))
            draw_y = player_y + (PLAYER_SIZE - height)

        else:
            sprite = base_sprite

        screen.blit(sprite, (draw_x, draw_y))

        # OBSTÁCULOS
        for obstacle in obstacles:
            frame_index = int(obstacle["frame"])
            sprite = obstacle["frames"][frame_index]
            rect = obstacle["rect"]
            sprite_w, sprite_h = obstacle["sprite_size"]

            screen.blit(
                sprite,
                (
                    rect.x - (sprite_w - rect.width)//2,
                    rect.y - (sprite_h - rect.height)
                )
            )

        # SCORE
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        highscore_text = font.render(f"Highscore: {highscore}", True, WHITE)
        screen.blit(highscore_text, (10, 40))


    elif game_state == GAME_OVER:

        # imagen congelada
        screen.blit(death_screen, (shake_x, shake_y))

        # FLASH (al morir)
        if flash_alpha > 0:
            flash = pygame.Surface((WIDTH, HEIGHT))
            flash.fill((255, 255, 255))
            flash.set_alpha(flash_alpha)
            screen.blit(flash, (0, 0))

            flash_alpha -= 5

        # oscurecer
        dark = pygame.Surface((WIDTH, HEIGHT))
        dark.fill((0, 0, 0))
        dark.set_alpha(10)
        screen.blit(dark, (0, 0))

        # game over
        screen.blit(gameover_img, (WIDTH // 2 - 110, 60))
        
        if (blink_timer // 30) % 2 == 0:
            restart = font.render("Press R to restart", True, WHITE)
            screen.blit(restart, (WIDTH // 2 - 115, 210))

    # -------------------------
    # INSTRUCCIONES (fade out)
    # -------------------------
    if instructions_timer > 0:

        alpha = int(255 * (instructions_timer / instructions_duration))

        instr1 = small_font.render("SPACE = jump", True, WHITE)
        instr2 = small_font.render("DOWN = duck", True, WHITE)

        instr1.set_alpha(alpha)
        instr2.set_alpha(alpha)

        screen.blit(instr1, (WIDTH // 2 - 70, 60))
        screen.blit(instr2, (WIDTH // 2 - 70, 90))

    pygame.display.update()

pygame.quit()