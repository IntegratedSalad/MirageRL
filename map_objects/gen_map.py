from map_objects.map_utils import CA_CaveFactory as CA_map
import constants


def generate_map_list():

	map_obj = CA_map(constants.MAP_HEIGHT, constants.MAP_WIDTH)
	map_list = map_obj.gen_map()
	return map_list
