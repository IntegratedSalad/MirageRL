"""A generic object on game that can be interacted in some way"""
import tcod
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

	def move_towards(self, target_x, target_y, game_map, entities):
		dx = target_x - self.x
		dy = target_y - self.y

		distance = math.sqrt(dx ** 2 + dy ** 2)

		dx = int(round(dx / distance))
		dy = int(round(dy / distance))

		if not (game_map.is_blocked(self.x + dx, self.y + dy) or get_blocking_entities_at_location(entities, self.x + dx, self.y + dy)):
			self.move(dx, dy)

	def distance_to(self, other):

		dx = other.x - self.x
		dy = other.y - self.y

		return sqrt(dx ** 2 + dy ** 2)

	def move_astar(self, target, entities, game_map): # it can overshoot, because of how we are setting map - see map_bjects.game_map.initialize_chunk range(1, ...)
		fov = tcod.map_new(game_map.width, game_map.height)

		for y1 in range(game_map.height):
			for x1 in range(game_map.width):
				tcod.map_set_properties(fov, x1, y1, not game_map.chunk[x1][y1].block_sight, not game_map.chunk[x1][y1].blocked)

		for entity in entities:
			if entity.blocks and entity != self and entity != target:
				tcod.map_set_properties(fov, entity.x, entity.y, True, False)

		my_path = tcod.path_new_using_map(fov, 1.41)

		tcod.path_compute(my_path, self.x, self.y, target.x, target.y)

		if not tcod.path_is_empty(my_path) and tcod.path_size(my_path) < 25:
			x, y = tcod.path_walk(my_path, True)

			if x or y:
				self.x = x
				self.y = y
		else:
			self.move_towards(target.x, target.y, game_map, entities)

		tcod.path_delete(my_path)

def get_blocking_entities_at_location(entities, x, y):
	for entity in entities:
		if entity.blocks and entity.x == x and entity.y == y:
			return entity

	return None
