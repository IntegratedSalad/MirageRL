import constants
from collections import abc

def get_pos_in_chunk(pos_x, pos_y):

	"""
	Returns x, y in chunk, that is between 0 and MAP_WIDTH or MAP_HEIGHT from world position, 
	that is between 0 and WORLD_WIDTH * MAP_WIDTH or WORLD_HEIGHT * MAP_HEIGHT.

	"""

	chunk_x = int(pos_x / constants.MAP_WIDTH) 
	x = pos_x - (chunk_x * constants.MAP_WIDTH)

	chunk_y = int(pos_y / constants.MAP_HEIGHT)
	y = pos_y - (chunk_y * constants.MAP_HEIGHT)

	return (x, y)

def get_chunk_pos(x, y):

    x = int(x / constants.MAP_WIDTH)
    y = int(y / constants.MAP_HEIGHT)

    return (x, y)


def enter_new_chunk(px, py):

	if (px >= constants.MAP_WIDTH) or (px < 0) or (py >= constants.MAP_HEIGHT) or (py < 0):
		return True

	return False


def nested_dict_iter(nested):

	for key, value in nested.items():
		if isinstance(value, abc.Mapping):
			yield from nested_dict_iter(value)
		else:
			yield key, value


def desaturate(color, val):

	des_color = color - val

	return des_color if des_color >= 0 else 0 
