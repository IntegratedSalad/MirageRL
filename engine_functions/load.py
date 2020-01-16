import shelve
import os

def load_game(name):

	path = os.path.join(os.path.join(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'data'), 'saves'), f"{name}")

	with shelve.open(path, 'r') as file:

		game_world = file['game_world']
		game_map = file['game_map']
		player = file['player']
		entities = file['entities']
		close_entities = file['close_entities']

	return game_world, game_map, player, entities, close_entities
