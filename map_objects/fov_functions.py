import tcod
from constants import FOV_LIGHT_WALLS, FOV_ALGO

def init_fov(game_map):

	fov_map = tcod.map_new(game_map.width, game_map.height)

	for y in range(game_map.height):
		for x in range(game_map.width):
			tcod.map_set_properties(fov_map, x, y, not game_map.tiles[x][y].block_sight, not game_map.tiles[x][y].blocked)

	return fov_map

def recomputer_fov(fov_map, x, y, radius, light_walls=FOV_LIGHT_WALLS, algorithm=FOV_ALGO):
	tcod.map_compute_fov(fov_map, x, y, radius, light_walls, algorithm)