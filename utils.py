import os
from pathlib import Path
import pygame
from settings import SCORE_FILE, DATA_DIR, FONT_NAME, SCREEN_WIDTH


def ensure_data_paths():
    Path(DATA_DIR).mkdir(parents=True, exist_ok=True)
    if not os.path.exists(SCORE_FILE):
        with open(SCORE_FILE, "w") as f:
            f.write("0")


def load_high_score():
    ensure_data_paths()
    try:
        with open(SCORE_FILE, "r") as f:
            content = f.read().strip()
            return int(content) if content else 0
    except Exception:
        return 0


def save_high_score(score: int):
    ensure_data_paths()
    try:
        with open(SCORE_FILE, "w") as f:
            f.write(str(int(score)))
    except Exception as e:
        print("Failed to save score:", e)


def draw_text(surface, text, size, y, centerx=SCREEN_WIDTH//2, bold=True, color=(255, 255, 255)):
    font = pygame.font.SysFont(FONT_NAME, size, bold)
    render = font.render(text, True, color)
    rect = render.get_rect(center=(centerx, y))
    surface.blit(render, rect)
