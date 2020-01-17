import shelve
import os

def save_game(game_world, game_map, player, entities, close_entities):

	path = os.path.join(os.path.join(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'data'), 'saves'), f"{player.name}")

	with shelve.open(path, 'n') as file:
		file['game_world'] = game_world
		file['game_map'] = game_map
		file['player'] = player
		file['entities'] = entities
		file['close_entities'] = close_entities

