import sys
import os
import pygame


BASE_TILE_SIZE = 16
SCALE_FACTOR = 1.75
PIXEL_RES = int(BASE_TILE_SIZE * SCALE_FACTOR)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BORDER = 15

camera_offset = (0, 0)

FPS = 60
DT = 1/FPS
# Handle frozen executables (cx_Freeze)
if getattr(sys, 'frozen', False):
    # Running as compiled executable
    ASSETS_DIR = os.path.join(os.path.dirname(sys.executable), "game/assets")
else:
    # Running as script
    ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")

SPRITES_DIR = os.path.join(ASSETS_DIR, "sprites/")
SOUNDS_DIR = os.path.join(ASSETS_DIR, "sounds/")
DIALOGUE_DIR = os.path.join(ASSETS_DIR, "dialogue/")
UI_PATH = os.path.join(ASSETS_DIR, "ui/")

FONT = pygame.font.Font(os.path.join(UI_PATH, "pixelfont.ttf"), 20)