import tcod
from data.game_data import constants
import os
import sys
from map_objects.game_world import GameWorld
from map_objects.game_map import GameMap
from components.fighter import Fighter
from components.item import Item
from components.entity import Entity
from map_objects.chunk import ChunkProperty
from ui_objects.render_order import RenderOrder
from misc.action_functions import *

def init_game():
	if getattr(sys, 'frozen', False):
		# init in executable
		path = os.path.join(os.path.dirname(sys.executable), 'terminal8x8_gs_tc.png')
	else:
		path = os.path.join(os.path.join(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'data'), 'game_data'), 'terminal8x8_gs_tc.png')
	
	if path is not None:
		tcod.console_set_custom_font(path, tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)
	else:
		tcod.console_set_custom_font('terminal8x8_gs_tc.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)

def init_new_game():

	game_world = GameWorld()

	player_fighter_component = Fighter(hp=200, defense=2, attack_value=20)
	player = Entity(int((constants.WORLD_WIDTH * constants.MAP_WIDTH / 2) + constants.MAP_WIDTH / 2), 
		int((constants.WORLD_HEIGHT * constants.MAP_HEIGHT / 2) + constants.MAP_HEIGHT / 2), '@', tcod.white, 
		constants.PLAYER_NAME, RenderOrder.ENTITY, fighter=player_fighter_component)

	hp_potion_item_component = Item(use_func=action_heal, heal_amount=10, category='consumables') # Item creation will be created through JSON.
	hp_potion = Entity(player.x, player.y + 1, '!', tcod.red, 'Health Potion', RenderOrder.ITEM, item=hp_potion_item_component)
	print(hp_potion.x, hp_potion.y)

	hp_potion_item_component = Item(use_func=action_heal, heal_amount=10, category='consumables') # Item creation will be created through JSON.
	hp_potion_second = Entity(player.x, player.y + 2, '!', tcod.red, 'Health Potion', RenderOrder.ITEM, item=hp_potion_item_component)
	print(hp_potion.x, hp_potion.y)

	px, py = game_world.get_chunk_pos_from_player_pos(player.x, player.y)
	game_world.chunks[px][py].property = ChunkProperty.START
	game_map = GameMap(constants.MAP_WIDTH, constants.MAP_HEIGHT, game_world.chunks[px][py])
	print(f"PLAYER POS: {player.x}, {player.y}")

	print(f"CURRENT CHUNK: {px} {py}")

	entities = [player, hp_potion, hp_potion_second]
	close_entities = []
	game_map.place_entities(px, py, entities)

	return {'game_world': game_world, 'player': player, 'game_map': game_map, 'entities': entities, 
	'close_entities': close_entities}
