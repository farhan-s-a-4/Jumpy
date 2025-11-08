import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Window setup
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FPS = 120

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Jumpy")

bg_img = pygame.image.load("bg.png").convert()
pipe_img = pygame.image.load("pipe.png").convert_alpha()
bird_img = pygame.image.load("python.png").convert_alpha()

# Scale images
bg_img = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
bird_img = pygame.transform.scale(bird_img, (50, 50))
pipe_img = pygame.transform.scale(pipe_img, (80, 500))

# Background scrolling
bg_x = 0
BG_SCROLL_SPEED = 2

# Bird setup
bird_rect = bird_img.get_rect(center=(100, SCREEN_HEIGHT // 2))
bird_movement = 0
gravity = 0.2
jump_strength = -6

# Pipes setup
PIPE_GAP = 170
PIPE_SPEED = 3
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)

def create_pipe():
    random_pipe_pos = random.randint(200, 400)
    bottom_pipe = pipe_img.get_rect(midtop=(SCREEN_WIDTH + 50, random_pipe_pos))
    top_pipe = pipe_img.get_rect(midbottom=(SCREEN_WIDTH + 50, random_pipe_pos - PIPE_GAP))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for p in pipes:
        p.centerx -= PIPE_SPEED
    return [p for p in pipes if p.right > 0]

def draw_pipes(pipes):
    for p in pipes:
        if p.bottom >= SCREEN_HEIGHT:
            screen.blit(pipe_img, p)
        else:
            flip_pipe = pygame.transform.flip(pipe_img, False, True)
            screen.blit(flip_pipe, p)

def check_collision(pipes):
    for p in pipes:
        if bird_rect.colliderect(p):
            return False
    if bird_rect.top <= -100 or bird_rect.bottom >= SCREEN_HEIGHT:
        return False
    return True

def rotate_bird(bird):
    rotated = pygame.transform.rotate(bird, -bird_movement * 2.5)
    return rotated

def show_text(text, size, y):
    font = pygame.font.SysFont("arial", size, True)
    render = font.render(text, True, (255, 255, 255))
    rect = render.get_rect(center=(SCREEN_WIDTH//2, y))
    screen.blit(render, rect)

# Game variables
game_active = True
score = 0
high_score = 0

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_active:
                    bird_movement = jump_strength
                else:
                    # Restart game
                    game_active = True
                    pipe_list.clear()
                    bird_rect.center = (100, SCREEN_HEIGHT // 2)
                    bird_movement = 0
                    score = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

    # Background scroll
    bg_x -= BG_SCROLL_SPEED
    if bg_x <= -SCREEN_WIDTH:
        bg_x = 0

    screen.blit(bg_img, (bg_x, 0))
    screen.blit(bg_img, (bg_x + SCREEN_WIDTH, 0))

    if game_active:
        # Bird
        bird_movement += gravity
        bird_rect.centery += bird_movement
        rotated_bird = rotate_bird(bird_img)
        screen.blit(rotated_bird, bird_rect)

        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        # Collision
        game_active = check_collision(pipe_list)

        # Score update
        for p in pipe_list:
            if p.centerx == bird_rect.centerx:
                score += 0.5  # each pipe pair counts once
        show_text(f"Score: {int(score)}", 32, 50)

    else:
        high_score = max(score, high_score)
        show_text("Game Over", 50, SCREEN_HEIGHT//2 - 50)
        show_text(f"Score: {int(score)}  High: {int(high_score)}", 30, SCREEN_HEIGHT//2 + 20)
        show_text("Press SPACE to Restart", 24, SCREEN_HEIGHT//2 + 70)

    pygame.display.update()
    clock.tick(FPS)
