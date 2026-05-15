import asyncio
import pygame
import sys
import random
import os
from settings import *
from utils import draw_text, save_high_score

async def game_loop(screen, clock, high_score):
    
    def load_img(name, size, fallback_color):
        path = os.path.join(IMAGES_DIR, name)
        if os.path.exists(path):
            img = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(img, size)
        surf = pygame.Surface(size)
        surf.fill(fallback_color)
        return surf

    bg_img = load_img(BG_IMAGE, (SCREEN_WIDTH, SCREEN_HEIGHT), (135, 206, 235))
    bird_img = load_img(BIRD_IMAGE, (50, 50), (255, 255, 0))
    pipe_img = load_img(PIPE_IMAGE, (80, 500), (0, 255, 0))

    pygame.mixer.init()
    jump_sound = None
    hit_sound = None
    try:
        if os.path.exists(os.path.join(SOUNDS_DIR, JUMP_SOUND)):
            jump_sound = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, JUMP_SOUND))
        if os.path.exists(os.path.join(SOUNDS_DIR, HIT_SOUND)):
            hit_sound = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, HIT_SOUND))
        
        bgm_path = os.path.join(SOUNDS_DIR, BGM)
        if os.path.exists(bgm_path):
            pygame.mixer.music.load(bgm_path)
            pygame.mixer.music.play(-1)
    except Exception as e:
        print("Audio load warning:", e)

    last_pipe_spawn = pygame.time.get_ticks()
    
    # Audio pause tracking
    bgm_paused = False
    game_over_time = 0

    bird_rect = bird_img.get_rect(center=(100, SCREEN_HEIGHT // 2))
    bird_movement = 0
    pipe_list = []
    scored_pipes = []
    score = 0
    game_active = True
    bg_x = 0
    
    # Game Over Menu state
    go_options = ["Restart", "Main Menu"]
    go_selected = 0

    def reset_game():
            nonlocal bird_rect, bird_movement, pipe_list, scored_pipes, score, game_active, high_score, last_pipe_spawn, bgm_paused, go_selected
            high_score = max(score, high_score)
            save_high_score(high_score)
            bird_rect = bird_img.get_rect(center=(100, SCREEN_HEIGHT // 2))
            bird_movement = 0
            pipe_list.clear()
            scored_pipes.clear()
            score = 0
            game_active = True
            go_selected = 0
            last_pipe_spawn = pygame.time.get_ticks()
            
            # --- NEW AUDIO RESET LOGIC ---
            # Stop all playing sound effects (like the hit sound)
            pygame.mixer.stop()
            
            # Stop the background music completely, then restart it from the beginning
            pygame.mixer.music.stop()
            pygame.mixer.music.play(-1)
            bgm_paused = False

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
        # Sound logic is removed from here so we can control it centrally in the main loop
        for p in pipes:
            if bird_rect.colliderect(p):
                return False
        if bird_rect.top <= -100 or bird_rect.bottom >= SCREEN_HEIGHT:
            return False
        return True

    def rotate_bird(bird):
        rot = max(-90, min(bird_movement * -3, 30))
        return pygame.transform.rotate(bird, rot)

    def update_score(pipes, bird_rect, score):
        for p in pipes:
            if p.bottom >= SCREEN_HEIGHT and p not in scored_pipes:
                if p.centerx < bird_rect.centerx:
                    score += 1
                    scored_pipes.append(p)
        return score

    def perform_jump():
        nonlocal bird_movement
        bird_movement = JUMP_STRENGTH
        if jump_sound: jump_sound.play()

    while True:
        current_time = pygame.time.get_ticks()
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False
        
        was_active = game_active

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                high_score = max(score, high_score)
                save_high_score(high_score)
                pygame.quit()
                sys.exit()

            # Touch / Click Logic
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_clicked = True
                if game_active:
                    perform_jump()

            # Keyboard Logic
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_active:
                    perform_jump()
                
                # Game Over Menu Keyboard Navigation
                elif not game_active:
                    if event.key == pygame.K_UP:
                        go_selected = (go_selected - 1) % len(go_options)
                    elif event.key == pygame.K_DOWN:
                        go_selected = (go_selected + 1) % len(go_options)
                    elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        mouse_clicked = True # Trigger the click logic below

        if game_active and current_time - last_pipe_spawn > PIPE_SPAWN_MS:
            pipe_list.extend(create_pipe())
            last_pipe_spawn = current_time

        bg_x -= BG_SCROLL_SPEED
        if bg_x <= -SCREEN_WIDTH:
            bg_x = 0

        screen.blit(bg_img, (bg_x, 0))
        screen.blit(bg_img, (bg_x + SCREEN_WIDTH, 0))

        if game_active:
            bird_movement += GRAVITY
            bird_rect.centery += bird_movement
            
            rotated_bird = rotate_bird(bird_img)
            rotated_rect = rotated_bird.get_rect(center=bird_rect.center)
            screen.blit(rotated_bird, rotated_rect)

            pipe_list = move_pipes(pipe_list)
            draw_pipes(pipe_list)

            game_active = check_collision(pipe_list)
            
            # --- DEATH LOGIC TRIGGERS HERE ---
            if not game_active and was_active: 
                if hit_sound: hit_sound.play()
                pygame.mixer.music.pause()
                bgm_paused = True
                game_over_time = current_time

            score = update_score(pipe_list, bird_rect, score)
            if score > high_score:
                high_score = score
                
            draw_text(screen, f"Score: {int(score)}  High: {int(high_score)}", 32, 40)

        else:
            # --- GAME OVER STATE ---
            
            # Resume BGM after 1.5 seconds (4600 ms)
            if bgm_paused and current_time - game_over_time >= 4600:
                pygame.mixer.music.unpause()
                bgm_paused = False

            draw_text(screen, "Game Over", 50, SCREEN_HEIGHT//2 - 80)
            draw_text(screen, f"Score: {int(score)}  High: {int(high_score)}", 30, SCREEN_HEIGHT//2 - 30)
            
            # Draw interactive Game Over Menu
            for i, opt in enumerate(go_options):
                color = (255, 255, 0) if i == go_selected else (255, 255, 255)
                prefix = "> " if i == go_selected else "  "
                rect = draw_text(screen, prefix + opt, 30, SCREEN_HEIGHT//2 + 30 + i * 40, color=color)
                
                # Check for hover/touch
                if rect.collidepoint(mouse_pos):
                    go_selected = i
                    if mouse_clicked:
                        if opt == "Restart":
                            reset_game()
                        elif opt == "Main Menu":
                            # Save score before exiting
                            save_high_score(high_score)
                            return  # Exits the game_loop, dropping you back to main.py's menu

        pygame.display.update()
        clock.tick(FPS)
        await asyncio.sleep(0)