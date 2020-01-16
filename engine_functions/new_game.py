import tcod
import constants
from map_objects.game_world import GameWorld
from map_objects.game_map import GameMap
from components.fighter import Fighter
from entity import Entity
from map_objects.chunk import ChunkProperty

def init_game():

	tcod.console_set_custom_font('terminal8x8_gs_tc.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)

def init_new_game():

	game_world = GameWorld()

	player_fighter_component = Fighter(8, 2, 20)
	player = Entity(int((constants.WORLD_WIDTH * constants.MAP_WIDTH / 2) + constants.MAP_WIDTH / 2), int((constants.WORLD_HEIGHT * constants.MAP_HEIGHT / 2) + constants.MAP_HEIGHT / 2), '@', tcod.white, constants.PLAYER_NAME, fighter=player_fighter_component)
	px, py = game_world.get_chunk_pos_from_player_pos(player.x, player.y)
	game_world.chunks[px][py].property = ChunkProperty.START
	game_map = GameMap(constants.MAP_WIDTH, constants.MAP_HEIGHT, game_world.chunks[px][py])
	print(f"PLAYER POS: {player.x}, {player.y}")

	print(f"CURRENT CHUNK: {px} {py}")

	entities = [player]
	close_entities = []
	game_map.place_entities(px, py, entities)

	return {'game_world': game_world, 'player': player, 'game_map': game_map, 'entities': entities, 
	'close_entities': close_entities}
