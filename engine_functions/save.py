import shelve
import os
import sys

def make_dir(path):
	try:
		os.mkdir(path)
	except FileExistsError:
		pass

def return_path():
	if getattr(sys, 'frozen', False):
		return os.path.join(os.path.dirname(sys.executable), 'saves')
	
	return os.path.join(os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'data'), 'saves')


def save_game(game_world, game_map, player, entities, close_entities, msg_log):

	# TODO: Save msglog



	path_of_folder = return_path()
	make_dir(path_of_folder)

	path_of_file = os.path.join(path_of_folder, f"{player.name}")

	with shelve.open(path_of_file, 'n') as file:
		file['game_world'] = game_world
		file['game_map'] = game_map
		file['player'] = player
		file['entities'] = entities
		file['close_entities'] = close_entities
		file['msg_log'] = msg_log

