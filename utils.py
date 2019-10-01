import constants

def enter_new_chunk(px, py):

	""" Returns px, py, mx, my  

	mx - map_x
	my - map_y

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