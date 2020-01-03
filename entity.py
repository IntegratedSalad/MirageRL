"""A generic object on game that can be interacted in some way"""
import tcod
import tcod.path
import utils
from math import sqrt

class Entity:

	def __init__(self, x, y, char, color, name, blocks=False, fighter=None, ai=None):
	    self.x = x
	    self.y = y
	    self.char = char
	    self.color = color
	    self.name = name
	    self.blocks = blocks
	    self.fighter = fighter
	    self.ai = ai

	    if self.fighter:
	    	self.fighter.owner = self

	    if self.ai:
	    	self.ai.owner = self


	def move(self, dx, dy):
	    self.x += dx
	    self.y += dy


	@property
	def position_in_chunk(self):
		return utils.get_pos_in_chunk(self.x, self.y)


	def move_towards(self, target_x, target_y, game_map, entities):
		# map_x, map_y = self.position_in_chunk
		# dx = target_x - map_x
		# dy = target_y - map_y

		dx = target_x - self.x
		dy = target_y - self.y

		distance = sqrt(dx ** 2 + dy ** 2)

		dx = int(round(dx / distance))
		dy = int(round(dy / distance))

		if not (game_map.is_blocked(self.x + dx, self.y + dy) or get_blocking_entities_at_location(entities, self.x + dx, self.y + dy)):
			self.move(dx, dy)

	def distance_to(self, other):
		# map_x, map_y = self.position_in_chunk

		# dx = other.x - map_x
		# dy = other.y - map_y

		dx = other.x - self.x
		dy = other.y - self.y

		return sqrt(dx ** 2 + dy ** 2)


	"""
	For now, positions in move_astar are world positions. If it gets slow, we will use chunk cords accordingly to where the monster is.
	
	"""

	# def move_astar(self, target, entities, game_map): # it can overshoot, because of how we are setting map - see map_bjects.game_map.initialize_chunk range(1, ...)
	# 	inframap = tcod.map.Map(game_map.width, game_map.height) # map used in above map

	# 	for entity in entities:
	# 		if entity.blocks and entity != self and entity != target:

	# 			map_x, map_y = entity.position_in_chunk

	# 			inframap.transparent[map_x, map_y] = True
	# 			inframap.walkable[map_x, map_y] = False

	# 	monster_path = tcod.path.AStar(inframap, diagonal=1.41)

	# 	self_map_x, self_map_y = self.position_in_chunk
	# 	target_map_x, target_map_y = target.position_in_chunk
	# 	tcod.path_compute(monster_path, self_map_x, self_map_y, target_map_x, target_map_y)

	# 	print(f"MON: {self_map_x, self_map_y}")
	# 	print(f"TARG: {target_map_x, target_map_y}")
	# 	print(f"MON WORLD: {self.x, self.y}")
	# 	print(tcod.path_size(monster_path))

	# 	if not tcod.path_is_empty(monster_path) and tcod.path_size(monster_path) < 25:
	# 		x, y = tcod.path_walk(monster_path, True)

	# 		if x or y:
	# 			self.x = x
	# 			self.y = y

	# 	else:
	# 		self.move_towards(target_map_x, target_map_y, game_map, entities)

	def move_astar(self, target, entities, game_map): # it can overshoot, because of how we are setting map - see map_bjects.game_map.initialize_chunk range(1, ...)
		inframap = tcod.map.Map(450, 450) # map used in above map

		for entity in entities:
			if entity.blocks and entity != self and entity != target:

				inframap.transparent[entity.x, entity.y] = True
				inframap.walkable[entity.x, entity.y] = False

		monster_path = tcod.path.AStar(inframap, diagonal=1.41)

		tcod.path_compute(monster_path, self.x, self.y, target.x, target.y)

		print(f"PLAYER WORLD: {target.x, target.y}")
		print(f"MON WORLD: {self.x, self.y}")
		# print(tcod.path_size(monster_path))

		if not tcod.path_is_empty(monster_path) and tcod.path_size(monster_path) < 25:
			x, y = tcod.path_walk(monster_path, True)

			if x or y:
				self.x = x
				self.y = y

		else:
			self.move_towards(target.x, target.y, game_map, entities)

def get_blocking_entities_at_location(entities, x, y):
	for entity in entities:
		if entity.blocks and entity.x == x and entity.y == y:
			return entity

	return None
