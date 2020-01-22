import shelve
import sys
import os

def return_path(): # add that to utils
	if getattr(sys, 'frozen', False):
		return os.path.join(os.path.dirname(sys.executable), 'saves')
	
	return os.path.join(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'data'), 'saves')


def load_game(name):

	path = return_path()

	with shelve.open(os.path.join(path, name), 'r') as file:

		game_world = file['game_world']
		game_map = file['game_map']
		player = file['player']
		entities = file['entities']
		close_entities = file['close_entities']
		msg_log = file['msg_log']

	return game_world, game_map, player, entities, close_entities, msg_log
