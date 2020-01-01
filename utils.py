import constants

def enter_new_chunk(px, py):

	""" Returns px, py, mx, my  

	wx - world_x
	wy - world_y

	"""

	if px >= constants.MAP_WIDTH:
		return (1, py, 1, 0)

	elif px <= 0:
		return (constants.MAP_WIDTH - 1, py, -1, 0)

	elif py >= constants.MAP_HEIGHT:
		return (px, 1, 0, 1)

	elif py <= 0:
		return (px, constants.MAP_HEIGHT - 1, 0, -1)

	return None

def get_pos_in_chunk(pos_x, pos_y):

	chunk_x = int(pos_x / constants.MAP_WIDTH) 
	x = pos_x - (chunk_x * constants.MAP_WIDTH)

	chunk_y = int(pos_y / constants.MAP_HEIGHT)
	y = pos_y - (chunk_y * constants.MAP_HEIGHT)

	return (x, y)

