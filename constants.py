"""A constants file."""

import tcod

title = "Mirage RL"
version = "0.0.7 - Of Title."

SCREEN_WIDTH = 60
SCREEN_HEIGHT = 55
# World and Map dimensions must always be a square!
MAP_WIDTH = 45
MAP_HEIGHT = 45
WORLD_WIDTH = 10
WORLD_HEIGHT = 10
if (MAP_WIDTH != MAP_HEIGHT) or (WORLD_WIDTH != WORLD_HEIGHT):
	raise ValueError("Dimensions are not squares!")
#
MAX_MONSTERS_PER_CHUNK = 3
PLAYER_NAME = "Pysio"
FOV_ALGO = 0
FOV_LIGHT_WALLS = True
FOV_RADIUS_BELOW = 4
COLOR_LIGHTER = 30 # a value, that adds to the RGB - lights up the color | Saturation
GLYPHS_NUM = 8
DISTANCE_TO_PROCESS_ENTITY = 7
