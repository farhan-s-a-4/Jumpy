import asyncio
import pygame
import sys
import os
from settings import *
from utils import draw_text, load_high_score
from jumpy import game_loop

async def show_credits(screen, clock):
    credits_text = [
        "Jumpy",
        "A fan-made game inspired by Flappy Bird",
        "Built using Pygame module of PYTHON",
        "Programming & Design by:",
        "Farhan Shariar Arnob",
        "Department Of Computer Science and Engineering,",
        "University of Rajshahi",
        "GitHub: https://github.com/farhan-s-a-4"
    ]
    showing = True
    while showing:
        screen.fill((0, 0, 0))
        for i, line in enumerate(credits_text):
            draw_text(screen, line, 19, 140 + i * 50)

        draw_text(screen, "Press ESC or Tap anywhere to return", 22, SCREEN_HEIGHT - 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                showing = False
            # Allow touch/click to exit credits on mobile
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                showing = False

        pygame.display.update()
        clock.tick(FPS)
        await asyncio.sleep(0)

async def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Jumpy")
    clock = pygame.time.Clock()

    high_score = load_high_score()

    bg_path = os.path.join(IMAGES_DIR, BG_IMAGE)
    if os.path.exists(bg_path):
        bg_img = pygame.image.load(bg_path).convert()
        bg_img = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
    else:
        bg_img = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        bg_img.fill((135, 206, 235))

    menu_options = ["Start Game", "Credits", "Exit"]
    selected = 0

    running = True
    while running:
        screen.blit(bg_img, (0, 0))
        
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = False

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Mobile Tap / Mouse Click
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_clicked = True

            # Keyboard Input
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(menu_options)
                if event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(menu_options)
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    mouse_clicked = True # Trick the system into executing the selection

        # Draw Menu and handle clicks
        for i, option in enumerate(menu_options):
            color = (255, 255, 0) if i == selected else (255, 255, 255)
            prefix = "> " if i == selected else "  "
            
            # The rect returned from draw_text lets us check for touch/clicks!
            rect = draw_text(screen, prefix + option, 36, 200 + i * 60, centerx=SCREEN_WIDTH//2, bold=True, color=color)
            
            if rect.collidepoint(mouse_pos):
                selected = i # Highlight what the mouse/finger hovers over
                if mouse_clicked:
                    choice = menu_options[selected]
                    if choice == "Start Game":
                        await game_loop(screen, clock, high_score)
                        high_score = load_high_score()
                    elif choice == "Credits":
                        await show_credits(screen, clock)
                    elif choice == "Exit":
                        pygame.quit()
                        sys.exit()

        pygame.display.update()
        clock.tick(FPS)
        await asyncio.sleep(0)

if __name__ == "__main__":
    asyncio.run(main())
