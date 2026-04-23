import pygame
import sys
import random
import os
from settings import *
from utils import draw_text, save_high_score, load_high_score


def game_loop(screen, clock, high_score):
    bg_img = pygame.image.load(os.path.join(IMAGES_DIR, BG_IMAGE)).convert()
    pipe_img = pygame.image.load(os.path.join(IMAGES_DIR, PIPE_IMAGE)).convert_alpha()
    bird_img = pygame.image.load(os.path.join(IMAGES_DIR, BIRD_IMAGE)).convert_alpha()

    bg_img = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
    bird_img = pygame.transform.scale(bird_img, (50, 50))
    pipe_img = pygame.transform.scale(pipe_img, (80, 500))

    # Sounds
    pygame.mixer.init()
    try:
        jump_sound = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, JUMP_SOUND))
        hit_sound = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, HIT_SOUND))
        bgm_path = os.path.join(SOUNDS_DIR, BGM)
        if os.path.exists(bgm_path):
            pygame.mixer.music.load(bgm_path)
            pygame.mixer.music.play(-1)
    except Exception as e:
        print("Sound files not loaded:", e)

    SPAWNPIPE = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWNPIPE, PIPE_SPAWN_MS)

    bird_rect = bird_img.get_rect(center=(100, SCREEN_HEIGHT // 2))
    bird_movement = 0
    pipe_list = []
    scored_pipes = []
    score = 0
    game_active = True
    bg_x = 0

    def reset_game():
        nonlocal bird_rect, bird_movement, pipe_list, scored_pipes, score, game_active, high_score
        high_score = max(score, high_score)
        save_high_score(high_score)
        bird_rect = bird_img.get_rect(center=(100, SCREEN_HEIGHT // 2))
        bird_movement = 0
        pipe_list.clear()
        scored_pipes.clear()
        score = 0
        game_active = True

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
                if 'hit_sound' in locals(): hit_sound.play()
                return False
        if bird_rect.top <= -100 or bird_rect.bottom >= SCREEN_HEIGHT:
            if 'hit_sound' in locals(): hit_sound.play()
            return False
        return True

    def rotate_bird(bird):
        rotated = pygame.transform.rotate(bird, -bird_movement * 2.5)
        return rotated

    def update_score(pipes, bird_rect, score):
        for p in pipes:
            if p.bottom >= SCREEN_HEIGHT and p not in scored_pipes:
                if p.centerx < bird_rect.centerx:
                    score += 1
                    scored_pipes.append(p)
        return score

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                high_score = max(score, high_score)
                save_high_score(high_score)
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game_active:
                        bird_movement = JUMP_STRENGTH
                        if 'jump_sound' in locals(): jump_sound.play()
                    else:
                        reset_game()

            if event.type == SPAWNPIPE:
                pipe_list.extend(create_pipe())

        bg_x -= BG_SCROLL_SPEED
        if bg_x <= -SCREEN_WIDTH:
            bg_x = 0

        screen.blit(bg_img, (bg_x, 0))
        screen.blit(bg_img, (bg_x + SCREEN_WIDTH, 0))

        if game_active:
            bird_movement += GRAVITY
            bird_rect.centery += bird_movement
            rotated_bird = rotate_bird(bird_img)
            screen.blit(rotated_bird, bird_rect)

            pipe_list = move_pipes(pipe_list)
            draw_pipes(pipe_list)

            game_active = check_collision(pipe_list)
            score = update_score(pipe_list, bird_rect, score)
            if score > high_score:
                high_score = score
                save_high_score(high_score)
            draw_text(screen, f"Score: {int(score)}  High: {int(high_score)}", 32, 40)

        else:
            draw_text(screen, "Game Over", 50, SCREEN_HEIGHT//2 - 50)
            draw_text(screen, f"Score: {int(score)}  High: {int(high_score)}", 30, SCREEN_HEIGHT//2 + 10)
            draw_text(screen, "Press SPACE to restart", 24, SCREEN_HEIGHT//2 + 60)

        pygame.display.update()
        clock.tick(FPS)
