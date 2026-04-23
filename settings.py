import os

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FPS = 120

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
IMAGES_DIR = os.path.join(ASSETS_DIR, "images")
SOUNDS_DIR = os.path.join(ASSETS_DIR, "sounds")
DATA_DIR = os.path.join(BASE_DIR, "data")
SCORE_FILE = os.path.join(DATA_DIR, "score.txt")

BG_SCROLL_SPEED = 2
GRAVITY = 0.2
JUMP_STRENGTH = -6
PIPE_GAP = 170
PIPE_SPEED = 3
PIPE_SPAWN_MS = 1200

BG_IMAGE = "bg.png"
PIPE_IMAGE = "pipe.png"
BIRD_IMAGE = "Jumpy.png"

# Sounds
JUMP_SOUND = "jump.wav"
HIT_SOUND = "hit.mp3"
BGM = "bgm.mp3"

FONT_NAME = "arial"
